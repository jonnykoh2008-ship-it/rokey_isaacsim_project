"""Adapt synchronized conveyor RGB-D topics to the quality inspection contract."""

from __future__ import annotations

import copy
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any

from inspection_session import QUALITY_CAMERA_OPTICAL_FRAME
from opencv_size_grader import AppleNotDetected, DetectionConfig, detect_single_apple


DEFAULT_RGB_TOPIC = "/rgb"
DEFAULT_DEPTH_TOPIC = "/depth"
DEFAULT_CAMERA_INFO_TOPIC = "/camera_info"
INSPECTION_TOPIC = "/quality/inspection_images"
COMPLETION_TOPIC = "/quality/inspection_completed"
DEFAULT_REARM_ABSENT_FRAMES = 3
DEFAULT_SYNC_QUEUE_SIZE = 20


try:
    import rclpy
    from appleproj_interfaces.msg import InspectionCompleted, InspectionImage
    from rclpy.node import Node
    from rclpy.parameter import Parameter
    from rclpy.qos import (
        DurabilityPolicy,
        HistoryPolicy,
        QoSProfile,
        ReliabilityPolicy,
    )
    from sensor_msgs.msg import CameraInfo, CompressedImage, Image
    from std_msgs.msg import Header

    _ROS_IMPORT_ERROR: ImportError | None = None
except ImportError as exc:
    rclpy = None  # type: ignore[assignment]
    InspectionCompleted = None  # type: ignore[assignment,misc]
    InspectionImage = None  # type: ignore[assignment,misc]
    CameraInfo = None  # type: ignore[assignment,misc]
    CompressedImage = None  # type: ignore[assignment,misc]
    Image = None  # type: ignore[assignment,misc]
    Header = None  # type: ignore[assignment,misc]
    Node = object  # type: ignore[assignment,misc]
    Parameter = None  # type: ignore[assignment,misc]
    QoSProfile = None  # type: ignore[assignment,misc]
    ReliabilityPolicy = None  # type: ignore[assignment,misc]
    DurabilityPolicy = None  # type: ignore[assignment,misc]
    HistoryPolicy = None  # type: ignore[assignment,misc]
    _ROS_IMPORT_ERROR = exc


def stamp_to_ns(stamp: Any) -> int:
    return int(stamp.sec) * 1_000_000_000 + int(stamp.nanosec)


@dataclass
class _PendingFrame:
    rgb: Any | None = None
    depth: Any | None = None
    camera_info: Any | None = None

    @property
    def complete(self) -> bool:
        return self.rgb is not None and self.depth is not None and self.camera_info is not None


@dataclass
class ExactStampSynchronizer:
    """Bounded exact-stamp synchronizer independent of ROS message_filters."""

    queue_size: int = DEFAULT_SYNC_QUEUE_SIZE
    _pending: OrderedDict[int, _PendingFrame] = field(
        default_factory=OrderedDict,
        init=False,
        repr=False,
    )

    def __post_init__(self) -> None:
        if self.queue_size < 1:
            raise ValueError("queue_size must be positive")

    def add(self, component: str, message: Any) -> tuple[Any, Any, Any] | None:
        if component not in {"rgb", "depth", "camera_info"}:
            raise ValueError(f"unsupported synchronized component: {component}")
        key = stamp_to_ns(message.header.stamp)
        pending = self._pending.setdefault(key, _PendingFrame())
        setattr(pending, component, message)
        self._pending.move_to_end(key)
        while len(self._pending) > self.queue_size:
            self._pending.popitem(last=False)
        if not pending.complete:
            return None
        self._pending.pop(key, None)
        return pending.rgb, pending.depth, pending.camera_info


def _packed_rows(message: Any, bytes_per_pixel: int) -> bytes:
    import numpy as np

    height = int(message.height)
    width = int(message.width)
    step = int(message.step)
    row_size = width * bytes_per_pixel
    if height <= 0 or width <= 0 or step < row_size:
        raise ValueError("raw image dimensions or step are invalid")
    raw = np.frombuffer(bytes(message.data), dtype=np.uint8)
    if raw.size < height * step:
        raise ValueError("raw image data is shorter than height * step")
    rows = raw[: height * step].reshape(height, step)
    return np.ascontiguousarray(rows[:, :row_size]).tobytes()


def decode_rgb_bgr(message: Any):
    """Decode common ROS Image RGB encodings into an OpenCV BGR array."""

    import cv2
    import numpy as np

    encoding = str(message.encoding).lower()
    channels = {
        "rgb8": 3,
        "bgr8": 3,
        "rgba8": 4,
        "bgra8": 4,
    }.get(encoding)
    if channels is None:
        raise ValueError(f"unsupported RGB encoding: {message.encoding!r}")
    packed = _packed_rows(message, channels)
    image = np.frombuffer(packed, dtype=np.uint8).reshape(
        int(message.height),
        int(message.width),
        channels,
    )
    if encoding == "rgb8":
        return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if encoding == "rgba8":
        return cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
    if encoding == "bgra8":
        return cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    return image.copy()


