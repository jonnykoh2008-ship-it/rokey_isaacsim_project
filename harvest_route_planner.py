"""개인 PC 1에서 실행 가능한 planning-proxy 기반 전역 waypoint planner."""

from dataclasses import dataclass

import numpy as np


SHAPE_SPHERE = 1
SHAPE_BOX = 2
SHAPE_CAPSULE = 3

PREGRASP_DISTANCE_M = 0.15
STAGING_DISTANCE_M = 0.30
OUTSIDE_OFFSET_M = 0.45
SIDE_OFFSET_M = 0.20
SAMPLE_SPACING_M = 0.03


class RoutePlanningError(RuntimeError):
    """안전한 waypoint 후보를 찾지 못했을 때 발생한다."""


@dataclass(frozen=True)
class Proxy:
    obstacle_id: str
    shape: int
    position: np.ndarray
    orientation_xyzw: np.ndarray
    dimensions: np.ndarray
    safety_margin: float

    def __post_init__(self):
        position = np.asarray(self.position, dtype=float)
        orientation = np.asarray(self.orientation_xyzw, dtype=float)
        dimensions = np.asarray(self.dimensions, dtype=float)
        if position.shape != (3,) or not np.all(np.isfinite(position)):
            raise ValueError(f"{self.obstacle_id}: proxy position이 유효하지 않습니다.")
        if orientation.shape != (4,) or not np.all(np.isfinite(orientation)):
            raise ValueError(f"{self.obstacle_id}: proxy orientation이 유효하지 않습니다.")
        if dimensions.shape != (3,) or not np.all(np.isfinite(dimensions)):
            raise ValueError(f"{self.obstacle_id}: proxy dimensions가 유효하지 않습니다.")
        if np.linalg.norm(orientation) <= 1e-12:
            raise ValueError(f"{self.obstacle_id}: proxy quaternion이 0입니다.")
        if not np.isfinite(self.safety_margin) or self.safety_margin < 0.0:
            raise ValueError(f"{self.obstacle_id}: safety margin이 유효하지 않습니다.")
        object.__setattr__(self, "position", position)
        object.__setattr__(self, "orientation_xyzw", orientation / np.linalg.norm(orientation))
        object.__setattr__(self, "dimensions", dimensions)


@dataclass(frozen=True)
class PlannedRoute:
    name: str
    positions: tuple
    orientation_xyzw: np.ndarray
    minimum_clearance: float
    closest_obstacle: str


def validate_scene_version(scene_reset_id, scene_version, state_reset_id, state_version):
    """계획 입력 snapshot이 현재 GPU simulation 세대와 같은지 검사한다."""
    if int(scene_reset_id) != int(state_reset_id) or int(scene_version) != int(
        state_version
    ):
        raise RoutePlanningError(
            "planning scene version mismatch: "
            f"scene={scene_reset_id}/{scene_version}, "
            f"state={state_reset_id}/{state_version}"
        )


