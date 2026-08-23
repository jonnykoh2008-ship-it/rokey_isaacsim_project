"""Inspection-frame contract validation and per-apple session storage."""

from __future__ import annotations

from dataclasses import dataclass, field


UINT16_MAX = 65_535
MAX_REPRESENTATIVE_FRAMES = 6
RESULT_DEADLINE_NS = 500_000_000
QUALITY_CAMERA_OPTICAL_FRAME = "quality_camera_optical_frame"


class InspectionContractError(ValueError):
    """Base error for an invalid or inconsistent inspection-frame contract."""


class InspectionIdentityMismatch(InspectionContractError):
    """Raised when one inspection ID is associated with different apple IDs."""


class TotalFramesMismatch(InspectionContractError):
    """Raised when frames in one inspection disagree about total_frames."""


class DuplicateFrameConflict(InspectionContractError):
    """Raised when one frame index is reused with different frame contents."""


@dataclass(frozen=True)
class InspectionCompletion:
    """Transport-neutral ROI-exit event using Isaac simulation time."""

    inspection_id: str
    apple_id: str
    total_frames: int
    roi_exit_time_ns: int
    frame_id: str

    def __post_init__(self) -> None:
        if not self.inspection_id.strip() or not self.apple_id.strip():
            raise InspectionContractError("completion IDs must be non-empty")
        if not 1 <= self.total_frames <= MAX_REPRESENTATIVE_FRAMES:
            raise InspectionContractError(
                f"completion total_frames must be between 1 and {MAX_REPRESENTATIVE_FRAMES}"
            )
        if self.roi_exit_time_ns < 0:
            raise InspectionContractError("roi_exit_time_ns must be non-negative")
        if self.frame_id != QUALITY_CAMERA_OPTICAL_FRAME:
            raise InspectionContractError(
                f"completion frame_id must be {QUALITY_CAMERA_OPTICAL_FRAME!r}")

    @property
    def deadline_time_ns(self) -> int:
        return self.roi_exit_time_ns + RESULT_DEADLINE_NS


@dataclass(frozen=True)
class InspectionFrame:
    """One synchronized, zero-based RGB-D representative frame."""

    inspection_id: str
    apple_id: str
    frame_index: int
    total_frames: int
    image_data: bytes
    image_format: str
    apple_mask_data: bytes
    apple_mask_format: str
    depth_data: bytes
    depth_format: str
    camera_width: int
    camera_height: int
    camera_k: tuple[float, ...]
    camera_p: tuple[float, ...]
    stamp_ns: int
    frame_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.inspection_id, str) or not self.inspection_id.strip():
            raise InspectionContractError("inspection_id must be a non-empty string")
        if not isinstance(self.apple_id, str) or not self.apple_id.strip():
            raise InspectionContractError("apple_id must be a non-empty string")
        if isinstance(self.total_frames, bool) or not isinstance(self.total_frames, int):
            raise InspectionContractError("total_frames must be an integer")
        if not 1 <= self.total_frames <= MAX_REPRESENTATIVE_FRAMES:
            raise InspectionContractError(
                f"total_frames must be between 1 and {MAX_REPRESENTATIVE_FRAMES}"
            )
        if isinstance(self.frame_index, bool) or not isinstance(self.frame_index, int):
            raise InspectionContractError("frame_index must be an integer")
        if not 0 <= self.frame_index <= UINT16_MAX:
            raise InspectionContractError("frame_index must fit in uint16")
        if self.frame_index >= self.total_frames:
            raise InspectionContractError("frame_index must be less than total_frames")
        for name, value in (
            ("image_data", self.image_data),
            ("apple_mask_data", self.apple_mask_data),
            ("depth_data", self.depth_data),
        ):
            if not isinstance(value, bytes) or not value:
                raise InspectionContractError(f"{name} must be non-empty bytes")
        for name, value in (
            ("image_format", self.image_format),
            ("apple_mask_format", self.apple_mask_format),
            ("depth_format", self.depth_format),
            ("frame_id", self.frame_id),
        ):
            if not isinstance(value, str) or not value.strip():
                raise InspectionContractError(f"{name} must be a non-empty string")
        if self.frame_id != QUALITY_CAMERA_OPTICAL_FRAME:
            raise InspectionContractError(
                f"frame_id must be {QUALITY_CAMERA_OPTICAL_FRAME!r}")
        if self.camera_width <= 0 or self.camera_height <= 0:
            raise InspectionContractError("CameraInfo width and height must be positive")
        if len(self.camera_k) != 9 or len(self.camera_p) != 12:
            raise InspectionContractError("CameraInfo K and P matrices have invalid lengths")
        if float(self.camera_k[0]) <= 0.0 or float(self.camera_k[4]) <= 0.0:
            raise InspectionContractError("CameraInfo is uncalibrated")
        if self.stamp_ns < 0:
            raise InspectionContractError("frame stamp must be non-negative")