def decode_depth_mm(message: Any):
    """Decode 16-bit millimetres or 32-bit metres into uint16 millimetres."""

    import numpy as np

    encoding = str(message.encoding).lower()
    is_bigendian = bool(message.is_bigendian)
    if encoding in {"16uc1", "mono16"}:
        packed = _packed_rows(message, 2)
        dtype = np.dtype(">u2" if is_bigendian else "<u2")
        return np.frombuffer(packed, dtype=dtype).reshape(
            int(message.height), int(message.width)
        ).astype(np.uint16)
    if encoding == "32fc1":
        packed = _packed_rows(message, 4)
        dtype = np.dtype(">f4" if is_bigendian else "<f4")
        depth_m = np.frombuffer(packed, dtype=dtype).reshape(
            int(message.height), int(message.width)
        )
        depth_mm = np.zeros(depth_m.shape, dtype=np.uint16)
        valid = np.isfinite(depth_m) & (depth_m > 0.0) & (depth_m <= 65.535)
        depth_mm[valid] = np.rint(depth_m[valid] * 1000.0).astype(np.uint16)
        return depth_mm
    raise ValueError(f"unsupported depth encoding: {message.encoding!r}")


def selected_apple_mask(image, config: DetectionConfig = DetectionConfig()):
    """Return only the selected apple contour, excluding other saturated objects."""

    import cv2
    import numpy as np

    detection = detect_single_apple(image, config)
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    cv2.drawContours(mask, [detection.contour], -1, 255, thickness=cv2.FILLED)
    return detection, mask


def encode_image(extension: str, image) -> bytes:
    import cv2

    success, encoded = cv2.imencode(extension, image)
    if not success:
        raise ValueError(f"OpenCV failed to encode {extension} image")
    return encoded.tobytes()


def make_reliable_qos(depth: int = 10) -> Any:
    if QoSProfile is None:
        raise RuntimeError("rclpy is required to construct QoS profiles")
    return QoSProfile(
        reliability=ReliabilityPolicy.RELIABLE,
        durability=DurabilityPolicy.VOLATILE,
        history=HistoryPolicy.KEEP_LAST,
        depth=depth,
    )


