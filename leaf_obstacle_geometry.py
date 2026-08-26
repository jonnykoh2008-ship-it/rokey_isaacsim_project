"""Pure geometry helpers for Personal PC 1 leaf-obstacle perception.

The functions in this module do not depend on ROS 2.  They validate aligned
RGB-D inputs, create a parameter-driven HSV leaf mask, deproject valid depth
pixels, transform points into a target frame, and reduce the result to stable
voxel-based sphere proxies.

Project-specific thresholds are intentionally not defined here.  HSV bounds,
depth limits, voxel size, proxy radius, and safety margin must be supplied by
the caller after they are approved for the active simulation test.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Optional, Sequence

import cv2
import numpy as np


@dataclass(frozen=True)
class CameraIntrinsics:
    """Pinhole intrinsics for an RGB-aligned depth image."""

    fx: float
    fy: float
    cx: float
    cy: float

    def __post_init__(self) -> None:
        values = np.asarray([self.fx, self.fy, self.cx, self.cy], dtype=float)
        if not np.all(np.isfinite(values)):
            raise ValueError("camera intrinsics must be finite")
        if self.fx <= 0.0 or self.fy <= 0.0:
            raise ValueError("camera focal lengths must be greater than zero")

    @classmethod
    def from_camera_matrix(cls, values: Sequence[float]) -> "CameraIntrinsics":
        """Create intrinsics from the row-major nine-element CameraInfo.k."""

        matrix = np.asarray(values, dtype=float)
        if matrix.shape != (9,):
            raise ValueError("CameraInfo.k must contain exactly nine values")
        return cls(
            fx=float(matrix[0]),
            fy=float(matrix[4]),
            cx=float(matrix[2]),
            cy=float(matrix[5]),
        )


@dataclass(frozen=True)
class MaskedPointCloud:
    """Valid camera-frame points and quality counts for one leaf mask."""

    points_camera: np.ndarray
    pixels_uv: np.ndarray
    mask_pixel_count: int
    valid_depth_pixel_count: int

    @property
    def valid_depth_ratio(self) -> float:
        if self.mask_pixel_count == 0:
            return 0.0
        return self.valid_depth_pixel_count / self.mask_pixel_count


@dataclass(frozen=True)
class LeafVoxel:
    """One deterministic world-frame voxel occupied by detected leaf points."""

    obstacle_id: str
    index_xyz: tuple[int, int, int]
    center_world: np.ndarray
    point_count: int


@dataclass(frozen=True)
class LeafSphereProxy:
    """ROS-independent sphere proxy ready for message conversion by a node."""

    obstacle_id: str
    center_world: np.ndarray
    radius_m: float
    safety_margin_m: float
    point_count: int


def validate_aligned_rgbd(bgr_image: np.ndarray, depth_image: np.ndarray) -> tuple[int, int]:
    """Validate RGB/depth array layout and return ``(height, width)``.

    Resizing is deliberately not performed.  A caller must provide calibrated,
    RGB-aligned depth rather than silently mixing unrelated pixel coordinates.
    """

    bgr = np.asarray(bgr_image)
    depth = np.asarray(depth_image)
    if bgr.ndim != 3 or bgr.shape[2] != 3:
        raise ValueError("BGR image must have shape (height, width, 3)")
    if depth.ndim != 2:
        raise ValueError("depth image must have shape (height, width)")
    if bgr.shape[:2] != depth.shape:
        raise ValueError(
            "RGB and depth resolutions do not match: "
            f"RGB={bgr.shape[:2]}, depth={depth.shape}"
        )
    if bgr.shape[0] == 0 or bgr.shape[1] == 0:
        raise ValueError("RGB-D images must not be empty")
    return int(bgr.shape[0]), int(bgr.shape[1])


def depth_to_meters(depth_image: np.ndarray, encoding: str) -> np.ndarray:
    """Normalize supported ROS depth encodings to float32 metres."""

    depth = np.asarray(depth_image)
    normalized_encoding = str(encoding).strip().upper()
    if normalized_encoding == "16UC1":
        if depth.dtype != np.uint16:
            raise ValueError("16UC1 depth must use numpy.uint16 storage")
        return depth.astype(np.float32) * 0.001
    if normalized_encoding == "32FC1":
        if not np.issubdtype(depth.dtype, np.floating):
            raise ValueError("32FC1 depth must use floating-point storage")
        return depth.astype(np.float32, copy=True)
    raise ValueError(f"unsupported depth encoding: {encoding!r}")


def _validate_hsv_triplet(name: str, values: Sequence[int]) -> np.ndarray:
    result = np.asarray(values, dtype=int)
    if result.shape != (3,):
        raise ValueError(f"{name} must contain H, S, and V")
    if not 0 <= result[0] <= 179:
        raise ValueError(f"{name} hue must be in the OpenCV range 0..179")
    if np.any(result[1:] < 0) or np.any(result[1:] > 255):
        raise ValueError(f"{name} saturation/value must be in 0..255")
    return result.astype(np.uint8)


def create_leaf_mask(
    bgr_image: np.ndarray,
    *,
    hsv_lower: Sequence[int],
    hsv_upper: Sequence[int],
    minimum_component_area_px: int,
    morphology_kernel_size: int,
    exclusion_mask: Optional[np.ndarray] = None,
) -> np.ndarray:
    """Return a uint8 leaf mask using caller-approved HSV parameters.

    Only non-wrapping HSV intervals are supported because the initial leaf
    colour range is expected to be green.  Red apple exclusion can be supplied
    through ``exclusion_mask`` by the ROS node or another perception stage.
    """

    bgr = np.asarray(bgr_image)
    if bgr.ndim != 3 or bgr.shape[2] != 3 or bgr.shape[:2] == (0, 0):
        raise ValueError("BGR image must have non-empty shape (height, width, 3)")
    if bgr.dtype != np.uint8:
        raise ValueError("BGR image must use numpy.uint8 storage")

    lower = _validate_hsv_triplet("hsv_lower", hsv_lower)
    upper = _validate_hsv_triplet("hsv_upper", hsv_upper)
    if np.any(lower.astype(int) > upper.astype(int)):
        raise ValueError("hsv_lower must not exceed hsv_upper")
    if int(minimum_component_area_px) != minimum_component_area_px:
        raise ValueError("minimum_component_area_px must be an integer")
    minimum_area = int(minimum_component_area_px)
    if minimum_area <= 0:
        raise ValueError("minimum_component_area_px must be greater than zero")
    if int(morphology_kernel_size) != morphology_kernel_size:
        raise ValueError("morphology_kernel_size must be an integer")
    kernel_size = int(morphology_kernel_size)
    if kernel_size <= 0 or kernel_size % 2 == 0:
        raise ValueError("morphology_kernel_size must be a positive odd integer")

    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    if exclusion_mask is not None:
        exclusion = np.asarray(exclusion_mask)
        if exclusion.shape != mask.shape:
            raise ValueError("exclusion mask resolution must match the BGR image")
        mask[exclusion.astype(bool)] = 0

    if kernel_size > 1:
        kernel = np.ones((kernel_size, kernel_size), dtype=np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    component_count, labels, stats, _centroids = cv2.connectedComponentsWithStats(
        mask, connectivity=8
    )
    filtered = np.zeros_like(mask)
    for label in range(1, component_count):
        area = int(stats[label, cv2.CC_STAT_AREA])
        if area >= minimum_area:
            filtered[labels == label] = 255
    return filtered


def deproject_pixels(
    pixels_uv: np.ndarray,
    depths_m: np.ndarray,
    intrinsics: CameraIntrinsics,
) -> np.ndarray:
    """Deproject matching ``(u, v)`` pixels and Z-depths into camera points."""

    pixels = np.asarray(pixels_uv, dtype=float)
    depths = np.asarray(depths_m, dtype=float)
    if pixels.ndim != 2 or pixels.shape[1] != 2:
        raise ValueError("pixels_uv must have shape (N, 2)")
    if depths.shape != (pixels.shape[0],):
        raise ValueError("depths_m must contain one value for every pixel")
    if not np.all(np.isfinite(pixels)) or not np.all(np.isfinite(depths)):
        raise ValueError("pixels and depths must be finite")
    if np.any(depths <= 0.0):
        raise ValueError("depths must be greater than zero")

    u = pixels[:, 0]
    v = pixels[:, 1]
    points = np.empty((pixels.shape[0], 3), dtype=float)
    points[:, 0] = (u - intrinsics.cx) * depths / intrinsics.fx
    points[:, 1] = (v - intrinsics.cy) * depths / intrinsics.fy
    points[:, 2] = depths
    return points


def masked_depth_to_points(
    leaf_mask: np.ndarray,
    depth_m: np.ndarray,
    intrinsics: CameraIntrinsics,
    *,
    minimum_depth_m: float,
    maximum_depth_m: float,
    pixel_stride: int,
) -> MaskedPointCloud:
    """Convert valid masked depth pixels into camera-frame points."""

    mask = np.asarray(leaf_mask)
    depth = np.asarray(depth_m, dtype=float)
    if mask.ndim != 2 or depth.ndim != 2 or mask.shape != depth.shape:
        raise ValueError("leaf mask and depth must have the same 2D resolution")
    if not math.isfinite(minimum_depth_m) or not math.isfinite(maximum_depth_m):
        raise ValueError("depth limits must be finite")
    if minimum_depth_m <= 0.0 or maximum_depth_m <= minimum_depth_m:
        raise ValueError("depth limits must satisfy 0 < minimum < maximum")
    if int(pixel_stride) != pixel_stride or int(pixel_stride) <= 0:
        raise ValueError("pixel_stride must be a positive integer")
    stride = int(pixel_stride)

    mask_bool = mask.astype(bool)
    valid = (
        mask_bool
        & np.isfinite(depth)
        & (depth >= minimum_depth_m)
        & (depth <= maximum_depth_m)
    )
    mask_pixel_count = int(np.count_nonzero(mask_bool))
    valid_depth_pixel_count = int(np.count_nonzero(valid))

    rows, columns = np.nonzero(valid)
    if stride > 1 and rows.size:
        keep = (rows % stride == 0) & (columns % stride == 0)
        rows = rows[keep]
        columns = columns[keep]
    pixels = np.column_stack((columns, rows)).astype(float, copy=False)
    if rows.size:
        points = deproject_pixels(pixels, depth[rows, columns], intrinsics)
    else:
        points = np.empty((0, 3), dtype=float)
    return MaskedPointCloud(
        points_camera=points,
        pixels_uv=pixels,
        mask_pixel_count=mask_pixel_count,
        valid_depth_pixel_count=valid_depth_pixel_count,
    )


def transform_points(
    points: np.ndarray,
    translation_xyz: Sequence[float],
    quaternion_xyzw: Sequence[float],
) -> np.ndarray:
    """Apply a normalized rigid transform to an ``(N, 3)`` point array."""

    source = np.asarray(points, dtype=float)
    translation = np.asarray(translation_xyz, dtype=float)
    quaternion = np.asarray(quaternion_xyzw, dtype=float)
    if source.ndim != 2 or source.shape[1] != 3:
        raise ValueError("points must have shape (N, 3)")
    if translation.shape != (3,) or not np.all(np.isfinite(translation)):
        raise ValueError("translation must contain three finite values")
    if quaternion.shape != (4,) or not np.all(np.isfinite(quaternion)):
        raise ValueError("quaternion must contain four finite xyzw values")
    if not np.all(np.isfinite(source)):
        raise ValueError("points must be finite")
    norm = float(np.linalg.norm(quaternion))
    if norm <= 1e-12:
        raise ValueError("quaternion norm must be greater than zero")
    x, y, z, w = quaternion / norm
    rotation = np.array(
        [
            [1.0 - 2.0 * (y * y + z * z), 2.0 * (x * y - z * w), 2.0 * (x * z + y * w)],
            [2.0 * (x * y + z * w), 1.0 - 2.0 * (x * x + z * z), 2.0 * (y * z - x * w)],
            [2.0 * (x * z - y * w), 2.0 * (y * z + x * w), 1.0 - 2.0 * (x * x + y * y)],
        ],
        dtype=float,
    )
    return source @ rotation.T + translation


def voxelize_world_points(points_world: np.ndarray, voxel_size_m: float) -> tuple[LeafVoxel, ...]:
    """Reduce world points to deterministic voxels with stable IDs."""

    points = np.asarray(points_world, dtype=float)
    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError("points_world must have shape (N, 3)")
    if not np.all(np.isfinite(points)):
        raise ValueError("points_world must be finite")
    if not math.isfinite(voxel_size_m) or voxel_size_m <= 0.0:
        raise ValueError("voxel_size_m must be a finite positive value")
    if points.shape[0] == 0:
        return ()

    indices = np.floor(points / voxel_size_m).astype(np.int64)
    unique_indices, inverse = np.unique(indices, axis=0, return_inverse=True)
    sums = np.zeros((unique_indices.shape[0], 3), dtype=float)
    counts = np.zeros(unique_indices.shape[0], dtype=np.int64)
    np.add.at(sums, inverse, points)
    np.add.at(counts, inverse, 1)
    centers = sums / counts[:, None]

    voxels = []
    for index, center, count in zip(unique_indices, centers, counts):
        index_tuple = tuple(int(value) for value in index)
        obstacle_id = "leaf_voxel_{}_{}_{}".format(*index_tuple)
        voxels.append(
            LeafVoxel(
                obstacle_id=obstacle_id,
                index_xyz=index_tuple,
                center_world=center,
                point_count=int(count),
            )
        )
    return tuple(voxels)


def build_leaf_sphere_proxies(
    points_world: np.ndarray,
    *,
    voxel_size_m: float,
    proxy_radius_m: float,
    safety_margin_m: float,
    maximum_proxy_count: Optional[int],
) -> tuple[LeafSphereProxy, ...]:
    """Build a deterministic, optionally bounded set of sphere proxies."""

    if not math.isfinite(proxy_radius_m) or proxy_radius_m <= 0.0:
        raise ValueError("proxy_radius_m must be a finite positive value")
    if not math.isfinite(safety_margin_m) or safety_margin_m < 0.0:
        raise ValueError("safety_margin_m must be a finite non-negative value")
    if maximum_proxy_count is not None:
        if int(maximum_proxy_count) != maximum_proxy_count:
            raise ValueError("maximum_proxy_count must be an integer or None")
        if int(maximum_proxy_count) <= 0:
            raise ValueError("maximum_proxy_count must be greater than zero")

    voxels = list(voxelize_world_points(points_world, voxel_size_m))
    if maximum_proxy_count is not None and len(voxels) > maximum_proxy_count:
        voxels.sort(key=lambda item: (-item.point_count, item.obstacle_id))
        voxels = voxels[: int(maximum_proxy_count)]
        voxels.sort(key=lambda item: item.obstacle_id)

    return tuple(
        LeafSphereProxy(
            obstacle_id=voxel.obstacle_id,
            center_world=voxel.center_world,
            radius_m=float(proxy_radius_m),
            safety_margin_m=float(safety_margin_m),
            point_count=voxel.point_count,
        )
        for voxel in voxels
    )
