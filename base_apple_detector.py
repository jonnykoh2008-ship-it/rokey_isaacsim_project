"""base_rsd455 RGB-D 전체 영상에서 가장 가까운 빨간 사과를 검출한다.

이 파일은 Isaac Sim Python이 아니라 ROS 2 Jazzy가 설치된 시스템 환경에서
실행한다. 현재 단계의 HSV 검출은 RGB-D와 TF 파이프라인 검증용이며, 여러
품종과 조명 조건을 다룰 때는 검출기 부분을 학습 기반 segmentation으로
교체해야 한다.

구독 토픽:
    /base_camera/color/image_raw
    /base_camera/depth/image_raw
    /base_camera/camera_info
    /simulation/state
    /tf, /tf_static

발행 토픽:
    /harvest/detection_pose_camera  카메라 좌표의 검출 결과
    /harvest/target                 검증 메타데이터를 포함한 world 수확 목표
    /harvest/perception_status      target 생성 전후의 인식 상태
    /harvest/detection_debug        검출 윤곽과 좌표가 표시된 RGB 영상

실행 예시:
    source /opt/ros/jazzy/setup.bash
    ROS_DOMAIN_ID=102 python3 base_apple_detector.py

use_sim_time은 노드가 직접 강제하므로 별도 인자가 필요하지 않다.
"""

import math
import os
from typing import Optional, Tuple

# 퍼블리셔와 동일한 개별 테스트 Domain을 기본값으로 사용한다.
# 셸에서 ROS_DOMAIN_ID를 지정했다면 해당 값을 그대로 따른다.
os.environ.setdefault("ROS_DOMAIN_ID", "102")

import cv2
import numpy as np
import rclpy
from appleproj_interfaces.msg import (
    HarvestPerceptionStatus,
    HarvestTarget,
    SimulationState,
)
from cv_bridge import CvBridge
from geometry_msgs.msg import PoseStamped
from rclpy.duration import Duration
from rclpy.node import Node
from rclpy.parameter import Parameter
from rclpy.qos import (
    DurabilityPolicy,
    HistoryPolicy,
    QoSProfile,
    ReliabilityPolicy,
    qos_profile_sensor_data,
)
from rclpy.time import Time
from sensor_msgs.msg import CameraInfo, Image
from tf2_ros import Buffer, TransformException, TransformListener


RGB_TOPIC = "/base_camera/color/image_raw"
DEPTH_TOPIC = "/base_camera/depth/image_raw"
CAMERA_INFO_TOPIC = "/base_camera/camera_info"
CAMERA_POSE_TOPIC = "/harvest/detection_pose_camera"
SIMULATION_STATE_TOPIC = "/simulation/state"
TARGET_TOPIC = "/harvest/target"
PERCEPTION_STATUS_TOPIC = "/harvest/perception_status"
DEBUG_IMAGE_TOPIC = "/harvest/detection_debug"

TARGET_QOS = QoSProfile(
    history=HistoryPolicy.KEEP_LAST,
    depth=1,
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.VOLATILE,
)
STATUS_QOS = QoSProfile(
    history=HistoryPolicy.KEEP_LAST,
    depth=10,
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.VOLATILE,
)
SIMULATION_STATE_QOS = QoSProfile(
    history=HistoryPolicy.KEEP_LAST,
    depth=1,
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.TRANSIENT_LOCAL,
)


def stamp_to_nanoseconds(stamp) -> int:
    """ROS builtin_interfaces/Time을 비교 가능한 정수 나노초로 변환한다."""
    return int(stamp.sec) * 1_000_000_000 + int(stamp.nanosec)


def rotate_vector_by_quaternion(vector, quaternion):
    """[x, y, z, w] quaternion으로 3차원 벡터를 회전한다."""
    vector = np.asarray(vector, dtype=float)
    q_xyz = np.asarray(quaternion[:3], dtype=float)
    q_w = float(quaternion[3])
    twice_cross = 2.0 * np.cross(q_xyz, vector)
    return vector + q_w * twice_cross + np.cross(q_xyz, twice_cross)