@dataclass
class InspectionSession:
    """Collect frames that belong to one inspection and one apple."""

    inspection_id: str
    apple_id: str
    total_frames: int
    _frames: dict[int, InspectionFrame] = field(default_factory=dict, init=False, repr=False)
    _completion: InspectionCompletion | None = field(default=None, init=False, repr=False)

    @classmethod
    def from_frame(cls, frame: InspectionFrame) -> "InspectionSession":
        session = cls(frame.inspection_id, frame.apple_id, frame.total_frames)
        session.add(frame)
        return session

    def add(self, frame: InspectionFrame) -> bool:
        if frame.inspection_id != self.inspection_id or frame.apple_id != self.apple_id:
            raise InspectionIdentityMismatch(
                "inspection_id and apple_id must remain constant within a session"
            )
        if frame.total_frames != self.total_frames:
            raise TotalFramesMismatch(
                f"total_frames changed from {self.total_frames} to {frame.total_frames}"
            )
        existing = self._frames.get(frame.frame_index)
        if existing is not None:
            if existing == frame:
                return False
            raise DuplicateFrameConflict(
                f"frame_index {frame.frame_index} was received with different contents"
            )
        if len(self._frames) >= self.total_frames:
            raise InspectionContractError(
                "received more unique frames than the declared total_frames"
            )
        self._frames[frame.frame_index] = frame
        return True

    def mark_completed(self, completion: InspectionCompletion) -> bool:
        if (
            completion.inspection_id != self.inspection_id
            or completion.apple_id != self.apple_id
        ):
            raise InspectionIdentityMismatch(
                "completion inspection_id and apple_id must match the session"
            )
        if completion.total_frames != self.total_frames:
            raise TotalFramesMismatch(
                f"completion total_frames {completion.total_frames} does not match {self.total_frames}"
            )
        if self._completion is not None:
            if self._completion == completion:
                return False
            raise InspectionContractError("inspection received conflicting completion events")
        self._completion = completion
        return True

    @property
    def completion(self) -> InspectionCompletion | None:
        return self._completion

    def deadline_reached(self, simulation_time_ns: int) -> bool:
        return (
            self._completion is not None
            and simulation_time_ns >= self._completion.deadline_time_ns
        )

    @property
    def received_count(self) -> int:
        return len(self._frames)

    @property
    def has_all_declared_frames(self) -> bool:
        return self.received_count == self.total_frames

    @property
    def frame_indices(self) -> tuple[int, ...]:
        return tuple(sorted(self._frames))

    @property
    def ordered_frames(self) -> tuple[InspectionFrame, ...]:
        return tuple(self._frames[index] for index in self.frame_indices)


@dataclass(frozen=True)
class FrameAcceptance:
    session: InspectionSession
    is_new_frame: bool


class InspectionStore:
    """Own active inspection sessions, keyed by inspection_id."""

    def __init__(self) -> None:
        self._sessions: dict[str, InspectionSession] = {}

    def accept(self, frame: InspectionFrame) -> FrameAcceptance:
        session = self._sessions.get(frame.inspection_id)
        if session is None:
            session = InspectionSession.from_frame(frame)
            self._sessions[frame.inspection_id] = session
            return FrameAcceptance(session, True)
        return FrameAcceptance(session, session.add(frame))

    def complete(self, completion: InspectionCompletion) -> InspectionSession:
        session = self._sessions.get(completion.inspection_id)
        if session is None:
            session = InspectionSession(
                completion.inspection_id,
                completion.apple_id,
                completion.total_frames,
            )
            self._sessions[completion.inspection_id] = session
        session.mark_completed(completion)
        return session

    def get(self, inspection_id: str) -> InspectionSession | None:
        return self._sessions.get(inspection_id)

    @property
    def sessions(self) -> tuple[InspectionSession, ...]:
        return tuple(self._sessions.values())

    def pop(self, inspection_id: str) -> InspectionSession | None:
        return self._sessions.pop(inspection_id, None)

    def __len__(self) -> int:
        return len(self._sessions)