class ConveyorCameraAdapterNode(Node):  # type: ignore[misc]
    """Create one InspectionImage when a new apple enters the camera view."""

    def __init__(self) -> None:
        if _ROS_IMPORT_ERROR is not None:
            raise RuntimeError(
                "ROS 2 Python packages are unavailable; source ROS 2 Jazzy and "
                "the built workspace first"
            ) from _ROS_IMPORT_ERROR
        super().__init__(
            "conveyor_camera_adapter_node",
            parameter_overrides=[Parameter("use_sim_time", value=True)],
            automatically_declare_parameters_from_overrides=True,
        )
        for name, default in (
            ("rgb_topic", DEFAULT_RGB_TOPIC),
            ("depth_topic", DEFAULT_DEPTH_TOPIC),
            ("camera_info_topic", DEFAULT_CAMERA_INFO_TOPIC),
            ("output_frame_id", QUALITY_CAMERA_OPTICAL_FRAME),
            ("rearm_absent_frames", DEFAULT_REARM_ABSENT_FRAMES),
            ("min_saturation", DetectionConfig().min_saturation),
            ("min_value", DetectionConfig().min_value),
            ("max_value", DetectionConfig().max_value),
            ("min_area_ratio", DetectionConfig().min_area_ratio),
            ("morphology_kernel", DetectionConfig().morphology_kernel),
        ):
            if not self.has_parameter(name):
                self.declare_parameter(name, default)

        self._output_frame_id = str(self.get_parameter("output_frame_id").value)
        self._rearm_absent_frames = int(
            self.get_parameter("rearm_absent_frames").value
        )
        if self._rearm_absent_frames < 1:
            raise ValueError("rearm_absent_frames must be positive")
        self._detection_config = DetectionConfig(
            min_saturation=int(self.get_parameter("min_saturation").value),
            min_value=int(self.get_parameter("min_value").value),
            max_value=int(self.get_parameter("max_value").value),
            min_area_ratio=float(self.get_parameter("min_area_ratio").value),
            morphology_kernel=int(self.get_parameter("morphology_kernel").value),
        )
        self._synchronizer = ExactStampSynchronizer()
        self._armed = True
        self._absent_frames = 0
        self._inspection_sequence = 0

        qos = make_reliable_qos()
        self._inspection_publisher = self.create_publisher(
            InspectionImage, INSPECTION_TOPIC, qos
        )
        self._completion_publisher = self.create_publisher(
            InspectionCompleted, COMPLETION_TOPIC, qos
        )
        self.create_subscription(
            Image,
            str(self.get_parameter("rgb_topic").value),
            lambda message: self._accept("rgb", message),
            qos,
        )
        self.create_subscription(
            Image,
            str(self.get_parameter("depth_topic").value),
            lambda message: self._accept("depth", message),
            qos,
        )
        self.create_subscription(
            CameraInfo,
            str(self.get_parameter("camera_info_topic").value),
            lambda message: self._accept("camera_info", message),
            qos,
        )
        self.get_logger().info(
            "GPU PC 2 conveyor adapter ready: "
            f"{self.get_parameter('rgb_topic').value} + "
            f"{self.get_parameter('depth_topic').value} + "
            f"{self.get_parameter('camera_info_topic').value} -> "
            f"{INSPECTION_TOPIC}"
        )

    def _accept(self, component: str, message: Any) -> None:
        synchronized = self._synchronizer.add(component, message)
        if synchronized is None:
            return
        try:
            self._process(*synchronized)
        except Exception as exc:
            self.get_logger().error(
                f"Rejected synchronized conveyor RGB-D frame: {type(exc).__name__}: {exc}"
            )

    def _process(self, rgb_message: Any, depth_message: Any, camera_info: Any) -> None:
        signatures = {
            (
                stamp_to_ns(message.header.stamp),
                str(message.header.frame_id),
            )
            for message in (rgb_message, depth_message, camera_info)
        }
        if len(signatures) != 1:
            raise ValueError("RGB, depth and CameraInfo stamps/frame_ids must match")
        if (
            int(rgb_message.width) != int(depth_message.width)
            or int(rgb_message.height) != int(depth_message.height)
            or int(rgb_message.width) != int(camera_info.width)
            or int(rgb_message.height) != int(camera_info.height)
        ):
            raise ValueError("RGB, depth and CameraInfo dimensions must match")

        image = decode_rgb_bgr(rgb_message)
        depth_mm = decode_depth_mm(depth_message)
        try:
            detection, apple_mask = selected_apple_mask(image, self._detection_config)
        except AppleNotDetected:
            self._absent_frames += 1
            if self._absent_frames >= self._rearm_absent_frames:
                self._armed = True
            return
        self._absent_frames = 0
        if not self._armed:
            return
        self._armed = False
        self._inspection_sequence += 1
        self._publish_inspection(
            rgb_message,
            camera_info,
            image,
            apple_mask,
            depth_mm,
            detection.confidence,
        )

    def _header(self, source_stamp: Any) -> Any:
        header = Header()
        header.stamp = copy.deepcopy(source_stamp)
        header.frame_id = self._output_frame_id
        return header

    @staticmethod
    def _compressed(header: Any, data: bytes, image_format: str) -> Any:
        message = CompressedImage()
        message.header = copy.deepcopy(header)
        message.format = image_format
        message.data = data
        return message

    def _publish_inspection(
        self,
        rgb_message: Any,
        camera_info: Any,
        image,
        apple_mask,
        depth_mm,
        detection_confidence: float,
    ) -> None:
        import numpy as np

        header = self._header(rgb_message.header.stamp)
        stamp_ns = stamp_to_ns(header.stamp)
        suffix = f"{stamp_ns}-{self._inspection_sequence}"
        inspection_id = f"inspection-{suffix}"
        apple_id = f"apple-{suffix}"
        ignore_mask = np.zeros(apple_mask.shape, dtype=np.uint8)

        inspection = InspectionImage()
        inspection.header = copy.deepcopy(header)
        inspection.inspection_id = inspection_id
        inspection.apple_id = apple_id
        inspection.frame_index = 0
        inspection.total_frames = 1
        inspection.image = self._compressed(
            header,
            encode_image(".jpg", image),
            "bgr8; jpeg compressed bgr8",
        )
        inspection.apple_mask = self._compressed(
            header,
            encode_image(".png", apple_mask),
            "mono8; png",
        )
        inspection.ignore_mask = self._compressed(
            header,
            encode_image(".png", ignore_mask),
            "mono8; png",
        )
        inspection.aligned_depth = self._compressed(
            header,
            encode_image(".png", depth_mm),
            "16UC1; compressedDepth png",
        )
        inspection.camera_info = copy.deepcopy(camera_info)
        inspection.camera_info.header = copy.deepcopy(header)

        completion = InspectionCompleted()
        completion.header = copy.deepcopy(header)
        completion.inspection_id = inspection_id
        completion.apple_id = apple_id
        completion.total_frames = 1

        self._inspection_publisher.publish(inspection)
        self._completion_publisher.publish(completion)
        self.get_logger().info(
            f"Published inspection {inspection_id}: "
            f"mask_confidence={detection_confidence:.3f}"
        )


def main(args: list[str] | None = None) -> None:
    if rclpy is None:
        raise RuntimeError(
            "ROS 2 Python packages are unavailable; source ROS 2 Jazzy and the workspace"
        ) from _ROS_IMPORT_ERROR
    rclpy.init(args=args)
    node = ConveyorCameraAdapterNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