class BaseAppleDetector(Node):
    """RGB, Depth, CameraInfo를 결합해 사과 중심 Pose를 계산하는 노드."""

    def __init__(self):
        # docs/architecture/ros2_interfaces.md는 모든 ROS 2 노드가
        # use_sim_time:=true를 쓰도록 규정한다. CLI 인자를 빠뜨리면 이 노드만
        # wall time으로 동작해 /clock 기준 timestamp 비교가 어긋나므로
        # 노드에서 직접 강제한다.
        super().__init__(
            "base_apple_detector",
            parameter_overrides=[Parameter("use_sim_time", value=True)],
        )

        # 현재 빨간 사과 에셋용 검출 파라미터다. ROS parameter로 노출하여
        # 코드를 수정하지 않고 환경별로 조절할 수 있다.
        self.declare_parameter("minimum_contour_area", 60.0)
        # 통합 시험 전 confidence threshold는 TBD다. 음수 sentinel은 필터를
        # 비활성화하며, 후보별 진단값을 확인한 뒤 실행 시 임시값을 주입한다.
        self.declare_parameter("minimum_contour_confidence", -1.0)
        self.declare_parameter("minimum_depth_m", 0.2)
        self.declare_parameter("maximum_depth_m", 10.0)
        self.declare_parameter("maximum_sync_error_sec", 0.08)
        self.declare_parameter("apple_radius_m", 0.04)
        # surface_point_to_center가 "가장 앞면 표면점"을 가정하므로 윤곽 내부
        # depth에서 앞면에 해당하는 낮은 분위를 사용한다. 0에 가까울수록
        # 기하학적으로 정확하지만 depth noise에 민감해진다.
        self.declare_parameter("depth_surface_percentile", 10.0)
        self.declare_parameter("target_frame", "world")
        # ID 생성 규칙은 아직 TBD이므로 실행 시 명시적으로 주입한다.
        # reset_id와 조합한 lifecycle 규약은 HarvestTarget 계약을 따른다.
        self.declare_parameter("target_id", "")
        self.declare_parameter("show_debug_window", True)

        self.minimum_contour_area = float(
            self.get_parameter("minimum_contour_area").value
        )
        minimum_contour_confidence = float(
            self.get_parameter("minimum_contour_confidence").value
        )
        if not math.isfinite(minimum_contour_confidence):
            raise ValueError(
                "minimum_contour_confidence는 유한값이어야 합니다: "
                f"{minimum_contour_confidence}"
            )
        if minimum_contour_confidence > 1.0:
            raise ValueError(
                "minimum_contour_confidence는 음수 sentinel 또는 0~1 "
                f"범위여야 합니다: {minimum_contour_confidence}"
            )
        self.minimum_contour_confidence = (
            None
            if minimum_contour_confidence < 0.0
            else minimum_contour_confidence
        )
        self.minimum_depth_m = float(
            self.get_parameter("minimum_depth_m").value
        )
        self.maximum_depth_m = float(
            self.get_parameter("maximum_depth_m").value
        )
        self.maximum_sync_error_ns = int(
            float(self.get_parameter("maximum_sync_error_sec").value) * 1e9
        )
        self.apple_radius_m = float(self.get_parameter("apple_radius_m").value)
        if not math.isfinite(self.apple_radius_m) or self.apple_radius_m < 0.0:
            raise ValueError(
                f"apple_radius_m은 0 이상의 유한값이어야 합니다: "
                f"{self.apple_radius_m}"
            )
        self.depth_surface_percentile = float(
            self.get_parameter("depth_surface_percentile").value
        )
        if not 0.0 <= self.depth_surface_percentile <= 100.0:
            raise ValueError(
                "depth_surface_percentile은 0~100 범위여야 합니다: "
                f"{self.depth_surface_percentile}"
            )
        self.target_frame = str(self.get_parameter("target_frame").value)
        if self.target_frame != "world":
            raise ValueError(
                "HarvestTarget 계약의 target_frame은 'world'여야 합니다: "
                f"{self.target_frame!r}"
            )
        self.target_id = str(self.get_parameter("target_id").value).strip()
        if not self.target_id:
            raise ValueError(
                "target_id 규칙은 아직 TBD입니다. 실행 시 ROS parameter로 "
                "명시해야 합니다. 예: --ros-args -p target_id:=<approved_id>"
            )
        self.show_debug_window = bool(
            self.get_parameter("show_debug_window").value
        )

        self.bridge = CvBridge()
        self.camera_info: Optional[CameraInfo] = None
        self.latest_rgb: Optional[Image] = None
        self.latest_depth: Optional[Image] = None
        self.last_processed_rgb_stamp = -1
        self.last_detection_log_ns = -1
        self.last_tf_warning_ns = -1
        self.last_status_code = None
        self.last_status_publish_ns = -1
        self.simulation_state: Optional[SimulationState] = None

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.create_subscription(
            CameraInfo,
            CAMERA_INFO_TOPIC,
            self.camera_info_callback,
            qos_profile_sensor_data,
        )
        self.create_subscription(
            Image, RGB_TOPIC, self.rgb_callback, qos_profile_sensor_data
        )
        self.create_subscription(
            Image, DEPTH_TOPIC, self.depth_callback, qos_profile_sensor_data
        )
        self.create_subscription(
            SimulationState,
            SIMULATION_STATE_TOPIC,
            self.simulation_state_callback,
            SIMULATION_STATE_QOS,
        )

        self.camera_pose_publisher = self.create_publisher(
            PoseStamped, CAMERA_POSE_TOPIC, 10
        )
        self.target_publisher = self.create_publisher(
            HarvestTarget, TARGET_TOPIC, TARGET_QOS
        )
        self.perception_status_publisher = self.create_publisher(
            HarvestPerceptionStatus, PERCEPTION_STATUS_TOPIC, STATUS_QOS
        )
        self.debug_image_publisher = self.create_publisher(
            Image, DEBUG_IMAGE_TOPIC, qos_profile_sensor_data
        )

        self.get_logger().info("base_rsd455 RGB-D 사과 검출 노드 시작")
        self.get_logger().info(f"RGB: {RGB_TOPIC}")
        self.get_logger().info(f"Depth: {DEPTH_TOPIC}")
        self.get_logger().info(f"CameraInfo: {CAMERA_INFO_TOPIC}")
        self.get_logger().info(f"Target: {TARGET_TOPIC} (target_id={self.target_id})")

    def simulation_state_callback(self, message: SimulationState):
        """최신 Timeline 상태를 보관하고 reset 세대가 바뀌면 입력 캐시를 버린다."""
        previous_reset_id = (
            self.simulation_state.reset_id if self.simulation_state is not None else None
        )
        self.simulation_state = message
        if previous_reset_id is not None and previous_reset_id != message.reset_id:
            self.latest_rgb = None
            self.latest_depth = None
            self.last_processed_rgb_stamp = -1
            self.get_logger().info(
                f"simulation reset_id 변경: {previous_reset_id} -> "
                f"{message.reset_id}; RGB-D 캐시 폐기"
            )

    def camera_info_callback(self, message: CameraInfo):
        """카메라 내부 파라미터 fx, fy, cx, cy가 포함된 메시지를 보관한다."""
        self.camera_info = message

    def rgb_callback(self, message: Image):
        self.latest_rgb = message
        self.try_process_pair()

    def depth_callback(self, message: Image):
        self.latest_depth = message
        self.try_process_pair()

    def try_process_pair(self):
        """시간이 가까운 RGB와 Depth가 모였을 때 한 번만 처리한다."""
        if (
            self.camera_info is None
            or self.latest_rgb is None
            or self.latest_depth is None
        ):
            return

        rgb_stamp = stamp_to_nanoseconds(self.latest_rgb.header.stamp)
        depth_stamp = stamp_to_nanoseconds(self.latest_depth.header.stamp)
        if rgb_stamp == self.last_processed_rgb_stamp:
            return
        if abs(rgb_stamp - depth_stamp) > self.maximum_sync_error_ns:
            self.publish_perception_status(
                self.latest_rgb,
                HarvestPerceptionStatus.INPUT_NOT_SYNCHRONIZED,
                message=(
                    f"RGB/depth timestamp 차이 "
                    f"{abs(rgb_stamp - depth_stamp) / 1e9:.6f}s"
                ),
            )
            return

        self.last_processed_rgb_stamp = rgb_stamp
        try:
            self.process_rgbd(self.latest_rgb, self.latest_depth, self.camera_info)
        except Exception as error:  # 콜백 예외로 노드가 종료되는 것을 방지한다.
            self.get_logger().error(f"RGB-D 처리 실패: {error}")
            self.publish_perception_status(
                self.latest_rgb,
                HarvestPerceptionStatus.INTERNAL_ERROR,
                message=str(error),
            )

    @staticmethod
    def red_mask(bgr_image):
        """현재 빨간 사과 에셋을 위한 HSV 이중 구간 mask를 생성한다."""
        hsv = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
        lower_red = cv2.inRange(hsv, (0, 90, 60), (12, 255, 255))
        upper_red = cv2.inRange(hsv, (168, 90, 60), (179, 255, 255))
        mask = cv2.bitwise_or(lower_red, upper_red)
        kernel = np.ones((3, 3), dtype=np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        return cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    def find_apple_contours(self, bgr_image):
        """전체 화각에서 최소 면적을 만족하는 모든 빨간 사과 후보를 찾는다."""
        mask = self.red_mask(bgr_image)
        contours, _hierarchy = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        candidates = [
            contour
            for contour in contours
            if cv2.contourArea(contour) >= self.minimum_contour_area
        ]
        return candidates, mask

    def depth_in_meters(self, depth_message: Image):
        """Isaac/ROS depth encoding을 meter 단위 float 배열로 통일한다."""
        depth = self.bridge.imgmsg_to_cv2(depth_message, desired_encoding="passthrough")
        encoding = depth_message.encoding.upper()
        if encoding == "16UC1" or depth.dtype == np.uint16:
            return depth.astype(np.float32) / 1000.0
        return depth.astype(np.float32)

    def robust_depth(self, contour, depth_m):
        """윤곽 내부에서 사과의 '카메라를 향한 앞면' depth를 추정한다.

        중앙값을 쓰면 구 표면 전체의 평균적 깊이(중심에서 약 0.71r 앞)가
        나오는데, surface_point_to_center는 여기에 반지름 전체를 더하므로
        추정 중심이 시선 방향으로 약 0.29r(사과 기준 약 12 mm) 밀린다.
        앞면에 해당하는 낮은 분위를 사용해 두 단계의 가정을 일치시킨다.
        순수 최솟값은 depth noise와 배경 픽셀에 취약하므로 분위를 쓴다.
        """
        contour_mask = np.zeros(depth_m.shape[:2], dtype=np.uint8)
        cv2.drawContours(contour_mask, [contour], -1, 255, thickness=cv2.FILLED)

        eroded = cv2.erode(contour_mask, np.ones((3, 3), np.uint8), iterations=1)
        if cv2.countNonZero(eroded) >= 9:
            contour_mask = eroded

        valid = (
            (contour_mask > 0)
            & np.isfinite(depth_m)
            & (depth_m >= self.minimum_depth_m)
            & (depth_m <= self.maximum_depth_m)
        )
        mask_pixels = int(np.count_nonzero(contour_mask))
        valid_pixels = int(np.count_nonzero(valid))
        valid_depth_ratio = valid_pixels / mask_pixels if mask_pixels else 0.0
        values = depth_m[valid]
        if values.size < 5:
            return None
        return (
            float(np.percentile(values, self.depth_surface_percentile)),
            float(valid_depth_ratio),
        )

    @staticmethod
    def contour_shape_metrics(contour):
        """HSV 후보의 면적·원형도·solidity·비보정 confidence를 반환한다."""
        area = float(cv2.contourArea(contour))
        perimeter = float(cv2.arcLength(contour, closed=True))
        hull_area = float(cv2.contourArea(cv2.convexHull(contour)))
        if area <= 0.0 or perimeter <= 0.0 or hull_area <= 0.0:
            return area, 0.0, 0.0, 0.0
        circularity = min(1.0, max(0.0, 4.0 * math.pi * area / perimeter**2))
        solidity = min(1.0, max(0.0, area / hull_area))
        confidence = float(math.sqrt(circularity * solidity))
        return area, circularity, solidity, confidence

    @classmethod
    def contour_confidence(cls, contour) -> float:
        """HSV 후보의 원형도와 solidity를 0~1 비보정 점수로 변환한다."""
        return cls.contour_shape_metrics(contour)[3]

    @staticmethod
    def draw_candidate_diagnostics(image, diagnostics):
        """검출된 모든 HSV 후보의 형상·depth·선택 상태를 영상에 표시한다."""
        height, width = image.shape[:2]
        font = cv2.FONT_HERSHEY_SIMPLEX
        for diagnostic in diagnostics:
            if diagnostic["selected"]:
                color = (0, 255, 0)
                state = "SELECTED"
            elif diagnostic["reason"] == "low_confidence":
                color = (0, 0, 255)
                state = "LOW_CONF"
            elif diagnostic["reason"] == "accepted":
                color = (0, 255, 255)
                state = "VALID"
            else:
                color = (0, 165, 255)
                state = "DEPTH_INVALID"

            contour = diagnostic["contour"]
            cv2.drawContours(image, [contour], -1, color, 2)
            center = diagnostic["center"]
            if center is None:
                x, y, box_width, box_height = cv2.boundingRect(contour)
                center = (x + 0.5 * box_width, y + 0.5 * box_height)

            distance = diagnostic["distance"]
            depth_text = "invalid" if distance is None else f"{distance:.2f}m"
            label = (
                f"#{diagnostic['index']} {state} "
                f"A={diagnostic['area']:.0f} "
                f"C={diagnostic['confidence']:.2f} "
                f"Ci={diagnostic['circularity']:.2f} "
                f"S={diagnostic['solidity']:.2f} D={depth_text}"
            )
            (text_width, text_height), baseline = cv2.getTextSize(
                label, font, 0.42, 1
            )
            label_x = max(
                0,
                min(width - text_width - 2, round(center[0]) - text_width // 2),
            )
            label_y = max(
                text_height + baseline,
                min(height - baseline - 1, round(center[1]) - 12),
            )
            cv2.putText(
                image,
                label,
                (label_x, label_y),
                font,
                0.42,
                color,
                1,
                cv2.LINE_AA,
            )

    @staticmethod
    def contour_center(contour) -> Optional[Tuple[float, float]]:
        moments = cv2.moments(contour)
        if math.isclose(moments["m00"], 0.0):
            return None
        return (
            float(moments["m10"] / moments["m00"]),
            float(moments["m01"] / moments["m00"]),
        )

    @staticmethod
    def deproject(u, v, depth_m, camera_info):
        """핀홀 카메라 모델로 픽셀과 depth를 optical-frame 3D로 바꾼다."""
        fx = float(camera_info.k[0])
        fy = float(camera_info.k[4])
        cx = float(camera_info.k[2])
        cy = float(camera_info.k[5])
        if fx <= 0.0 or fy <= 0.0:
            raise ValueError("CameraInfo의 focal length가 유효하지 않습니다.")
        return np.array(
            [
                (u - cx) * depth_m / fx,
                (v - cy) * depth_m / fy,
                depth_m,
            ],
            dtype=float,
        )

    @staticmethod
    def surface_point_to_center(surface_point, apple_radius_m):
        """카메라에 보이는 사과 표면점을 구의 중심점으로 보정한다."""
        surface_point = np.asarray(surface_point, dtype=float)
        ray_length = float(np.linalg.norm(surface_point))
        if ray_length <= 1e-9 or not np.isfinite(ray_length):
            raise ValueError(f"사과 표면점이 유효하지 않습니다: {surface_point}")
        return surface_point + surface_point / ray_length * apple_radius_m

    def make_camera_pose(self, rgb_message, point_camera):
        pose = PoseStamped()
        pose.header = rgb_message.header
        if not pose.header.frame_id:
            pose.header.frame_id = "base_camera"
        pose.pose.position.x = float(point_camera[0])
        pose.pose.position.y = float(point_camera[1])
        pose.pose.position.z = float(point_camera[2])
        pose.pose.orientation.w = 1.0
        return pose

    def transform_to_world(self, camera_pose):
        """동일 시각의 TF를 사용하여 카메라 3D 점을 world 좌표로 변환한다."""
        try:
            transform = self.tf_buffer.lookup_transform(
                self.target_frame,
                camera_pose.header.frame_id,
                Time.from_msg(camera_pose.header.stamp),
                timeout=Duration(seconds=0.05),
            )
        except TransformException as error:
            now_ns = self.get_clock().now().nanoseconds
            if (
                self.last_tf_warning_ns < 0
                or now_ns - self.last_tf_warning_ns >= 5_000_000_000
            ):
                self.get_logger().warning(
                    f"{camera_pose.header.frame_id} -> {self.target_frame} "
                    f"TF 대기 중: {error}"
                )
                self.last_tf_warning_ns = now_ns
            return None, math.nan

        translation = transform.transform.translation
        rotation = transform.transform.rotation
        quaternion = np.array(
            [rotation.x, rotation.y, rotation.z, rotation.w], dtype=float
        )
        quaternion_norm = np.linalg.norm(quaternion)
        if quaternion_norm <= 1e-9:
            return None, math.nan
        quaternion /= quaternion_norm

        camera_point = np.array(
            [
                camera_pose.pose.position.x,
                camera_pose.pose.position.y,
                camera_pose.pose.position.z,
            ],
            dtype=float,
        )
        world_point = rotate_vector_by_quaternion(camera_point, quaternion)
        world_point += np.array(
            [translation.x, translation.y, translation.z], dtype=float
        )

        result = PoseStamped()
        result.header.stamp = camera_pose.header.stamp
        result.header.frame_id = self.target_frame
        result.pose.position.x = float(world_point[0])
        result.pose.position.y = float(world_point[1])
        result.pose.position.z = float(world_point[2])
        # PoseStamped는 로컬 camera debug 호환용이다. HarvestTarget에는
        # orientation을 싣지 않으며 GPU PC 1이 접근 자세를 결정한다.
        result.pose.orientation.w = 1.0
        transform_stamp_ns = stamp_to_nanoseconds(transform.header.stamp)
        camera_stamp_ns = stamp_to_nanoseconds(camera_pose.header.stamp)
        # /tf_static은 stamp=0으로 저장되며 모든 simulation time에 유효하다.
        tf_time_error_sec = (
            0.0
            if transform_stamp_ns == 0
            else abs(camera_stamp_ns - transform_stamp_ns) / 1e9
        )
        return result, float(tf_time_error_sec)

    def target_publication_allowed(self) -> bool:
        return self.simulation_state is not None and self.simulation_state.state in {
            SimulationState.READY,
            SimulationState.PLAYING,
        }

    def publish_perception_status(
        self,
        source_message,
        status,
        *,
        target_id="",
        confidence=math.nan,
        valid_depth_ratio=math.nan,
        tf_time_error_sec=math.nan,
        message="",
    ):
        """같은 상태를 최대 1Hz로 제한해 Reliable 상태 토픽에 발행한다."""
        now_ns = self.get_clock().now().nanoseconds
        if (
            status == self.last_status_code
            and self.last_status_publish_ns >= 0
            and now_ns - self.last_status_publish_ns < 1_000_000_000
        ):
            return

        result = HarvestPerceptionStatus()
        result.header = source_message.header
        result.status = int(status)
        result.target_id = target_id
        if self.simulation_state is not None:
            result.reset_id = self.simulation_state.reset_id
            result.scene_version = self.simulation_state.scene_version
        result.confidence = float(confidence)
        result.valid_depth_ratio = float(valid_depth_ratio)
        result.tf_time_error_sec = float(tf_time_error_sec)
        result.message = message
        self.perception_status_publisher.publish(result)
        self.last_status_code = int(status)
        self.last_status_publish_ns = now_ns

    def publish_harvest_target(
        self,
        rgb_message,
        camera_pose,
        world_pose,
        confidence,
        valid_depth_ratio,
        tf_time_error_sec,
    ):
        """문서 계약을 모두 채운 유효 target과 OK 상태를 발행한다."""
        if not self.target_publication_allowed():
            state_name = (
                "UNAVAILABLE"
                if self.simulation_state is None
                else str(self.simulation_state.state)
            )
            self.publish_perception_status(
                rgb_message,
                HarvestPerceptionStatus.SIMULATION_NOT_READY,
                confidence=confidence,
                valid_depth_ratio=valid_depth_ratio,
                tf_time_error_sec=tf_time_error_sec,
                message=f"SimulationState가 READY/PLAYING이 아님: {state_name}",
            )
            return

        target = HarvestTarget()
        target.header.stamp = rgb_message.header.stamp
        target.header.frame_id = "world"
        target.target_id = self.target_id
        target.reset_id = self.simulation_state.reset_id
        target.scene_version = self.simulation_state.scene_version
        target.position = world_pose.pose.position
        target.source_point.header = camera_pose.header
        target.source_point.point = camera_pose.pose.position
        target.confidence = float(confidence)
        target.valid_depth_ratio = float(valid_depth_ratio)
        target.tf_time_error_sec = float(tf_time_error_sec)
        self.target_publisher.publish(target)
        self.publish_perception_status(
            rgb_message,
            HarvestPerceptionStatus.OK,
            target_id=self.target_id,
            confidence=confidence,
            valid_depth_ratio=valid_depth_ratio,
            tf_time_error_sec=tf_time_error_sec,
            message="HarvestTarget 발행 완료",
        )

    def publish_debug_image(self, source_message, image):
        debug_message = self.bridge.cv2_to_imgmsg(image, encoding="bgr8")
        debug_message.header = source_message.header
        self.debug_image_publisher.publish(debug_message)

    def process_rgbd(self, rgb_message, depth_message, camera_info):
        """사과 검출부터 camera/world Pose 발행까지 한 프레임을 처리한다."""
        bgr = self.bridge.imgmsg_to_cv2(rgb_message, desired_encoding="bgr8")
        depth_m = self.depth_in_meters(depth_message)
        if bgr.shape[:2] != depth_m.shape[:2]:
            raise ValueError(
                f"RGB와 Depth 해상도가 다릅니다: {bgr.shape[:2]} / "
                f"{depth_m.shape[:2]}"
            )

        contours, _red_mask = self.find_apple_contours(bgr)
        annotated = bgr.copy()
        if not contours:
            self.publish_perception_status(
                rgb_message,
                HarvestPerceptionStatus.NO_DETECTION,
                message="HSV 조건을 만족하는 사과 후보 없음",
            )
            cv2.putText(
                annotated,
                "APPLE NOT FOUND",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 0, 255),
                2,
            )
            self.publish_debug_image(rgb_message, annotated)
            self.show_debug(annotated)
            return

        diagnostics = []
        valid_candidates = []
        low_confidence_candidates = []
        for candidate_index, contour in enumerate(contours, start=1):
            area, circularity, solidity, confidence = (
                self.contour_shape_metrics(contour)
            )
            center = self.contour_center(contour)
            depth_result = self.robust_depth(contour, depth_m)
            diagnostic = {
                "index": candidate_index,
                "contour": contour,
                "center": center,
                "area": area,
                "circularity": circularity,
                "solidity": solidity,
                "confidence": confidence,
                "distance": None,
                "reason": "depth_invalid",
                "selected": False,
            }
            diagnostics.append(diagnostic)
            if center is None or depth_result is None:
                continue

            depth_value, valid_depth_ratio = depth_result
            u, v = center
            surface_point = self.deproject(u, v, depth_value, camera_info)
            center_point = self.surface_point_to_center(
                surface_point,
                self.apple_radius_m,
            )
            distance = float(np.linalg.norm(center_point))
            if not math.isfinite(distance):
                continue
            diagnostic["distance"] = distance
            candidate = {
                "diagnostic": diagnostic,
                "contour": contour,
                "center": center,
                "surface_point": surface_point,
                "center_point": center_point,
                "distance": distance,
                "confidence": confidence,
                "valid_depth_ratio": valid_depth_ratio,
                "area": area,
                "circularity": circularity,
                "solidity": solidity,
            }
            if (
                self.minimum_contour_confidence is not None
                and confidence < self.minimum_contour_confidence
            ):
                diagnostic["reason"] = "low_confidence"
                low_confidence_candidates.append(candidate)
                continue
            diagnostic["reason"] = "accepted"
            valid_candidates.append(candidate)

        if not valid_candidates:
            self.draw_candidate_diagnostics(annotated, diagnostics)
            if low_confidence_candidates:
                best_confidence = max(
                    candidate["confidence"]
                    for candidate in low_confidence_candidates
                )
                threshold = self.minimum_contour_confidence
                self.publish_perception_status(
                    rgb_message,
                    HarvestPerceptionStatus.LOW_CONFIDENCE,
                    confidence=best_confidence,
                    message=(
                        "유효 depth 후보가 모두 confidence 기준 미달: "
                        f"best={best_confidence:.3f}, threshold={threshold:.3f}"
                    ),
                )
                failure_text = "NO APPLE ABOVE CONFIDENCE"
                failure_color = (0, 0, 255)
            else:
                self.publish_perception_status(
                    rgb_message,
                    HarvestPerceptionStatus.DEPTH_INVALID,
                    message="사과 후보에서 유효 depth 픽셀 5개 미만",
                )
                failure_text = "NO APPLE WITH VALID DEPTH"
                failure_color = (0, 165, 255)
            cv2.putText(
                annotated,
                failure_text,
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                failure_color,
                2,
            )
            self.publish_debug_image(rgb_message, annotated)
            self.show_debug(annotated)
            return

        # 전체 유효 후보 중 카메라 광학 중심과의 3D 직선거리가 가장 짧은
        # 사과를 이번 수확 목표로 선택한다.
        selected = min(
            valid_candidates, key=lambda candidate: candidate["distance"]
        )
        selected["diagnostic"]["selected"] = True
        contour = selected["contour"]
        center = selected["center"]
        surface_point_camera = selected["surface_point"]
        point_camera = selected["center_point"]
        selected_distance = selected["distance"]
        confidence = selected["confidence"]
        valid_depth_ratio = selected["valid_depth_ratio"]
        u, v = center
        camera_pose = self.make_camera_pose(rgb_message, point_camera)
        self.camera_pose_publisher.publish(camera_pose)

        world_pose, tf_time_error_sec = self.transform_to_world(camera_pose)
        if world_pose is not None:
            self.publish_harvest_target(
                rgb_message,
                camera_pose,
                world_pose,
                confidence,
                valid_depth_ratio,
                tf_time_error_sec,
            )
        else:
            self.publish_perception_status(
                rgb_message,
                HarvestPerceptionStatus.TF_UNAVAILABLE,
                confidence=confidence,
                valid_depth_ratio=valid_depth_ratio,
                message=f"{camera_pose.header.frame_id} -> world TF 변환 실패",
            )

        self.draw_candidate_diagnostics(annotated, diagnostics)
        cv2.circle(annotated, (round(u), round(v)), 5, (255, 0, 0), -1)
        text = (
            f"SELECTED {selected['diagnostic']['index']}/{len(diagnostics)} "
            f"distance={selected_distance:.3f}m "
            f"conf={confidence:.3f} depth={valid_depth_ratio:.3f} "
            f"xyz=({point_camera[0]:.3f}, {point_camera[1]:.3f}, "
            f"{point_camera[2]:.3f})"
        )
        cv2.putText(
            annotated,
            text,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (0, 255, 0),
            2,
        )
        self.publish_debug_image(rgb_message, annotated)
        self.show_debug(annotated)

        now_ns = self.get_clock().now().nanoseconds
        if (
            self.last_detection_log_ns < 0
            or now_ns - self.last_detection_log_ns >= 1_000_000_000
        ):
            message = (
                f"사과 후보 {len(valid_candidates)}개, 최근접 거리 "
                f"{selected_distance:.4f} m, surface camera xyz = "
                f"{surface_point_camera.round(4).tolist()} m, "
                f"center camera xyz = {point_camera.round(4).tolist()} m"
            )
            if world_pose is not None:
                position = world_pose.pose.position
                message += (
                    f", world xyz = "
                    f"[{position.x:.4f}, {position.y:.4f}, {position.z:.4f}] m"
                )
            self.get_logger().info(message)
            self.last_detection_log_ns = now_ns

    def show_debug(self, image):
        """GUI 사용 시 로컬 검출 화면을 표시한다."""
        if not self.show_debug_window:
            return
        try:
            cv2.imshow("base_rsd455 apple detection", image)
            cv2.waitKey(1)
        except cv2.error as error:
            self.get_logger().warning(f"OpenCV 창을 열 수 없습니다: {error}")
            self.show_debug_window = False

    def destroy_node(self):
        if self.show_debug_window:
            cv2.destroyAllWindows()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = BaseAppleDetector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
