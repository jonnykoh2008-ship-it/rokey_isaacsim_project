import math
import unittest

import cv2
import numpy as np

from leaf_obstacle_geometry import (
    CameraIntrinsics,
    build_leaf_sphere_proxies,
    create_leaf_mask,
    deproject_pixels,
    depth_to_meters,
    masked_depth_to_points,
    transform_points,
    validate_aligned_rgbd,
    voxelize_world_points,
)


class TestRgbdValidation(unittest.TestCase):
    def test_accepts_matching_rgb_depth_resolution(self):
        rgb = np.zeros((4, 6, 3), dtype=np.uint8)
        depth = np.zeros((4, 6), dtype=np.float32)
        self.assertEqual(validate_aligned_rgbd(rgb, depth), (4, 6))

    def test_rejects_rgb_depth_resolution_mismatch(self):
        rgb = np.zeros((4, 6, 3), dtype=np.uint8)
        depth = np.zeros((3, 6), dtype=np.float32)
        with self.assertRaisesRegex(ValueError, "resolutions do not match"):
            validate_aligned_rgbd(rgb, depth)

    def test_converts_supported_depth_encodings(self):
        depth_mm = np.array([[0, 1_000, 2_500]], dtype=np.uint16)
        np.testing.assert_allclose(
            depth_to_meters(depth_mm, "16UC1"),
            [[0.0, 1.0, 2.5]],
        )
        depth_m = np.array([[0.5, np.nan]], dtype=np.float64)
        converted = depth_to_meters(depth_m, "32FC1")
        self.assertEqual(converted.dtype, np.float32)
        self.assertAlmostEqual(float(converted[0, 0]), 0.5)
        self.assertTrue(np.isnan(converted[0, 1]))

    def test_rejects_encoding_storage_mismatch(self):
        with self.assertRaisesRegex(ValueError, "numpy.uint16"):
            depth_to_meters(np.ones((2, 2), dtype=np.float32), "16UC1")
        with self.assertRaisesRegex(ValueError, "unsupported"):
            depth_to_meters(np.ones((2, 2), dtype=np.uint8), "8UC1")


class TestLeafMask(unittest.TestCase):
    def test_filters_small_components_and_applies_exclusion(self):
        image = np.zeros((12, 12, 3), dtype=np.uint8)
        green = cv2.cvtColor(
            np.uint8([[[60, 255, 255]]]), cv2.COLOR_HSV2BGR
        )[0, 0]
        image[2:8, 2:8] = green
        image[10, 10] = green
        exclusion = np.zeros((12, 12), dtype=np.uint8)
        exclusion[2:4, 2:4] = 255

        mask = create_leaf_mask(
            image,
            hsv_lower=(50, 200, 200),
            hsv_upper=(70, 255, 255),
            minimum_component_area_px=5,
            morphology_kernel_size=1,
            exclusion_mask=exclusion,
        )

        self.assertEqual(int(mask[10, 10]), 0)
        self.assertEqual(int(mask[2, 2]), 0)
        self.assertEqual(int(mask[6, 6]), 255)

    def test_requires_explicit_valid_hsv_and_kernel_parameters(self):
        image = np.zeros((2, 2, 3), dtype=np.uint8)
        with self.assertRaisesRegex(ValueError, "hsv_lower"):
            create_leaf_mask(
                image,
                hsv_lower=(100, 0, 0),
                hsv_upper=(90, 255, 255),
                minimum_component_area_px=1,
                morphology_kernel_size=1,
            )
        with self.assertRaisesRegex(ValueError, "positive odd"):
            create_leaf_mask(
                image,
                hsv_lower=(50, 0, 0),
                hsv_upper=(70, 255, 255),
                minimum_component_area_px=1,
                morphology_kernel_size=2,
            )


