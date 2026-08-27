"""GPU PC 1 conveyor landing and checkpoint lifecycle tracking."""

from dataclasses import dataclass
from typing import Callable, Dict, Optional, Tuple

import numpy as np


PLACE_IDS = {
    "robot_01": "CONVEYOR_PLACE_01_LANDING",
    "robot_02": "CONVEYOR_PLACE_02_LANDING",
}
INSPECTION_CHECKPOINT_ID = "CONVEYOR_INSPECTION_ROI"


@dataclass(frozen=True)
class ConveyorBounds:
    minimum: np.ndarray
    maximum: np.ndarray
    travel_axis: int

    def __post_init__(self):
        minimum = np.asarray(self.minimum, dtype=float)
        maximum = np.asarray(self.maximum, dtype=float)
        if minimum.shape != (3,) or maximum.shape != (3,):
            raise ValueError("conveyor bounds must contain three coordinates")
        if not np.all(np.isfinite(minimum)) or not np.all(np.isfinite(maximum)):
            raise ValueError("conveyor bounds must be finite")
        if np.any(maximum <= minimum):
            raise ValueError("conveyor maximum must be greater than minimum")
        if int(self.travel_axis) not in (0, 1):
            raise ValueError("travel_axis must be world X or Y")
        object.__setattr__(self, "minimum", minimum)
        object.__setattr__(self, "maximum", maximum)
        object.__setattr__(self, "travel_axis", int(self.travel_axis))

    @property
    def side_axis(self) -> int:
        return 1 - self.travel_axis

    @property
    def length_midpoint(self) -> float:
        """Halfway point used to keep the two Place zones physically separate."""
        return 0.5 * (
            self.minimum[self.travel_axis] + self.maximum[self.travel_axis]
        )

    def place_zone_bounds(self, robot_id: str) -> Tuple[float, float]:
        if robot_id not in PLACE_IDS:
            raise ValueError(f"unknown robot Place zone: {robot_id}")
        midpoint = self.length_midpoint
        if robot_id == "robot_01":
            return float(self.minimum[self.travel_axis]), float(midpoint)
        return float(midpoint), float(self.maximum[self.travel_axis])

    def in_landing_region(self, robot_id: str, center: np.ndarray) -> bool:
        center = np.asarray(center, dtype=float)
        if center.shape != (3,) or not np.all(np.isfinite(center)):
            return False
        if robot_id not in PLACE_IDS:
            return False
        side_center = 0.5 * (
            self.minimum[self.side_axis] + self.maximum[self.side_axis]
        )
        side_half_width = 0.20 * (
            self.maximum[self.side_axis] - self.minimum[self.side_axis]
        )
        if abs(center[self.side_axis] - side_center) > side_half_width:
            return False
        length_midpoint = self.length_midpoint
        if robot_id == "robot_01":
            return self.minimum[self.travel_axis] <= center[self.travel_axis] < length_midpoint
        return length_midpoint <= center[self.travel_axis] <= self.maximum[self.travel_axis]

    def in_inspection_region(
        self, center: np.ndarray, length_fraction: Tuple[float, float]
    ) -> bool:
        start, end = (float(value) for value in length_fraction)
        if not 0.0 <= start < end <= 1.0:
            raise ValueError("inspection ROI fractions must satisfy 0 <= start < end <= 1")
        center = np.asarray(center, dtype=float)
        if center.shape != (3,) or not np.all(np.isfinite(center)):
            return False
        length = self.maximum[self.travel_axis] - self.minimum[self.travel_axis]
        low = self.minimum[self.travel_axis] + start * length
        high = self.minimum[self.travel_axis] + end * length
        return bool(
            low <= center[self.travel_axis] <= high
            and self.minimum[self.side_axis]
            <= center[self.side_axis]
            <= self.maximum[self.side_axis]
        )


@dataclass(frozen=True)
class LandingConfig:
    stable_duration_s: float = 0.3
    timeout_s: float = 2.0
    maximum_vertical_speed_mps: float = 0.05
    belt_speed_tolerance_mps: float = 0.10

    def __post_init__(self):
        if self.stable_duration_s <= 0.0 or self.timeout_s <= 0.0:
            raise ValueError("landing durations must be greater than zero")
        if self.stable_duration_s >= self.timeout_s:
            raise ValueError("landing stable duration must be shorter than timeout")
        if self.maximum_vertical_speed_mps < 0.0 or self.belt_speed_tolerance_mps < 0.0:
            raise ValueError("landing velocity tolerances cannot be negative")


@dataclass(frozen=True)
class LandingObservation:
    center: np.ndarray
    linear_velocity: np.ndarray
    belt_contact: bool
    gripper_attached: bool


@dataclass(frozen=True)
class LandingResult:
    state: str
    robot_id: str
    reservation_id: str
    apple_id: str
    message: str


