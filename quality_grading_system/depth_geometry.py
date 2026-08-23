"""RGB-aligned depth geometry for one quality-inspection frame."""

from __future__ import annotations

import io
from dataclasses import dataclass, replace
from typing import Any

from inspection_session import InspectionContractError, InspectionFrame
from quality_rules import FrameMeasurements


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MIN_GEOMETRY_PIXELS = 10


class GeometryMeasurementError(InspectionContractError):
    """Raised when synchronized RGB-D data cannot produce valid geometry."""


@dataclass(frozen=True)
class GeometryMeasurements:
    diameter_mm: float
    diameter_confidence: float
    apple_mask: Any
    depth_m: Any


def _decode_png(data: bytes, description: str):
    try:
        import numpy as np
        from PIL import Image
    except ImportError as exc:
        raise GeometryMeasurementError("NumPy and Pillow are required for RGB-D geometry") from exc

    offset = data.find(PNG_SIGNATURE)
    if offset < 0:
        raise GeometryMeasurementError(f"{description} does not contain a PNG payload")
    try:
        value = np.asarray(Image.open(io.BytesIO(data[offset:])))
    except Exception as exc:
        raise GeometryMeasurementError(f"cannot decode {description} PNG") from exc
    if value.ndim == 3:
        value = value[..., 0]
    if value.ndim != 2:
        raise GeometryMeasurementError(f"{description} must decode to one channel")
    return value


def _decode_rgb_shape(frame: InspectionFrame) -> tuple[int, int]:
    try:
        from PIL import Image

        with Image.open(io.BytesIO(frame.image_data)) as image:
            width, height = image.size
    except Exception as exc:
        raise GeometryMeasurementError("cannot decode compressed RGB image") from exc
    if width <= 0 or height <= 0:
        raise GeometryMeasurementError("compressed RGB image has invalid dimensions")
    return height, width


def decode_apple_mask(frame: InspectionFrame):
    import numpy as np

    if "png" not in frame.apple_mask_format.lower():
        raise GeometryMeasurementError("apple_mask must use lossless PNG")
    mask = _decode_png(frame.apple_mask_data, "apple_mask") > 0
    if not bool(mask.any()):
        raise GeometryMeasurementError("apple_mask is empty")
    return np.asarray(mask, dtype=bool)


def decode_aligned_depth_m(frame: InspectionFrame):
    import numpy as np

    normalized = frame.depth_format.lower().replace(" ", "")
    if "16uc1" not in normalized or "compresseddepth" not in normalized or "png" not in normalized:
        raise GeometryMeasurementError(
            "aligned_depth format must be '16UC1; compressedDepth png'"
        )
    depth_mm = _decode_png(frame.depth_data, "aligned_depth")
    if depth_mm.dtype != np.uint16:
        if not np.issubdtype(depth_mm.dtype, np.integer):
            raise GeometryMeasurementError("aligned_depth PNG must contain uint16 millimetres")
        if int(depth_mm.min()) < 0 or int(depth_mm.max()) > 65_535:
            raise GeometryMeasurementError("aligned_depth values must fit uint16")
        depth_mm = depth_mm.astype(np.uint16)
    return depth_mm.astype(np.float32) * 0.001


def _intrinsics(frame: InspectionFrame) -> tuple[float, float, float, float]:
    if len(frame.camera_p) != 12 or len(frame.camera_k) != 9:
        raise GeometryMeasurementError("CameraInfo K and P matrices have invalid lengths")
    fx, fy = float(frame.camera_p[0]), float(frame.camera_p[5])
    cx, cy = float(frame.camera_p[2]), float(frame.camera_p[6])
    if fx <= 0.0 or fy <= 0.0:
        fx, fy = float(frame.camera_k[0]), float(frame.camera_k[4])
        cx, cy = float(frame.camera_k[2]), float(frame.camera_k[5])
    if fx <= 0.0 or fy <= 0.0:
        raise GeometryMeasurementError("CameraInfo is uncalibrated")
    return fx, fy, cx, cy


