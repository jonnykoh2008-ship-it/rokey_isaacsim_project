"""Inspection-frame contract validation and per-apple session storage.

This module deliberately contains no ROS 2, image-decoding, timeout, or model
policy.  Those concerns depend on the open decisions documented in
``docs/open_questions_gpu_pc2.md``.
"""

from __future__ import annotations

from dataclasses import dataclass, field


UINT16_MAX = 65_535
MAX_REPRESENTATIVE_FRAMES = 6
RESULT_DEADLINE_NS = 500_000_000


class InspectionContractError(ValueError):
    """Base error for an invalid or inconsistent inspection-frame contract."""


class InspectionIdentityMismatch(InspectionContractError):
    """Raised when one inspection ID is associated with different apple IDs."""


class TotalFramesMismatch(InspectionContractError):
    """Raised when frames in one inspection disagree about ``total_frames``."""


class DuplicateFrameConflict(InspectionContractError):
    """Raised when one frame index is reused with different frame contents."""


@dataclass(frozen=True)
class InspectionCompletion:
    """Transport-neutral ROI-exit event using Isaac Sim time in nanoseconds."""

    inspection_id: str
    apple_id: str
    total_frames: int
    roi_exit_time_ns: int

    def __post_init__(self) -> None:
        if not self.inspection_id.strip() or not self.apple_id.strip():
            raise InspectionContractError("completion IDs must be non-empty")
        if not 1 <= self.total_frames <= MAX_REPRESENTATIVE_FRAMES:
            raise InspectionContractError(
                f"completion total_frames must be between 1 and {MAX_REPRESENTATIVE_FRAMES}"
            )
        if self.roi_exit_time_ns < 0:
            raise InspectionContractError("roi_exit_time_ns must be non-negative")

    @property
    def deadline_time_ns(self) -> int:
        return self.roi_exit_time_ns + RESULT_DEADLINE_NS


@dataclass(frozen=True)
class InspectionFrame:
    """Transport-neutral representation of one ``InspectionImage`` message.

    ``frame_index`` is validated only as an unsigned 16-bit value.  The project
    specification does not yet state whether frame numbering is zero- or
    one-based, so this layer must not impose either convention.
    """

    inspection_id: str
    apple_id: str
    frame_index: int
    total_frames: int
    image_data: bytes
    image_format: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.inspection_id, str) or not self.inspection_id.strip():
            raise InspectionContractError("inspection_id must be a non-empty string")
        if not isinstance(self.apple_id, str) or not self.apple_id.strip():
            raise InspectionContractError("apple_id must be a non-empty string")
        if isinstance(self.frame_index, bool) or not isinstance(self.frame_index, int):
            raise InspectionContractError("frame_index must be an integer")
        if not 0 <= self.frame_index <= UINT16_MAX:
            raise InspectionContractError("frame_index must fit in uint16")
        if isinstance(self.total_frames, bool) or not isinstance(self.total_frames, int):
            raise InspectionContractError("total_frames must be an integer")
        if not 1 <= self.total_frames <= MAX_REPRESENTATIVE_FRAMES:
            raise InspectionContractError(
                f"total_frames must be between 1 and {MAX_REPRESENTATIVE_FRAMES}"
            )
        if not isinstance(self.image_data, bytes) or not self.image_data:
            raise InspectionContractError("image_data must be non-empty bytes")
        if not isinstance(self.image_format, str):
            raise InspectionContractError("image_format must be a string")


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
        """Add a frame and return ``True`` when it is new.

        An identical duplicate is idempotent and returns ``False``.  Reusing an
        index with different contents is a contract error so callers can choose
        the eventual ROS status after the relevant policy is approved.
        """

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
        """Attach the explicit ROI-exit event; identical duplicates are idempotent."""

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
        return self._completion is not None and simulation_time_ns >= self._completion.deadline_time_ns

    @property
    def received_count(self) -> int:
        return len(self._frames)

    @property
    def has_all_declared_frames(self) -> bool:
        """Whether the number of unique frames equals ``total_frames``.

        This is a transport fact, not an ROI-exit or deadline decision.
        """

        return self.received_count == self.total_frames

    @property
    def frame_indices(self) -> tuple[int, ...]:
        return tuple(sorted(self._frames))

    @property
    def ordered_frames(self) -> tuple[InspectionFrame, ...]:
        return tuple(self._frames[index] for index in self.frame_indices)


@dataclass(frozen=True)
class FrameAcceptance:
    """Result of accepting one frame into the inspection store."""

    session: InspectionSession
    is_new_frame: bool


class InspectionStore:
    """Own active inspection sessions, keyed by ``inspection_id``."""

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
        """Record ROI exit even if it arrives before the first image frame."""

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

    def pop(self, inspection_id: str) -> InspectionSession | None:
        """Remove a session after a higher layer has finalized its lifecycle."""

        return self._sessions.pop(inspection_id, None)

    def __len__(self) -> int:
        return len(self._sessions)
