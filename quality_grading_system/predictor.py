"""Replaceable inference boundary for GPU PC 2 quality models.

The model architecture and output contract are still TBD.  A generic protocol
keeps frame collection testable without selecting a temporary model or output
schema.
"""

from __future__ import annotations

import io
from dataclasses import dataclass
from pathlib import Path
from typing import Generic, Protocol, TypeVar, runtime_checkable

from apple_quality_dataset import TARGET_NAMES, letterbox_rgb
from inspection_session import InspectionFrame, InspectionSession
from quality_rules import FrameMeasurements


PredictionT = TypeVar("PredictionT")


class PredictorNotConfigured(RuntimeError):
    """Raised when runtime inference is requested without an approved model."""


class IncompleteInspectionError(ValueError):
    """Raised when batch inference is requested before all declared frames arrive."""


@runtime_checkable
class FramePredictor(Protocol[PredictionT]):
    """Protocol implemented later by the approved quality model adapter."""

    def predict(self, frame: InspectionFrame) -> PredictionT:
        """Return one model-specific prediction for ``frame``."""


@dataclass(frozen=True)
class IndexedPrediction(Generic[PredictionT]):
    """Associate an opaque prediction with its original frame index."""

    frame_index: int
    value: PredictionT


class UnconfiguredPredictor:
    """Safe runtime default that never fabricates a quality prediction."""

    def predict(self, frame: InspectionFrame) -> None:
        del frame
        raise PredictorNotConfigured("no approved quality model is configured")