def measure_geometry(frame: InspectionFrame) -> GeometryMeasurements:
    """Measure visible apple diameter from a synchronized mask and Z-depth."""

    import numpy as np

    rgb_shape = _decode_rgb_shape(frame)
    apple_mask = decode_apple_mask(frame)
    depth_m = decode_aligned_depth_m(frame)
    expected_shape = (frame.camera_height, frame.camera_width)
    if (
        rgb_shape != expected_shape
        or apple_mask.shape != expected_shape
        or depth_m.shape != expected_shape
    ):
        raise GeometryMeasurementError(
            "RGB, apple_mask, aligned_depth and CameraInfo dimensions must match"
        )
    fx, fy, cx, cy = _intrinsics(frame)
    valid = apple_mask & np.isfinite(depth_m) & (depth_m > 0.0)
    valid_count = int(valid.sum())
    apple_count = int(apple_mask.sum())
    if valid_count < MIN_GEOMETRY_PIXELS:
        raise GeometryMeasurementError("too few valid apple depth pixels")

    ys, xs = np.nonzero(valid)
    z = depth_m[ys, xs]
    points_x = (xs.astype(np.float32) - cx) * z / fx
    points_y = (ys.astype(np.float32) - cy) * z / fy
    extent_x = np.percentile(points_x, 99.5) - np.percentile(points_x, 0.5)
    extent_y = np.percentile(points_y, 99.5) - np.percentile(points_y, 0.5)
    diameter_mm = float(max(extent_x, extent_y) * 1000.0)
    if not np.isfinite(diameter_mm) or diameter_mm <= 0.0:
        raise GeometryMeasurementError("computed diameter is invalid")
    return GeometryMeasurements(
        diameter_mm=diameter_mm,
        diameter_confidence=min(1.0, valid_count / apple_count),
        apple_mask=apple_mask,
        depth_m=depth_m,
    )


def _prediction_mask(value: Any, name: str, expected_shape: tuple[int, int]):
    import numpy as np

    mask = getattr(value, name, None)
    if mask is None:
        return None
    mask = np.asarray(mask)
    if mask.shape != expected_shape:
        raise GeometryMeasurementError(f"{name} dimensions must match aligned depth")
    return mask >= 0.5


def _surface_area_cm2(
    damage_mask,
    apple_mask,
    depth_m,
    frame: InspectionFrame,
) -> tuple[float, float]:
    import numpy as np

    fx, fy, cx, cy = _intrinsics(frame)
    valid_depth = np.isfinite(depth_m) & (depth_m > 0.0)
    damage = damage_mask & apple_mask
    damage_count = int(damage.sum())
    if damage_count == 0:
        return 0.0, 1.0
    valid_damage = damage & valid_depth
    confidence = int(valid_damage.sum()) / damage_count
    if int(valid_damage.sum()) < 3:
        raise GeometryMeasurementError("too few valid depth pixels in damage mask")

    height, width = depth_m.shape
    ys, xs = np.indices((height, width), dtype=np.float32)
    points = np.empty((height, width, 3), dtype=np.float32)
    points[..., 2] = depth_m
    points[..., 0] = (xs - cx) * depth_m / fx
    points[..., 1] = (ys - cy) * depth_m / fy

    p00 = points[:-1, :-1]
    p01 = points[:-1, 1:]
    p10 = points[1:, :-1]
    p11 = points[1:, 1:]
    m00 = valid_damage[:-1, :-1]
    m01 = valid_damage[:-1, 1:]
    m10 = valid_damage[1:, :-1]
    m11 = valid_damage[1:, 1:]

    def triangle_area(a, b, c, mask):
        cross = np.cross(b - a, c - a)
        area = 0.5 * np.linalg.norm(cross, axis=2)
        return float(area[mask].sum())

    first = triangle_area(p00, p01, p10, m00 & m01 & m10)
    second = triangle_area(p11, p10, p01, m11 & m10 & m01)
    return (first + second) * 10_000.0, confidence


def combine_prediction_with_geometry(frame: InspectionFrame, prediction: Any) -> FrameMeasurements:
    """Combine RGB model outputs with depth-derived diameter and damage area."""

    geometry = measure_geometry(frame)
    expected_shape = geometry.apple_mask.shape

    if isinstance(prediction, FrameMeasurements):
        return replace(
            prediction,
            diameter_mm=geometry.diameter_mm,
            diameter_confidence=geometry.diameter_confidence,
        )

    color_mask = _prediction_mask(prediction, "color_mask", expected_shape)
    damage_mask = _prediction_mask(prediction, "damage_mask", expected_shape)
    valid_surface = geometry.apple_mask
    color_ratio = (
        float((color_mask & valid_surface).sum() / valid_surface.sum())
        if color_mask is not None
        else None
    )

    damage_area = None
    damage_geometry_confidence = None
    if damage_mask is not None:
        damage_area, damage_geometry_confidence = _surface_area_cm2(
            damage_mask,
            geometry.apple_mask,
            geometry.depth_m,
            frame,
        )
    model_damage_confidence = getattr(prediction, "damage_confidence", None)
    damage_confidence = (
        min(float(model_damage_confidence), float(damage_geometry_confidence))
        if model_damage_confidence is not None and damage_geometry_confidence is not None
        else None
    )
    return FrameMeasurements(
        color_ratio=color_ratio,
        diameter_mm=geometry.diameter_mm,
        damage_area_cm2=damage_area,
        severe_defect=getattr(prediction, "severe_defect", None),
        color_confidence=getattr(prediction, "color_confidence", None),
        diameter_confidence=geometry.diameter_confidence,
        damage_confidence=damage_confidence,
        severe_confidence=getattr(prediction, "severe_confidence", None),
    )
