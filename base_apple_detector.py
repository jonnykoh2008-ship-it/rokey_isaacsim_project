"""base_rsd455 RGB-D 영상에서 빨간 사과 한 개의 3D 중심을 검출한다.

이 파일은 Isaac Sim Python이 아니라 ROS 2 Jazzy가 설치된 시스템 환경에서
실행한다. 현재 단계의 HSV 검출은 RGB-D와 TF 파이프라인 검증용이며, 여러
품종과 조명 조건을 다룰 때는 검출기 부분을 학습 기반 segmentation으로
교체해야 한다.

구독 토픽:
    /base_camera/color/image_raw
    /base_camera/depth/image_raw
    /base_camera/camera_info
    /tf, /tf_static

발행 토픽:
    /harvest/detection_pose_camera  카메라 좌표의 검출 결과
    /harvest/target_pose            world 변환에 성공한 수확 목표
    /harvest/detection_debug        검출 윤곽과 좌표가 표시된 RGB 영상

실행 예시:
    source /opt/ros/jazzy/setup.bash
    ROS_DOMAIN_ID=102 python3 base_apple_detector.py \
        --ros-args -p use_sim_time:=true
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
from cv_bridge import CvBridge
from geometry_msgs.msg import PoseStamped
from rclpy.duration import Duration
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from rclpy.time import Time
from sensor_msgs.msg import CameraInfo, Image
from tf2_ros import Buffer, TransformException, TransformListener


RGB_TOPIC = "/base_camera/color/image_raw"
DEPTH_TOPIC = "/base_camera/depth/image_raw"
CAMERA_INFO_TOPIC = "/base_camera/camera_info"
CAMERA_POSE_TOPIC = "/harvest/detection_pose_camera"
TARGET_POSE_TOPIC = "/harvest/target_pose"
DEBUG_IMAGE_TOPIC = "/harvest/detection_debug"


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
        super().__init__("base_apple_detector")

        # 현재 빨간 사과 에셋용 검출 파라미터다. ROS parameter로 노출하여
        # 코드를 수정하지 않고 환경별로 조절할 수 있다.
        self.declare_parameter("minimum_contour_area", 60.0)
        self.declare_parameter("minimum_depth_m", 0.2)
        self.declare_parameter("maximum_depth_m", 10.0)
        self.declare_parameter("maximum_sync_error_sec", 0.08)
        self.declare_parameter("apple_radius_m", 0.04)
        self.declare_parameter("target_frame", "world")
        self.declare_parameter("show_debug_window", True)

        self.minimum_contour_area = float(
            self.get_parameter("minimum_contour_area").value
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
        self.target_frame = str(self.get_parameter("target_frame").value)
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

        self.camera_pose_publisher = self.create_publisher(
            PoseStamped, CAMERA_POSE_TOPIC, 10
        )
        self.target_pose_publisher = self.create_publisher(
            PoseStamped, TARGET_POSE_TOPIC, 10
        )
        self.debug_image_publisher = self.create_publisher(
            Image, DEBUG_IMAGE_TOPIC, qos_profile_sensor_data
        )

        self.get_logger().info("base_rsd455 RGB-D 사과 검출 노드 시작")
        self.get_logger().info(f"RGB: {RGB_TOPIC}")
        self.get_logger().info(f"Depth: {DEPTH_TOPIC}")
        self.get_logger().info(f"CameraInfo: {CAMERA_INFO_TOPIC}")

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
            return

        self.last_processed_rgb_stamp = rgb_stamp
        try:
            self.process_rgbd(self.latest_rgb, self.latest_depth, self.camera_info)
        except Exception as error:  # 콜백 예외로 노드가 종료되는 것을 방지한다.
            self.get_logger().error(f"RGB-D 처리 실패: {error}")

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

    def find_apple_contour(self, bgr_image):
        """최소 면적을 만족하는 가장 큰 빨간 영역을 사과 후보로 선택한다."""
        mask = self.red_mask(bgr_image)
        contours, _hierarchy = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        candidates = [
            contour
            for contour in contours
            if cv2.contourArea(contour) >= self.minimum_contour_area
        ]
        if not candidates:
            return None, mask
        return max(candidates, key=cv2.contourArea), mask

    def depth_in_meters(self, depth_message: Image):
        """Isaac/ROS depth encoding을 meter 단위 float 배열로 통일한다."""
        depth = self.bridge.imgmsg_to_cv2(depth_message, desired_encoding="passthrough")
        encoding = depth_message.encoding.upper()
        if encoding == "16UC1" or depth.dtype == np.uint16:
            return depth.astype(np.float32) / 1000.0
        return depth.astype(np.float32)

    def robust_depth(self, contour, depth_m):
        """윤곽 내부 유효 depth 중앙값을 사용해 잎·배경 outlier를 줄인다."""
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
        values = depth_m[valid]
        if values.size < 5:
            return None
        return float(np.median(values))

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
            return None

        translation = transform.transform.translation
        rotation = transform.transform.rotation
        quaternion = np.array(
            [rotation.x, rotation.y, rotation.z, rotation.w], dtype=float
        )
        quaternion_norm = np.linalg.norm(quaternion)
        if quaternion_norm <= 1e-9:
            return None
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
        # 현재 프로젝트 MVP 규약에 따라 접근 orientation은 월드축과 동일하다.
        result.pose.orientation.w = 1.0
        return result

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

        contour, _red_mask = self.find_apple_contour(bgr)
        annotated = bgr.copy()
        if contour is None:
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

        center = self.contour_center(contour)
        depth_value = self.robust_depth(contour, depth_m)
        if center is None or depth_value is None:
            cv2.drawContours(annotated, [contour], -1, (0, 165, 255), 2)
            cv2.putText(
                annotated,
                "INVALID DEPTH",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 165, 255),
                2,
            )
            self.publish_debug_image(rgb_message, annotated)
            self.show_debug(annotated)
            return

        u, v = center
        surface_point_camera = self.deproject(u, v, depth_value, camera_info)
        point_camera = self.surface_point_to_center(
            surface_point_camera,
            self.apple_radius_m,
        )
        camera_pose = self.make_camera_pose(rgb_message, point_camera)
        self.camera_pose_publisher.publish(camera_pose)

        world_pose = self.transform_to_world(camera_pose)
        if world_pose is not None:
            self.target_pose_publisher.publish(world_pose)

        cv2.drawContours(annotated, [contour], -1, (0, 255, 0), 2)
        cv2.circle(annotated, (round(u), round(v)), 5, (255, 0, 0), -1)
        text = (
            f"camera x={point_camera[0]:.3f} y={point_camera[1]:.3f} "
            f"z={point_camera[2]:.3f} m"
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
                f"사과 surface camera xyz = "
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
