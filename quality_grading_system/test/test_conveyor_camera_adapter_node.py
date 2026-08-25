from __future__ import annotations

import unittest
from types import SimpleNamespace

import numpy as np

from conveyor_camera_adapter_node import (
    ExactStampSynchronizer,
    decode_depth_mm,
    decode_rgb_bgr,
    selected_apple_mask,
)


def header(sec: int, nanosec: int = 0):
    return SimpleNamespace(
        stamp=SimpleNamespace(sec=sec, nanosec=nanosec),
        frame_id="sim_camera",
    )


def image_message(array, encoding: str, *, step_padding: int = 0, sec: int = 1):
    height, width = array.shape[:2]
    row_size = array[0].nbytes
    step = row_size + step_padding
    rows = []
    for row in array:
        rows.append(row.tobytes() + bytes(step_padding))
    return SimpleNamespace(
        header=header(sec),
        height=height,
        width=width,
        encoding=encoding,
        is_bigendian=0,
        step=step,
        data=b"".join(rows),
    )


class ExactStampSynchronizerTest(unittest.TestCase):
    def test_returns_only_complete_equal_stamp_triplet(self) -> None:
        synchronizer = ExactStampSynchronizer(queue_size=3)
        rgb = SimpleNamespace(header=header(10))
        depth = SimpleNamespace(header=header(10))
        info = SimpleNamespace(header=header(10))
        self.assertIsNone(synchronizer.add("rgb", rgb))
        self.assertIsNone(synchronizer.add("camera_info", info))
        self.assertEqual(
            synchronizer.add("depth", depth),
            (rgb, depth, info),
        )

    def test_discards_old_incomplete_stamps(self) -> None:
        synchronizer = ExactStampSynchronizer(queue_size=2)
        synchronizer.add("rgb", SimpleNamespace(header=header(1)))
        synchronizer.add("rgb", SimpleNamespace(header=header(2)))
        synchronizer.add("rgb", SimpleNamespace(header=header(3)))
        self.assertEqual(tuple(synchronizer._pending), (2_000_000_000, 3_000_000_000))


class ImageConversionTest(unittest.TestCase):
    def test_decodes_rgb8_with_row_padding_to_bgr(self) -> None:
        rgb = np.array([[[255, 10, 20], [1, 2, 3]]], dtype=np.uint8)
        decoded = decode_rgb_bgr(image_message(rgb, "rgb8", step_padding=2))
        np.testing.assert_array_equal(
            decoded,
            np.array([[[20, 10, 255], [3, 2, 1]]], dtype=np.uint8),
        )

    def test_converts_float_depth_metres_to_uint16_millimetres(self) -> None:
        depth = np.array([[0.5, 1.234, np.nan, np.inf, -1.0]], dtype=np.float32)
        decoded = decode_depth_mm(image_message(depth, "32FC1"))
        self.assertEqual(decoded.dtype, np.uint16)
        np.testing.assert_array_equal(
            decoded,
            np.array([[500, 1234, 0, 0, 0]], dtype=np.uint16),
        )

    def test_preserves_16uc1_millimetres(self) -> None:
        depth = np.array([[400, 1200]], dtype=np.uint16)
        decoded = decode_depth_mm(image_message(depth, "16UC1"))
        np.testing.assert_array_equal(decoded, depth)

    def test_selected_mask_excludes_other_saturated_objects(self) -> None:
        import cv2

        image = np.full((180, 240, 3), 180, dtype=np.uint8)
        cv2.circle(image, (80, 90), 45, (20, 30, 210), thickness=-1)
        cv2.circle(image, (210, 25), 10, (20, 210, 20), thickness=-1)
        detection, mask = selected_apple_mask(image)
        self.assertGreater(detection.diameter_px, 80.0)
        self.assertEqual(int(mask[90, 80]), 255)
        self.assertEqual(int(mask[25, 210]), 0)


if __name__ == "__main__":
    unittest.main()