def _quaternion_matrix_xyzw(quaternion):
    x, y, z, w = np.asarray(quaternion, dtype=float)
    return np.array(
        [
            [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
        ],
        dtype=float,
    )


def _matrix_quaternion_xyzw(matrix):
    matrix = np.asarray(matrix, dtype=float)
    trace = float(np.trace(matrix))
    if trace > 0.0:
        scale = np.sqrt(trace + 1.0) * 2.0
        quaternion = np.array(
            [
                (matrix[2, 1] - matrix[1, 2]) / scale,
                (matrix[0, 2] - matrix[2, 0]) / scale,
                (matrix[1, 0] - matrix[0, 1]) / scale,
                0.25 * scale,
            ]
        )
    else:
        index = int(np.argmax(np.diag(matrix)))
        if index == 0:
            scale = np.sqrt(1.0 + matrix[0, 0] - matrix[1, 1] - matrix[2, 2]) * 2.0
            quaternion = np.array(
                [
                    0.25 * scale,
                    (matrix[0, 1] + matrix[1, 0]) / scale,
                    (matrix[0, 2] + matrix[2, 0]) / scale,
                    (matrix[2, 1] - matrix[1, 2]) / scale,
                ]
            )
        elif index == 1:
            scale = np.sqrt(1.0 + matrix[1, 1] - matrix[0, 0] - matrix[2, 2]) * 2.0
            quaternion = np.array(
                [
                    (matrix[0, 1] + matrix[1, 0]) / scale,
                    0.25 * scale,
                    (matrix[1, 2] + matrix[2, 1]) / scale,
                    (matrix[0, 2] - matrix[2, 0]) / scale,
                ]
            )
        else:
            scale = np.sqrt(1.0 + matrix[2, 2] - matrix[0, 0] - matrix[1, 1]) * 2.0
            quaternion = np.array(
                [
                    (matrix[0, 2] + matrix[2, 0]) / scale,
                    (matrix[1, 2] + matrix[2, 1]) / scale,
                    0.25 * scale,
                    (matrix[1, 0] - matrix[0, 1]) / scale,
                ]
            )
    return quaternion / np.linalg.norm(quaternion)


def approach_orientation_xyzw(robot_position, apple_position):
    """palm +Y가 world +Z이고 palm +X가 로봇→사과 수평축인 자세."""
    horizontal = np.asarray(apple_position, dtype=float) - np.asarray(
        robot_position, dtype=float
    )
    horizontal[2] = 0.0
    norm = float(np.linalg.norm(horizontal))
    if norm <= 1e-9:
        raise RoutePlanningError("로봇과 사과의 수평 위치가 같아 접근 자세를 만들 수 없습니다.")
    x_axis = horizontal / norm
    y_axis = np.array([0.0, 0.0, 1.0])
    z_axis = np.cross(x_axis, y_axis)
    return _matrix_quaternion_xyzw(np.column_stack((x_axis, y_axis, z_axis)))


def point_clearance(point, proxy):
    point = np.asarray(point, dtype=float)
    local = _quaternion_matrix_xyzw(proxy.orientation_xyzw).T @ (
        point - proxy.position
    )
    if proxy.shape == SHAPE_SPHERE:
        return float(np.linalg.norm(local) - proxy.dimensions[0] - proxy.safety_margin)
    if proxy.shape == SHAPE_BOX:
        half = 0.5 * proxy.dimensions + proxy.safety_margin
        outside = np.maximum(np.abs(local) - half, 0.0)
        if np.any(outside > 0.0):
            return float(np.linalg.norm(outside))
        return -float(np.min(half - np.abs(local)))
    if proxy.shape == SHAPE_CAPSULE:
        radius = float(proxy.dimensions[0] + proxy.safety_margin)
        half_segment = max(0.0, 0.5 * float(proxy.dimensions[1]))
        closest_z = np.clip(local[2], -half_segment, half_segment)
        return float(np.linalg.norm(local - np.array([0.0, 0.0, closest_z])) - radius)
    raise ValueError(f"지원하지 않는 proxy shape입니다: {proxy.shape}")


def _segment_samples(points):
    samples = []
    for start, end in zip(points[:-1], points[1:]):
        start = np.asarray(start, dtype=float)
        end = np.asarray(end, dtype=float)
        distance = float(np.linalg.norm(end - start))
        count = max(2, int(np.ceil(distance / SAMPLE_SPACING_M)) + 1)
        samples.extend(start + alpha * (end - start) for alpha in np.linspace(0.0, 1.0, count))
    return samples


def route_clearance(points, proxies):
    samples = _segment_samples(points)
    if not samples or not proxies:
        return float("inf"), "none"
    best = (float("inf"), "none")
    for point in samples:
        for proxy in proxies:
            clearance = point_clearance(point, proxy)
            if clearance < best[0]:
                best = (clearance, proxy.obstacle_id)
    return best


def _proxy_world_bounds(proxy):
    margin = float(proxy.safety_margin)
    if proxy.shape == SHAPE_SPHERE:
        radius = float(proxy.dimensions[0]) + margin
        return proxy.position - radius, proxy.position + radius
    if proxy.shape == SHAPE_BOX:
        rotation = np.abs(_quaternion_matrix_xyzw(proxy.orientation_xyzw))
        half = rotation @ (0.5 * proxy.dimensions + margin)
        return proxy.position - half, proxy.position + half
    radius = float(proxy.dimensions[0]) + margin
    half_local = np.array([radius, radius, radius + 0.5 * proxy.dimensions[1]])
    half = np.abs(_quaternion_matrix_xyzw(proxy.orientation_xyzw)) @ half_local
    return proxy.position - half, proxy.position + half


def plan_approach_route(start_tcp, robot_position, apple_position, proxies):
    """direct 또는 나무 바깥 우회 경로를 만들고 마지막 pose를 pregrasp로 둔다."""
    start_tcp = np.asarray(start_tcp, dtype=float)
    robot_position = np.asarray(robot_position, dtype=float)
    apple_position = np.asarray(apple_position, dtype=float)
    for name, value in (
        ("start_tcp", start_tcp),
        ("robot_position", robot_position),
        ("apple_position", apple_position),
    ):
        if value.shape != (3,) or not np.all(np.isfinite(value)):
            raise RoutePlanningError(f"{name} 좌표가 유효하지 않습니다.")
    proxies = tuple(proxies)
    orientation = approach_orientation_xyzw(robot_position, apple_position)
    staging = apple_position - np.array([0.0, 0.0, STAGING_DISTANCE_M])
    pregrasp = apple_position - np.array([0.0, 0.0, PREGRASP_DISTANCE_M])

    direct = [start_tcp, staging, pregrasp]
    clearance, obstacle = route_clearance(direct, proxies)
    if clearance >= 0.0:
        return PlannedRoute(
            "direct", tuple(np.asarray(p, dtype=float) for p in direct[1:]), orientation, clearance, obstacle
        )
    if not proxies:
        raise RoutePlanningError("planning scene에 obstacle proxy가 없습니다.")

    bounds = [_proxy_world_bounds(proxy) for proxy in proxies]
    minimum = np.min(np.asarray([item[0] for item in bounds]), axis=0)
    maximum = np.max(np.asarray([item[1] for item in bounds]), axis=0)
    center = 0.5 * (minimum + maximum)
    outward = start_tcp - center
    outward[2] = 0.0
    if np.linalg.norm(outward) <= 1e-9:
        outward = robot_position - center
        outward[2] = 0.0
    if np.linalg.norm(outward) <= 1e-9:
        outward = np.array([1.0, 0.0, 0.0])
    outward /= np.linalg.norm(outward)
    lateral = np.array([-outward[1], outward[0], 0.0])
    corners = np.array(
        [[x, y] for x in (minimum[0], maximum[0]) for y in (minimum[1], maximum[1])]
    )
    radial_extent = float(np.max((corners - center[:2]) @ outward[:2]))
    outside = center + outward * (radial_extent + OUTSIDE_OFFSET_M)
    outside[2] = staging[2]

    definitions = [("outside", 0.0, 0.0)]
    for multiplier in (1.0, 2.0, 3.0):
        definitions.extend(
            [
                (f"outside +side x{multiplier:.0f}", 0.0, SIDE_OFFSET_M * multiplier),
                (f"outside -side x{multiplier:.0f}", 0.0, -SIDE_OFFSET_M * multiplier),
            ]
        )
    definitions.append(("outside extra", SIDE_OFFSET_M, 0.0))
    attempted = []
    for name, outward_offset, lateral_offset in definitions:
        low = outside + outward * outward_offset + lateral * lateral_offset
        high = low.copy()
        high[2] += STAGING_DISTANCE_M
        near_staging = staging + lateral * lateral_offset
        points = [start_tcp, high, low]
        if abs(lateral_offset) > 1e-9:
            points.append(near_staging)
        points.extend([staging, pregrasp])
        clearance, obstacle = route_clearance(points, proxies)
        attempted.append(f"{name}={clearance:.3f}m/{obstacle}")
        if clearance >= 0.0:
            return PlannedRoute(
                name,
                tuple(np.asarray(p, dtype=float) for p in points[1:]),
                orientation,
                clearance,
                obstacle,
            )
    raise RoutePlanningError("모든 APPROACH 후보가 충돌합니다: " + ", ".join(attempted))
