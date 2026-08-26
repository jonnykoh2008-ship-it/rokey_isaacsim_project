from __future__ import annotations

import unittest
from types import SimpleNamespace

import numpy as np

from conveyor_camera_adapter_node import (
    DEFAULT_CAMERA_NAMESPACES,
    apple_crop_box,
    apple_position_m,
    cropped_camera_info,
    unmeasurable_surface_mask,
    IGNORE_BOUNDARY_ERODE_PX,
    DEFAULT_GROUP_QUEUE_SIZE,
    GROUP_STAMP_TOLERANCE_NS,
    ConveyorCameraAdapterNode,
    ExactStampSynchronizer,
    decode_depth_mm,
    decode_rgb_bgr,
    selected_apple_mask,
)
from inspection_session import (
    MAX_REPRESENTATIVE_FRAMES,
    QUALITY_CAMERA_OPTICAL_FRAMES,
    REPRESENTATIVE_INSTANTS,
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


class ThreeViewGroupingTest(unittest.TestCase):
    """One inspection needs all three views within the 20 ms contract window."""

    @staticmethod
    def _adapter():
        adapter = ConveyorCameraAdapterNode.__new__(ConveyorCameraAdapterNode)
        adapter._namespaces = list(DEFAULT_CAMERA_NAMESPACES)
        adapter._groups = {name: [] for name in DEFAULT_CAMERA_NAMESPACES}
        adapter.processed = []
        adapter._process_group = lambda stamp, group: adapter.processed.append(
            (stamp, sorted(group))
        )
        return adapter

    @staticmethod
    def _view(nanosec: int, frame_id: str, sec: int = 7):
        message = SimpleNamespace(
            header=SimpleNamespace(
                stamp=SimpleNamespace(sec=sec, nanosec=nanosec),
                frame_id=frame_id,
            )
        )
        return (message, message, message)

    def _feed_all(self, adapter, offsets, sec: int = 7):
        for namespace, frame_id, offset in zip(
            DEFAULT_CAMERA_NAMESPACES, QUALITY_CAMERA_OPTICAL_FRAMES, offsets
        ):
            adapter._collect(namespace, self._view(offset, frame_id, sec=sec))

    def test_identical_stamps_form_one_group(self) -> None:
        adapter = self._adapter()
        self._feed_all(adapter, (0, 0, 0))
        self.assertEqual(len(adapter.processed), 1)
        stamp_ns, namespaces = adapter.processed[0]
        self.assertEqual(stamp_ns, 7_000_000_000)
        self.assertEqual(namespaces, sorted(DEFAULT_CAMERA_NAMESPACES))

    def test_stamps_inside_tolerance_still_group(self) -> None:
        adapter = self._adapter()
        self._feed_all(adapter, (0, 5_000_000, 19_000_000))
        self.assertEqual(len(adapter.processed), 1)

    def test_stamps_outside_tolerance_do_not_group(self) -> None:
        adapter = self._adapter()
        self._feed_all(adapter, (0, 5_000_000, GROUP_STAMP_TOLERANCE_NS + 1_000_000))
        self.assertEqual(adapter.processed, [])

    def test_partial_group_is_not_processed(self) -> None:
        adapter = self._adapter()
        adapter._collect(
            DEFAULT_CAMERA_NAMESPACES[0],
            self._view(0, QUALITY_CAMERA_OPTICAL_FRAMES[0]),
        )
        adapter._collect(
            DEFAULT_CAMERA_NAMESPACES[1],
            self._view(0, QUALITY_CAMERA_OPTICAL_FRAMES[1]),
        )
        self.assertEqual(adapter.processed, [])

    def test_consumed_views_are_not_reused_by_a_later_tick(self) -> None:
        adapter = self._adapter()
        self._feed_all(adapter, (0, 0, 0), sec=7)
        self._feed_all(adapter, (0, 0, 0), sec=8)
        self.assertEqual(
            [stamp for stamp, _ in adapter.processed],
            [7_000_000_000, 8_000_000_000],
        )

    def test_one_camera_alone_never_completes_a_group(self) -> None:
        adapter = self._adapter()
        for sec in range(DEFAULT_GROUP_QUEUE_SIZE + 4):
            adapter._collect(
                DEFAULT_CAMERA_NAMESPACES[0],
                self._view(0, QUALITY_CAMERA_OPTICAL_FRAMES[0], sec=sec),
            )
        self.assertEqual(adapter.processed, [])
        self.assertLessEqual(
            len(adapter._groups[DEFAULT_CAMERA_NAMESPACES[0]]),
            DEFAULT_GROUP_QUEUE_SIZE,
        )


class RoiSessionTest(unittest.TestCase):
    """ROI entry starts one inspection; exit emits exactly one completion."""

    @staticmethod
    def _adapter():
        adapter = ConveyorCameraAdapterNode.__new__(ConveyorCameraAdapterNode)
        adapter._namespaces = list(DEFAULT_CAMERA_NAMESPACES)
        adapter._roi_min_x_ratio = 0.25
        adapter._roi_max_x_ratio = 0.75
        adapter._roi_exit_patience = 3
        adapter._session = None
        adapter._outside_groups = 0
        adapter._inspection_sequence = 0
        adapter._last_track = None
        adapter._track_gap_ns = 1_500_000_000
        adapter._track_radius_m = 0.12
        adapter.completions = []
        adapter.published = []
        # The node is built without __init__, so rclpy's logger is absent.
        adapter.get_logger = lambda: SimpleNamespace(
            info=lambda *_: None, debug=lambda *_: None, error=lambda *_: None
        )
        adapter._publish_group = lambda stamp, views: (
            adapter.published.append((stamp, len(views))),
            adapter._session.__setitem__(
                "frames_sent", adapter._session["frames_sent"] + len(views)
            ),
        )
        adapter._finish_session = lambda stamp: (
            adapter.completions.append((stamp, adapter._session)),
            setattr(adapter, "_session", None),
            setattr(adapter, "_outside_groups", 0),
        )
        return adapter

    @staticmethod
    def _mask(centre_ratio: float, width: int = 100):
        mask = np.zeros((10, width), dtype=np.uint8)
        centre = int(centre_ratio * width)
        mask[:, max(0, centre - 3) : centre + 3] = 255
        return mask

    def test_centroid_inside_band_is_in_roi(self) -> None:
        adapter = self._adapter()
        self.assertTrue(adapter._mask_in_roi(self._mask(0.50)))
        self.assertTrue(adapter._mask_in_roi(self._mask(0.30)))

    def test_centroid_outside_band_is_not_in_roi(self) -> None:
        adapter = self._adapter()
        self.assertFalse(adapter._mask_in_roi(self._mask(0.05)))
        self.assertFalse(adapter._mask_in_roi(self._mask(0.95)))

    def test_empty_mask_is_not_in_roi(self) -> None:
        adapter = self._adapter()
        self.assertFalse(adapter._mask_in_roi(np.zeros((10, 100), dtype=np.uint8)))

    def test_entry_creates_one_session_reused_across_ticks(self) -> None:
        adapter = self._adapter()
        adapter._begin_session(1_000, [])
        first = adapter._session["inspection_id"]
        self.assertEqual(adapter._session["frames_sent"], 0)
        # A second tick inside the ROI must not start a new inspection.
        self.assertIsNotNone(adapter._session)
        self.assertEqual(adapter._session["inspection_id"], first)

    def test_exit_needs_patience_before_completing(self) -> None:
        adapter = self._adapter()
        adapter._begin_session(1_000, [])
        for _ in range(adapter._roi_exit_patience - 1):
            adapter._outside_groups += 1
            if adapter._outside_groups >= adapter._roi_exit_patience:
                adapter._finish_session(2_000)
        self.assertEqual(adapter.completions, [])

        adapter._outside_groups += 1
        if adapter._outside_groups >= adapter._roi_exit_patience:
            adapter._finish_session(2_000)
        self.assertEqual(len(adapter.completions), 1)
        self.assertIsNone(adapter._session)

    def test_second_apple_gets_a_new_inspection_id(self) -> None:
        adapter = self._adapter()
        adapter._begin_session(1_000, [])
        first = adapter._session["inspection_id"]
        adapter._finish_session(2_000)
        adapter._begin_session(3_000, [])
        self.assertNotEqual(adapter._session["inspection_id"], first)


class ThreeDimensionalRoiTest(unittest.TestCase):
    """All three cameras must test one physical question, not three image ones.

    The old band tested image x for every view. A top camera looking straight
    down shows travel as image y, so for that view image x measured sideways
    wobble instead (measured swing 0.184 against 0.819 on y), and the combined
    verdict was an AND over three different questions.
    """

    @staticmethod
    def _camera_info(fx=600.0, fy=600.0, cx=640.0, cy=360.0):
        return SimpleNamespace(k=[fx, 0.0, cx, 0.0, fy, cy, 0.0, 0.0, 1.0])

    @staticmethod
    def _scene(centre_uv, depth_m):
        mask = np.zeros((720, 1280), dtype=np.uint8)
        u, v = centre_uv
        mask[v - 20 : v + 20, u - 20 : u + 20] = 255
        depth = np.zeros((720, 1280), dtype=np.uint16)
        depth[mask > 0] = int(depth_m * 1000)
        return mask, depth

    def _adapter(self, aim=0.40, radius=0.08):
        adapter = ConveyorCameraAdapterNode.__new__(ConveyorCameraAdapterNode)
        adapter._roi_aim_distance_m = aim
        adapter._roi_radius_m = radius
        adapter._roi_min_x_ratio = 0.25
        adapter._roi_max_x_ratio = 0.75
        return adapter

    def test_apple_on_the_aim_point_is_inside(self) -> None:
        mask, depth = self._scene((640, 360), 0.40)
        self.assertTrue(
            self._adapter()._view_in_roi(mask, depth, self._camera_info())
        )

    def test_apple_too_near_the_camera_is_outside(self) -> None:
        mask, depth = self._scene((640, 360), 0.25)
        self.assertFalse(
            self._adapter()._view_in_roi(mask, depth, self._camera_info())
        )

    def test_apple_offset_sideways_is_outside(self) -> None:
        # 200 px off axis at 0.40 m and fx 600 is 0.13 m, beyond the radius.
        mask, depth = self._scene((840, 360), 0.40)
        self.assertFalse(
            self._adapter()._view_in_roi(mask, depth, self._camera_info())
        )

    def test_travel_along_image_y_is_judged_the_same_as_along_x(self) -> None:
        """The fix: a top view's travel axis must not be treated differently."""
        adapter = self._adapter()
        info = self._camera_info()
        along_x, depth_x = self._scene((640 + 150, 360), 0.40)
        along_y, depth_y = self._scene((640, 360 + 150), 0.40)
        self.assertEqual(
            adapter._view_in_roi(along_x, depth_x, info),
            adapter._view_in_roi(along_y, depth_y, info),
        )

    def test_missing_depth_falls_back_to_the_image_band(self) -> None:
        mask, _ = self._scene((640, 360), 0.40)
        blank = np.zeros((720, 1280), dtype=np.uint16)
        # Centroid is at x=0.5, inside the fallback band.
        self.assertTrue(self._adapter()._view_in_roi(mask, blank, self._camera_info()))

    def test_position_is_none_without_valid_depth(self) -> None:
        mask, _ = self._scene((640, 360), 0.40)
        blank = np.zeros((720, 1280), dtype=np.uint16)
        self.assertIsNone(apple_position_m(mask, blank, self._camera_info()))

    def test_back_projection_matches_the_pinhole_model(self) -> None:
        mask, depth = self._scene((640 + 60, 360), 0.50)
        position = apple_position_m(mask, depth, self._camera_info())
        self.assertIsNotNone(position)
        x, y, z = position
        self.assertAlmostEqual(z, 0.50, places=3)
        self.assertAlmostEqual(x, 60 * 0.50 / 600.0, places=3)
        self.assertAlmostEqual(y, 0.0, places=3)


class AppleTrackerTest(unittest.TestCase):
    """One apple must keep one apple_id even when its session breaks.

    Detection drops out near the ROI edge, which ends the session and opens a
    new one on the same fruit. Minting an id per session turned one apple into
    six inspections in a live run.
    """

    def _adapter(self, gap_ns=1_500_000_000, radius=0.12):
        adapter = ConveyorCameraAdapterNode.__new__(ConveyorCameraAdapterNode)
        adapter._track_gap_ns = gap_ns
        adapter._track_radius_m = radius
        adapter._last_track = None
        adapter.get_logger = lambda: SimpleNamespace(
            info=lambda *_: None, warn=lambda *_: None, debug=lambda *_: None
        )
        return adapter

    def test_same_place_soon_after_reuses_the_id(self) -> None:
        adapter = self._adapter()
        adapter._last_track = {
            "apple_id": "apple-1", "stamp_ns": 1_000_000_000,
            "position": (0.0, 0.0, 0.40),
        }
        resolved = adapter._resolve_apple_id(
            1_400_000_000, (0.01, 0.0, 0.42), "apple-new"
        )
        self.assertEqual(resolved, "apple-1")

    def test_a_long_gap_starts_a_new_apple(self) -> None:
        adapter = self._adapter()
        adapter._last_track = {
            "apple_id": "apple-1", "stamp_ns": 1_000_000_000,
            "position": (0.0, 0.0, 0.40),
        }
        resolved = adapter._resolve_apple_id(
            5_000_000_000, (0.0, 0.0, 0.40), "apple-new"
        )
        self.assertEqual(resolved, "apple-new")

    def test_a_distant_apple_is_a_different_apple(self) -> None:
        adapter = self._adapter()
        adapter._last_track = {
            "apple_id": "apple-1", "stamp_ns": 1_000_000_000,
            "position": (0.0, 0.0, 0.40),
        }
        resolved = adapter._resolve_apple_id(
            1_200_000_000, (0.30, 0.0, 0.40), "apple-new"
        )
        self.assertEqual(resolved, "apple-new")

    def test_without_a_previous_track_the_fallback_is_used(self) -> None:
        adapter = self._adapter()
        self.assertEqual(
            adapter._resolve_apple_id(1_000, (0.0, 0.0, 0.4), "apple-new"),
            "apple-new",
        )

    def test_unknown_position_cannot_claim_an_identity(self) -> None:
        adapter = self._adapter()
        adapter._last_track = {
            "apple_id": "apple-1", "stamp_ns": 1_000,
            "position": (0.0, 0.0, 0.40),
        }
        self.assertEqual(
            adapter._resolve_apple_id(1_100, None, "apple-new"), "apple-new"
        )

    def test_group_position_averages_the_views_that_have_one(self) -> None:
        adapter = self._adapter()
        views = [
            {"position_m": (0.0, 0.0, 0.40)},
            {"position_m": (0.02, 0.0, 0.42)},
            {"position_m": None},
        ]
        x, y, z = adapter._group_position_m(views)
        self.assertAlmostEqual(x, 0.01)
        self.assertAlmostEqual(z, 0.41)

    def test_group_position_is_none_when_no_view_has_depth(self) -> None:
        adapter = self._adapter()
        self.assertIsNone(adapter._group_position_m([{"position_m": None}]))


class RepresentativeInstantsTest(unittest.TestCase):
    """One instant covers about a third of the peel, so keep several spread out.

    The thinning rule has to preserve the spread, not just the count: eight
    consecutive frames show nearly the same pose and would leave most of the
    surface unmeasured.
    """

    @staticmethod
    def _adapter(budget: int = 8):
        adapter = ConveyorCameraAdapterNode.__new__(ConveyorCameraAdapterNode)
        adapter._representative_instants = budget
        return adapter

    @staticmethod
    def _instants(stamps, score=1.0):
        return [
            {"stamp_ns": int(s), "score": (score, 1.0), "views": []} for s in stamps
        ]

    def _feed(self, stamps, budget=8):
        adapter = self._adapter(budget)
        kept = []
        for stamp in stamps:
            kept.append({"stamp_ns": int(stamp), "score": (1.0, 1.0), "views": []})
            adapter._thin_instants(kept)
        return [item["stamp_ns"] for item in kept]

    def test_budget_is_never_exceeded(self) -> None:
        kept = self._feed(range(0, 200_000_000, 1_000_000), budget=8)
        self.assertEqual(len(kept), 8)

    def test_the_two_ends_of_the_transit_survive(self) -> None:
        stamps = list(range(0, 100_000_000, 5_000_000))
        kept = self._feed(stamps, budget=8)
        self.assertEqual(kept[0], stamps[0])
        self.assertEqual(kept[-1], stamps[-1])

    def test_kept_instants_stay_spread_rather_than_bunched(self) -> None:
        """A run of consecutive frames must not collapse onto one moment."""
        stamps = list(range(0, 100_000_000, 1_000_000))
        kept = self._feed(stamps, budget=8)
        span = kept[-1] - kept[0]
        gaps = [b - a for a, b in zip(kept, kept[1:])]
        # No gap should dominate: with even spread each is about span/7.
        self.assertLess(max(gaps), span / 2)
        self.assertGreater(min(gaps), 0)

    def test_below_budget_nothing_is_dropped(self) -> None:
        stamps = [0, 5_000_000, 9_000_000]
        self.assertEqual(self._feed(stamps, budget=8), stamps)

    def test_thinning_removes_the_most_redundant_instant(self) -> None:
        adapter = self._adapter(budget=3)
        # 10 and 11 are near-duplicates; one of them is the redundant one.
        kept = self._instants([0, 10, 11, 100])
        adapter._thin_instants(kept)
        stamps = [item["stamp_ns"] for item in kept]
        self.assertEqual(len(stamps), 3)
        self.assertIn(0, stamps)
        self.assertIn(100, stamps)
        self.assertTrue(10 in stamps or 11 in stamps)


class FrameIndexAcrossInstantsTest(unittest.TestCase):
    """frame_index must stay unique once a session carries several instants."""

    def test_indices_do_not_collide_between_instants(self) -> None:
        cameras = 3
        seen = set()
        for ordinal in range(REPRESENTATIVE_INSTANTS):
            for view_index in range(cameras):
                index = ordinal * cameras + view_index
                self.assertNotIn(index, seen)
                seen.add(index)
        self.assertEqual(len(seen), REPRESENTATIVE_INSTANTS * cameras)
        self.assertEqual(max(seen) + 1, MAX_REPRESENTATIVE_FRAMES)

    def test_the_frame_budget_matches_cameras_times_instants(self) -> None:
        self.assertEqual(REPRESENTATIVE_INSTANTS * 3, MAX_REPRESENTATIVE_FRAMES)


class CropGeometryTest(unittest.TestCase):
    """Cropping must shrink the payload without moving the projection."""

    FX = FY = 640.0
    CX = CY = 360.0
    WIDTH, HEIGHT = 1280, 720

    def _camera_info(self, as_numpy: bool):
        k = [self.FX, 0.0, self.CX, 0.0, self.FY, self.CY, 0.0, 0.0, 1.0]
        p = [self.FX, 0.0, self.CX, 0.0, 0.0, self.FY, self.CY, 0.0,
             0.0, 0.0, 1.0, 0.0]
        return SimpleNamespace(
            width=self.WIDTH,
            height=self.HEIGHT,
            # rclpy hands over fixed-size float64 arrays, not lists.
            k=np.array(k, dtype=np.float64) if as_numpy else k,
            p=np.array(p, dtype=np.float64) if as_numpy else p,
            roi=SimpleNamespace(
                x_offset=0, y_offset=0, width=0, height=0, do_rectify=False
            ),
        )

    @staticmethod
    def _mask(cx: int = 700, cy: int = 300, radius: int = 60):
        import cv2

        mask = np.zeros((720, 1280), dtype=np.uint8)
        cv2.circle(mask, (cx, cy), radius, 255, -1)
        return mask

    def test_box_covers_mask_with_margin(self) -> None:
        box = apple_crop_box(self._mask(), 48)
        x0, y0, x1, y1 = box
        self.assertEqual((x1 - x0, y1 - y0), (217, 217))
        self.assertLessEqual(x0, 700 - 60)
        self.assertGreaterEqual(x1, 700 + 60)

    def test_box_is_clamped_to_the_frame(self) -> None:
        box = apple_crop_box(self._mask(cx=20, cy=15, radius=10), 48)
        x0, y0, _x1, _y1 = box
        self.assertEqual((x0, y0), (0, 0))

    def test_empty_mask_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            apple_crop_box(np.zeros((720, 1280), dtype=np.uint8), 48)

    def test_numpy_intrinsics_are_shifted_not_rebuilt(self) -> None:
        """Regression: rebuilding via type(k)(values) reads them as a shape."""
        info = self._camera_info(as_numpy=True)
        box = apple_crop_box(self._mask(), 48)
        cropped = cropped_camera_info(info, box)
        x0, y0, x1, y1 = box
        self.assertAlmostEqual(float(cropped.k[2]), self.CX - x0)
        self.assertAlmostEqual(float(cropped.k[5]), self.CY - y0)
        self.assertAlmostEqual(float(cropped.p[2]), self.CX - x0)
        self.assertAlmostEqual(float(cropped.p[6]), self.CY - y0)
        self.assertEqual((cropped.width, cropped.height), (x1 - x0, y1 - y0))

    def test_source_camera_info_is_not_mutated(self) -> None:
        info = self._camera_info(as_numpy=True)
        cropped_camera_info(info, apple_crop_box(self._mask(), 48))
        self.assertAlmostEqual(float(info.k[2]), self.CX)
        self.assertAlmostEqual(float(info.p[2]), self.CX)

    def test_back_projection_is_unchanged_by_the_crop(self) -> None:
        info = self._camera_info(as_numpy=True)
        box = apple_crop_box(self._mask(), 48)
        cropped = cropped_camera_info(info, box)
        x0, y0, _x1, _y1 = box
        depth = 0.65
        for pixel_x, pixel_y in ((700, 300), (660, 260), (745, 352)):
            full_x = (pixel_x - self.CX) * depth / self.FX
            full_y = (pixel_y - self.CY) * depth / self.FY
            crop_x = (
                (pixel_x - x0) - float(cropped.p[2])
            ) * depth / float(cropped.p[0])
            crop_y = (
                (pixel_y - y0) - float(cropped.p[6])
            ) * depth / float(cropped.p[5])
            self.assertAlmostEqual(full_x, crop_x, places=9)
            self.assertAlmostEqual(full_y, crop_y, places=9)

    def test_roi_records_the_original_window(self) -> None:
        info = self._camera_info(as_numpy=True)
        box = apple_crop_box(self._mask(), 48)
        cropped = cropped_camera_info(info, box)
        x0, y0, x1, y1 = box
        self.assertEqual(
            (
                cropped.roi.x_offset,
                cropped.roi.y_offset,
                cropped.roi.width,
                cropped.roi.height,
            ),
            (x0, y0, x1 - x0, y1 - y0),
        )


class IgnoreMaskTest(unittest.TestCase):
    """Surface whose colour cannot be judged must leave the ratio's denominator.

    Leaving deep shadow in it measured a fully red apple at 78 percent, because
    roughly 15 percent of the surface was too dark to carry a hue.
    """

    @staticmethod
    def _scene():
        import cv2

        bgr = np.zeros((120, 120, 3), dtype=np.uint8)
        mask = np.zeros((120, 120), dtype=np.uint8)
        cv2.circle(mask, (60, 60), 50, 255, -1)
        bgr[mask > 0] = (35, 45, 200)
        cv2.circle(bgr, (45, 40), 8, (250, 250, 252), -1)
        cv2.circle(bgr, (80, 85), 12, (8, 6, 10), -1)
        return bgr, mask

    def test_specular_highlight_is_ignored(self) -> None:
        bgr, mask = self._scene()
        self.assertTrue(unmeasurable_surface_mask(bgr, mask)[40, 45] > 0)

    def test_deep_shadow_is_ignored(self) -> None:
        bgr, mask = self._scene()
        self.assertTrue(unmeasurable_surface_mask(bgr, mask)[85, 80] > 0)

    def test_normal_peel_is_kept(self) -> None:
        bgr, mask = self._scene()
        self.assertEqual(int(unmeasurable_surface_mask(bgr, mask)[60, 20]), 0)

    def test_nothing_outside_the_apple_is_marked(self) -> None:
        bgr, mask = self._scene()
        ignore = unmeasurable_surface_mask(bgr, mask)
        self.assertEqual(int(np.count_nonzero(ignore[mask == 0])), 0)

    def test_silhouette_band_is_ignored(self) -> None:
        """The rim blends apple with background, so its ratios are not skin.

        Live measurement: the band is 4-9 percent of the surface but carries
        35-47 percent of the pixels that fail the red test.
        """
        bgr, mask = self._scene()
        ignore = unmeasurable_surface_mask(bgr, mask)
        # (60, 10) sits on the left rim: 50px from centre (60, 60).
        self.assertTrue(ignore[60, 10] > 0)

    def test_band_thickness_matches_the_configured_erosion(self) -> None:
        import cv2

        bgr, mask = self._scene()
        ignore = unmeasurable_surface_mask(bgr, mask) > 0
        inside = mask > 0
        eroded = cv2.erode(
            inside.astype(np.uint8),
            np.ones((3, 3), np.uint8),
            iterations=IGNORE_BOUNDARY_ERODE_PX,
        ) > 0
        # Every rim pixel is ignored, and the interior keeps its own verdict.
        self.assertTrue(bool((ignore | ~inside)[inside & ~eroded].all()))
        self.assertEqual(int(np.count_nonzero(ignore[mask == 0])), 0)


class ViewValidationTest(unittest.TestCase):
    @staticmethod
    def _message(frame_id: str, *, sec: int = 3, width: int = 8, height: int = 4):
        return SimpleNamespace(
            header=SimpleNamespace(
                stamp=SimpleNamespace(sec=sec, nanosec=0),
                frame_id=frame_id,
            ),
            width=width,
            height=height,
        )

    def test_accepts_each_known_camera_frame(self) -> None:
        for frame_id in QUALITY_CAMERA_OPTICAL_FRAMES:
            message = self._message(frame_id)
            ConveyorCameraAdapterNode._validate_view(message, message, message)

    def test_rejects_unknown_camera_frame(self) -> None:
        message = self._message("some_other_frame")
        with self.assertRaises(ValueError):
            ConveyorCameraAdapterNode._validate_view(message, message, message)

    def test_rejects_mismatched_stamps(self) -> None:
        rgb = self._message(QUALITY_CAMERA_OPTICAL_FRAMES[0], sec=3)
        depth = self._message(QUALITY_CAMERA_OPTICAL_FRAMES[0], sec=4)
        with self.assertRaises(ValueError):
            ConveyorCameraAdapterNode._validate_view(rgb, depth, rgb)

    def test_rejects_mismatched_dimensions(self) -> None:
        rgb = self._message(QUALITY_CAMERA_OPTICAL_FRAMES[0])
        depth = self._message(QUALITY_CAMERA_OPTICAL_FRAMES[0], width=16)
        with self.assertRaises(ValueError):
            ConveyorCameraAdapterNode._validate_view(rgb, depth, rgb)


if __name__ == "__main__":
    unittest.main()