class TestDepthGeometry(unittest.TestCase):
    def test_camera_intrinsics_from_camera_info_matrix(self):
        intrinsics = CameraIntrinsics.from_camera_matrix(
            [100.0, 0.0, 2.0, 0.0, 120.0, 3.0, 0.0, 0.0, 1.0]
        )
        self.assertEqual(intrinsics, CameraIntrinsics(100.0, 120.0, 2.0, 3.0))
        with self.assertRaisesRegex(ValueError, "focal lengths"):
            CameraIntrinsics(0.0, 100.0, 0.0, 0.0)

    def test_deprojects_pixels_using_ros_optical_axes(self):
        points = deproject_pixels(
            np.array([[2.0, 3.0], [12.0, 23.0]]),
            np.array([2.0, 2.0]),
            CameraIntrinsics(fx=100.0, fy=200.0, cx=2.0, cy=3.0),
        )
        np.testing.assert_allclose(
            points,
            np.array([[0.0, 0.0, 2.0], [0.2, 0.2, 2.0]]),
        )

    def test_masked_depth_reports_quality_before_stride_sampling(self):
        mask = np.full((3, 3), 255, dtype=np.uint8)
        depth = np.array(
            [
                [1.0, np.nan, 1.0],
                [0.0, 1.0, 8.0],
                [1.0, 1.0, 1.0],
            ],
            dtype=np.float32,
        )
        result = masked_depth_to_points(
            mask,
            depth,
            CameraIntrinsics(100.0, 100.0, 1.0, 1.0),
            minimum_depth_m=0.4,
            maximum_depth_m=6.0,
            pixel_stride=2,
        )
        self.assertEqual(result.mask_pixel_count, 9)
        self.assertEqual(result.valid_depth_pixel_count, 6)
        self.assertAlmostEqual(result.valid_depth_ratio, 6.0 / 9.0)
        np.testing.assert_array_equal(
            result.pixels_uv,
            np.array([[0.0, 0.0], [2.0, 0.0], [0.0, 2.0], [2.0, 2.0]]),
        )

    def test_transforms_points_with_xyzw_quaternion(self):
        angle = math.pi / 2.0
        transformed = transform_points(
            np.array([[1.0, 0.0, 0.0]]),
            translation_xyz=(1.0, 2.0, 3.0),
            quaternion_xyzw=(0.0, 0.0, math.sin(angle / 2.0), math.cos(angle / 2.0)),
        )
        np.testing.assert_allclose(transformed, [[1.0, 3.0, 3.0]], atol=1e-12)


class TestVoxelProxies(unittest.TestCase):
    def test_voxel_ids_and_centers_are_stable_across_input_order(self):
        points = np.array(
            [
                [0.01, 0.01, 0.01],
                [0.02, 0.03, 0.02],
                [0.11, 0.01, 0.01],
                [-0.01, 0.01, 0.01],
            ]
        )
        first = voxelize_world_points(points, voxel_size_m=0.1)
        second = voxelize_world_points(points[::-1], voxel_size_m=0.1)

        self.assertEqual(
            [voxel.obstacle_id for voxel in first],
            [voxel.obstacle_id for voxel in second],
        )
        self.assertEqual(
            [voxel.point_count for voxel in first],
            [voxel.point_count for voxel in second],
        )
        for left, right in zip(first, second):
            np.testing.assert_allclose(left.center_world, right.center_world)

    def test_proxy_limit_prefers_more_supported_voxels(self):
        points = np.array(
            [
                [0.01, 0.01, 0.01],
                [0.02, 0.02, 0.02],
                [0.03, 0.03, 0.03],
                [0.11, 0.01, 0.01],
                [0.21, 0.01, 0.01],
                [0.22, 0.02, 0.02],
            ]
        )
        proxies = build_leaf_sphere_proxies(
            points,
            voxel_size_m=0.1,
            proxy_radius_m=0.02,
            safety_margin_m=0.01,
            maximum_proxy_count=2,
        )
        self.assertEqual(len(proxies), 2)
        self.assertEqual(
            {proxy.point_count for proxy in proxies},
            {2, 3},
        )
        self.assertTrue(all(proxy.radius_m == 0.02 for proxy in proxies))
        self.assertTrue(all(proxy.safety_margin_m == 0.01 for proxy in proxies))


if __name__ == "__main__":
    unittest.main()