class LandingTracker:
    WAITING = "WAITING"
    CONFIRMED = "CONFIRMED"
    TIMEOUT = "TIMEOUT"

    def __init__(
        self,
        bounds: ConveyorBounds,
        belt_speed_mps: float,
        config: LandingConfig = LandingConfig(),
    ):
        self.bounds = bounds
        self.belt_speed_mps = abs(float(belt_speed_mps))
        self.config = config
        self.session = None
        self.stable_since_s: Optional[float] = None
        self.terminal = False

    def start(
        self,
        robot_id: str,
        reservation_id: str,
        apple_id: str,
        apple_prim_path: str,
        now_s: float,
    ) -> None:
        values = tuple(str(value).strip() for value in (
            robot_id, reservation_id, apple_id, apple_prim_path
        ))
        if not all(values) or values[0] not in PLACE_IDS:
            raise ValueError("landing session identifiers are invalid")
        self.session = (*values, float(now_s))
        self.stable_since_s = None
        self.terminal = False

    @property
    def apple_prim_path(self) -> str:
        return "" if self.session is None else self.session[3]

    def reset(self) -> None:
        self.session = None
        self.stable_since_s = None
        self.terminal = False

    def update(self, observation: LandingObservation, now_s: float) -> Optional[LandingResult]:
        if self.session is None or self.terminal:
            return None
        robot_id, reservation_id, apple_id, _prim_path, started_s = self.session
        now_s = float(now_s)
        if now_s - started_s >= self.config.timeout_s:
            self.terminal = True
            return LandingResult(
                self.TIMEOUT,
                robot_id,
                reservation_id,
                apple_id,
                "landing was not confirmed before simulation-time timeout",
            )
        velocity = np.asarray(observation.linear_velocity, dtype=float)
        speed_valid = velocity.shape == (3,) and np.all(np.isfinite(velocity))
        stable = bool(
            speed_valid
            and observation.belt_contact
            and not observation.gripper_attached
            and self.bounds.in_landing_region(robot_id, observation.center)
            and abs(velocity[2]) <= self.config.maximum_vertical_speed_mps
            and abs(abs(velocity[self.bounds.travel_axis]) - self.belt_speed_mps)
            <= self.config.belt_speed_tolerance_mps
        )
        if not stable:
            self.stable_since_s = None
            return None
        if self.stable_since_s is None:
            self.stable_since_s = now_s
            return None
        if now_s - self.stable_since_s < self.config.stable_duration_s:
            return None
        self.terminal = True
        return LandingResult(
            self.CONFIRMED,
            robot_id,
            reservation_id,
            apple_id,
            "belt contact and landing stability confirmed",
        )


@dataclass(frozen=True)
class CheckpointRecord:
    apple_id: str
    checkpoint_id: str
    entered: bool


class InspectionCheckpointTracker:
    """Emits one ENTER/EXIT edge per apple for the single inspection ROI."""

    def __init__(
        self,
        bounds: ConveyorBounds,
        length_fraction: Tuple[float, float],
        publish: Callable[[CheckpointRecord], None],
    ):
        self.bounds = bounds
        self.length_fraction = tuple(float(value) for value in length_fraction)
        self.bounds.in_inspection_region(self.bounds.minimum, self.length_fraction)
        self.publish = publish
        self.apple_paths: Dict[str, str] = {}
        self.inside = set()

    def bind_apple(self, apple_id: str, prim_path: str) -> None:
        apple_id = str(apple_id).strip()
        prim_path = str(prim_path).strip()
        if not apple_id or not prim_path:
            raise ValueError("checkpoint apple binding cannot be empty")
        known_path = self.apple_paths.get(apple_id)
        if known_path is not None and known_path != prim_path:
            raise ValueError("apple_id is already bound to a different prim")
        if prim_path in self.apple_paths.values() and known_path != prim_path:
            raise ValueError("apple prim is already bound to a different apple_id")
        self.apple_paths[apple_id] = prim_path

    def update(self, centers_by_prim: Dict[str, np.ndarray]) -> None:
        for apple_id, prim_path in self.apple_paths.items():
            center = centers_by_prim.get(prim_path)
            if center is None:
                continue
            key = (apple_id, INSPECTION_CHECKPOINT_ID)
            now_inside = self.bounds.in_inspection_region(center, self.length_fraction)
            was_inside = key in self.inside
            if now_inside == was_inside:
                continue
            if now_inside:
                self.inside.add(key)
            else:
                self.inside.remove(key)
            self.publish(
                CheckpointRecord(apple_id, INSPECTION_CHECKPOINT_ID, now_inside)
            )

    def reset(self) -> None:
        self.apple_paths.clear()
        self.inside.clear()
