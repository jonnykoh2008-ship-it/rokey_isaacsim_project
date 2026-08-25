from __future__ import annotations

import unittest

import cv2
import numpy as np

from opencv_size_grader import (
    AppleNotDetected,
    DetectionConfig,
    detect_single_apple,
    draw_size_result,
    fit_linear_calibration,
    grade_image_by_size,
    pixels_per_mm_from_reference,
)
from quality_rules import Grade


def apple_image(radius: int, *, size: int = 320):
    image = np.full((size, size, 3), 150, dtype=np.uint8)
    cv2.circle(
        image,
        (size // 2, size // 2),
        radius,
        (30, 40, 210),
        thickness=-1,
        lineType=cv2.LINE_AA,
    )
    return image


class OpenCvAppleDetectionTest(unittest.TestCase):
    def test_detects_largest_saturated_apple(self) -> None:
        detection = detect_single_apple(apple_image(60))
        self.assertAlmostEqual(detection.center[0], 160.0, delta=2.0)
        self.assertAlmostEqual(detection.center[1], 160.0, delta=2.0)
        self.assertAlmostEqual(detection.diameter_px, 120.0, delta=4.0)
        self.assertGreater(detection.confidence, 0.75)

    def test_rejects_plain_background(self) -> None:
        background = np.full((240, 320, 3), 150, dtype=np.uint8)
        with self.assertRaises(AppleNotDetected):
            detect_single_apple(background)

    def test_reference_calibration_recovers_size(self) -> None:
        config = DetectionConfig()
        pixels_per_mm = pixels_per_mm_from_reference(
            apple_image(60),
            60.0,
            config,
        )
        result = grade_image_by_size(apple_image(78), pixels_per_mm, config)
        self.assertAlmostEqual(result.diameter_mm, 78.0, delta=2.0)
        self.assertEqual(result.grade, Grade.HIGH)

    def test_draws_visible_overlay_without_resizing(self) -> None:
        image = apple_image(65)
        result = grade_image_by_size(image, calibration=2.0)
        annotated = draw_size_result(image, result)
        self.assertEqual(annotated.shape, image.shape)
        self.assertFalse(np.array_equal(annotated, image))

    def test_multi_point_linear_calibration_includes_intercept(self) -> None:
        calibration = fit_linear_calibration(
            [100.0, 120.0, 160.0],
            [60.0, 70.0, 90.0],
        )
        self.assertAlmostEqual(calibration.mm_per_pixel, 0.5)
        self.assertAlmostEqual(calibration.intercept_mm, 10.0)
        self.assertAlmostEqual(calibration.diameter_mm(130.0), 75.0)


if __name__ == "__main__":
    unittest.main()