def create_measurement_model():
    """Create the small multi-head network shared by training and inference."""

    try:
        import torch
        from torch import nn
    except ImportError as exc:
        raise PredictorNotConfigured("PyTorch is required for the training checkpoint backend") from exc

    class MeasurementNet(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            layers = []
            channels = (3, 16, 32, 64, 96, 128)
            for input_channels, output_channels in zip(channels, channels[1:]):
                layers.extend(
                    [
                        nn.Conv2d(input_channels, output_channels, 3, stride=2, padding=1),
                        nn.BatchNorm2d(output_channels),
                        nn.SiLU(inplace=True),
                    ]
                )
            self.features = nn.Sequential(*layers, nn.AdaptiveAvgPool2d(1))
            self.head = nn.Linear(channels[-1], len(TARGET_NAMES) * 2)

        def forward(self, images):
            raw = self.head(self.features(images).flatten(1))
            raw_values = raw[:, : len(TARGET_NAMES)]
            values = torch.stack(
                (
                    torch.sigmoid(raw_values[:, 0]),
                    torch.sigmoid(raw_values[:, 1]) * 10.0,
                    torch.sigmoid(raw_values[:, 2]),
                ),
                dim=1,
            )
            confidences = torch.sigmoid(raw[:, len(TARGET_NAMES) :])
            return values, confidences

    return MeasurementNet()


def _image_bytes_to_tensor(image_data: bytes, image_size: int):
    try:
        import numpy as np
        import torch
        from PIL import Image
    except ImportError as exc:
        raise PredictorNotConfigured("NumPy, Pillow and PyTorch are required for image inference") from exc

    try:
        image = letterbox_rgb(Image.open(io.BytesIO(image_data)), image_size)
    except Exception as exc:
        raise ValueError("InspectionImage does not contain a decodable compressed RGB image") from exc
    pixels = np.asarray(image, dtype=np.float32) / 255.0
    return torch.from_numpy(pixels).permute(2, 0, 1).unsqueeze(0).contiguous()


class TorchMeasurementPredictor:
    """Development backend for checkpoints produced by ``train_quality_model``."""

    def __init__(self, checkpoint_path: str | Path, *, device: str = "auto") -> None:
        try:
            import torch
        except ImportError as exc:
            raise PredictorNotConfigured("PyTorch is not installed") from exc

        checkpoint_path = Path(checkpoint_path).expanduser().resolve()
        if not checkpoint_path.is_file():
            raise PredictorNotConfigured(f"model checkpoint not found: {checkpoint_path}")
        selected_device = (
            "cuda" if device == "auto" and torch.cuda.is_available() else
            "cpu" if device == "auto" else device
        )
        checkpoint = torch.load(checkpoint_path, map_location=selected_device, weights_only=False)
        self._model = create_measurement_model()
        self._model.load_state_dict(checkpoint["model_state"])
        self._model.to(selected_device).eval()
        self._device = selected_device
        self._image_size = int(checkpoint.get("image_size", 640))
        self._trained_targets = frozenset(checkpoint.get("trained_targets", []))

    def predict(self, frame: InspectionFrame) -> FrameMeasurements:
        import torch

        tensor = _image_bytes_to_tensor(frame.image_data, self._image_size).to(self._device)
        with torch.inference_mode():
            values, confidences = self._model(tensor)
        raw_values = values[0].detach().cpu().tolist()
        raw_confidences = confidences[0].detach().cpu().tolist()
        available = {
            name: (raw_values[index], raw_confidences[index])
            for index, name in enumerate(TARGET_NAMES)
            if name in self._trained_targets
        }
        return FrameMeasurements(
            color_ratio=_value(available, "color_ratio"),
            diameter_mm=None,
            damage_area_cm2=_value(available, "damage_area_cm2"),
            severe_defect=(
                _value(available, "severe_defect") >= 0.5
                if _value(available, "severe_defect") is not None
                else None
            ),
            color_confidence=_confidence(available, "color_ratio"),
            diameter_confidence=None,
            damage_confidence=_confidence(available, "damage_area_cm2"),
            severe_confidence=_confidence(available, "severe_defect"),
        )


class OnnxMeasurementPredictor:
    """MVP deployment backend using ONNX Runtime CUDA when available."""

    def __init__(self, model_path: str | Path) -> None:
        try:
            import onnxruntime as ort
        except ImportError as exc:
            raise PredictorNotConfigured(
                "onnxruntime-gpu is required on GPU PC 2 for ONNX inference"
            ) from exc
        model_path = Path(model_path).expanduser().resolve()
        metadata_path = model_path.with_suffix(model_path.suffix + ".json")
        if not model_path.is_file() or not metadata_path.is_file():
            raise PredictorNotConfigured("ONNX model and its .json metadata sidecar are required")
        import json

        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        available = ort.get_available_providers()
        providers = (
            ["CUDAExecutionProvider", "CPUExecutionProvider"]
            if "CUDAExecutionProvider" in available
            else ["CPUExecutionProvider"]
        )
        self._session = ort.InferenceSession(str(model_path), providers=providers)
        self._image_size = int(metadata.get("image_size", 640))
        self._trained_targets = frozenset(metadata.get("trained_targets", []))

    def predict(self, frame: InspectionFrame) -> FrameMeasurements:
        tensor = _image_bytes_to_tensor(frame.image_data, self._image_size)
        values, confidences = self._session.run(None, {"images": tensor.numpy()})
        available = {
            name: (float(values[0, index]), float(confidences[0, index]))
            for index, name in enumerate(TARGET_NAMES)
            if name in self._trained_targets
        }
        severe = _value(available, "severe_defect")
        return FrameMeasurements(
            color_ratio=_value(available, "color_ratio"),
            diameter_mm=None,
            damage_area_cm2=_value(available, "damage_area_cm2"),
            severe_defect=severe >= 0.5 if severe is not None else None,
            color_confidence=_confidence(available, "color_ratio"),
            diameter_confidence=None,
            damage_confidence=_confidence(available, "damage_area_cm2"),
            severe_confidence=_confidence(available, "severe_defect"),
        )


def _value(outputs: dict[str, tuple[float, float]], name: str) -> float | None:
    return outputs[name][0] if name in outputs else None


def _confidence(outputs: dict[str, tuple[float, float]], name: str) -> float | None:
    return outputs[name][1] if name in outputs else None


def load_measurement_predictor(model_path: str | Path, *, backend: str = "auto"):
    path = Path(model_path)
    selected = ("onnx" if path.suffix.lower() == ".onnx" else "torch") if backend == "auto" else backend
    if selected == "onnx":
        return OnnxMeasurementPredictor(path)
    if selected == "torch":
        return TorchMeasurementPredictor(path)
    raise ValueError("backend must be auto, onnx, or torch")


def predict_declared_frames(
    session: InspectionSession,
    predictor: FramePredictor[PredictionT],
) -> tuple[IndexedPrediction[PredictionT], ...]:
    """Run inference in frame-index order after all declared frames arrive.

    The function returns opaque per-frame outputs.  It intentionally does not
    choose a multi-frame aggregation rule or create a ``QualityResult``.
    """

    if not session.has_all_declared_frames:
        raise IncompleteInspectionError(
            f"inspection {session.inspection_id!r} has {session.received_count}/"
            f"{session.total_frames} declared frames"
        )
    return tuple(
        IndexedPrediction(frame.frame_index, predictor.predict(frame))
        for frame in session.ordered_frames
    )
