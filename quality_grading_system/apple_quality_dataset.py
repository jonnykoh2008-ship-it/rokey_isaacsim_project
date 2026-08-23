"""Dataset reader for segmentation-based apple quality annotations."""

from __future__ import annotations

import argparse
import ast
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable


MASK_TARGETS = ("target_color_mask", "damage_mask")
ANNOTATION_FILE = "quality_annotations.json"


class DatasetContractError(ValueError):
    pass


@dataclass(frozen=True)
class CameraIntrinsics:
    width: int
    height: int
    fx: float
    fy: float
    cx: float
    cy: float


@dataclass(frozen=True)
class AppleDatasetRecord:
    dataset_root: Path
    asset_type: str
    view_index: int
    rgb_path: Path
    depth_path: Path
    instance_segmentation_path: Path
    instance_mapping_path: Path
    camera_params_path: Path
    measured_diameter_mm: float
    target_color_mask_path: Path | None = None
    damage_mask_path: Path | None = None
    ignore_mask_path: Path | None = None
    severe_defect: bool | None = None

    @property
    def relative_rgb_path(self) -> str:
        return self.rgb_path.relative_to(self.dataset_root).as_posix()


@dataclass(frozen=True)
class DatasetCapabilities:
    samples: int
    diameter_labels: int
    color_mask_labels: int
    damage_mask_labels: int
    severe_defect_labels: int
    asset_types: tuple[str, ...]

    @property
    def supports_complete_quality_training(self) -> bool:
        return bool(self.samples) and all(
            count == self.samples
            for count in (
                self.color_mask_labels,
                self.damage_mask_labels,
                self.severe_defect_labels,
            )
        )

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["color_ratio_labels"] = self.color_mask_labels
        value["damage_area_labels"] = self.damage_mask_labels
        value["supports_complete_quality_training"] = self.supports_complete_quality_training
        return value


def resolve_dataset_root(path: str | Path) -> Path:
    candidate = Path(path).expanduser().resolve()
    if (candidate / "dataset_manifest.json").is_file():
        return candidate
    runs = sorted(
        child
        for child in candidate.iterdir()
        if child.is_dir() and (child / "dataset_manifest.json").is_file()
    ) if candidate.is_dir() else []
    if not runs:
        raise DatasetContractError(f"dataset_manifest.json not found below {candidate}")
    return runs[-1]


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise DatasetContractError(f"cannot read JSON {path}: {exc}") from exc


def _require_file(path: Path) -> Path:
    if not path.is_file():
        raise DatasetContractError(f"required dataset file is missing: {path}")
    return path


def _load_optional_annotations(root: Path) -> dict[str, dict[str, Any]]:
    path = root / ANNOTATION_FILE
    if not path.is_file():
        return {}
    value = _load_json(path)
    if not isinstance(value, dict):
        raise DatasetContractError(f"{path} must contain an object keyed by relative RGB path")
    return value


def _optional_path(root: Path, values: dict[str, Any], key: str) -> Path | None:
    raw = values.get(key)
    if raw in (None, ""):
        return None
    path = (root / str(raw)).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise DatasetContractError(f"{key} must stay inside dataset root") from exc
    return _require_file(path)


def _optional_bool(values: dict[str, Any], key: str) -> bool | None:
    value = values.get(key)
    if value is None:
        return None
    if not isinstance(value, bool):
        raise DatasetContractError(f"{key} must be boolean or null")
    return value


def load_dataset_records(path: str | Path) -> tuple[AppleDatasetRecord, ...]:
    root = resolve_dataset_root(path)
    manifest = _load_json(root / "dataset_manifest.json")
    annotations = _load_optional_annotations(root)
    records: list[AppleDatasetRecord] = []

    for asset_type in manifest.get("apple_types", []):
        asset_root = root / str(asset_type)
        if not asset_root.is_dir():
            raise DatasetContractError(f"asset folder is missing: {asset_root}")
        for size_root in sorted(child for child in asset_root.iterdir() if child.is_dir()):
            metadata_path = _require_file(size_root / "metadata.json")
            metadata = _load_json(metadata_path)
            if not isinstance(metadata, list):
                raise DatasetContractError(f"{metadata_path} must contain a list")
            for item in metadata:
                rgb_name = str(item["rgb_file"])
                stem = Path(rgb_name).stem.removeprefix("rgb_")
                rgb_path = _require_file(size_root / rgb_name)
                relative = rgb_path.relative_to(root).as_posix()
                extra = annotations.get(relative, {})
                if not isinstance(extra, dict):
                    raise DatasetContractError(f"annotation for {relative} must be an object")
                records.append(
                    AppleDatasetRecord(
                        dataset_root=root,
                        asset_type=str(item["asset_type"]),
                        view_index=int(item["view_index"]),
                        rgb_path=rgb_path,
                        depth_path=_require_file(
                            size_root / f"distance_to_camera_{stem}.npy"
                        ),
                        instance_segmentation_path=_require_file(
                            size_root / f"instance_id_segmentation_{stem}.png"
                        ),
                        instance_mapping_path=_require_file(
                            size_root / f"instance_id_segmentation_mapping_{stem}.json"
                        ),
                        camera_params_path=_require_file(
                            size_root / f"camera_params_{stem}.json"
                        ),
                        measured_diameter_mm=float(item["measured_diameter_mm"]),
                        target_color_mask_path=_optional_path(
                            root, extra, "target_color_mask"
                        ),
                        damage_mask_path=_optional_path(root, extra, "damage_mask"),
                        ignore_mask_path=_optional_path(root, extra, "ignore_mask"),
                        severe_defect=_optional_bool(extra, "severe_defect"),
                    )
                )
    expected = int(manifest.get("total_rgb_images", len(records)))
    if len(records) != expected:
        raise DatasetContractError(
            f"manifest declares {expected} images but found {len(records)}"
        )
    return tuple(records)


def inspect_capabilities(records: Iterable[AppleDatasetRecord]) -> DatasetCapabilities:
    values = tuple(records)
    return DatasetCapabilities(
        samples=len(values),
        diameter_labels=sum(item.measured_diameter_mm > 0.0 for item in values),
        color_mask_labels=sum(item.target_color_mask_path is not None for item in values),
        damage_mask_labels=sum(item.damage_mask_path is not None for item in values),
        severe_defect_labels=sum(item.severe_defect is not None for item in values),
        asset_types=tuple(sorted({item.asset_type for item in values})),
    )


def load_camera_intrinsics(record: AppleDatasetRecord) -> CameraIntrinsics:
    params = _load_json(record.camera_params_path)
    width, height = (int(value) for value in params["renderProductResolution"])
    projection = params["cameraProjection"]
    return CameraIntrinsics(
        width=width,
        height=height,
        fx=float(projection[0]) * width * 0.5,
        fy=float(projection[5]) * height * 0.5,
        cx=width * 0.5,
        cy=height * 0.5,
    )


def load_apple_mask(record: AppleDatasetRecord):
    import numpy as np
    from PIL import Image

    segmentation = np.asarray(
        Image.open(record.instance_segmentation_path).convert("RGBA")
    )
    mapping = _load_json(record.instance_mapping_path)
    colors = [
        np.asarray(ast.literal_eval(encoded), dtype=np.uint8)
        for encoded, prim_path in mapping.items()
        if record.asset_type in str(prim_path)
    ]
    if not colors:
        raise DatasetContractError(
            f"apple prim is absent from {record.instance_mapping_path}"
        )
    mask = np.zeros(segmentation.shape[:2], dtype=bool)
    for color in colors:
        mask |= np.all(segmentation == color, axis=2)
    if not bool(mask.any()):
        raise DatasetContractError(
            f"apple mask is empty in {record.instance_segmentation_path}"
        )
    return mask


def estimate_visible_diameter_mm(record: AppleDatasetRecord) -> float:
    """Diagnostic visible extent for the existing radial-depth capture."""

    import numpy as np

    mask = load_apple_mask(record)
    depth = np.load(record.depth_path)
    intrinsics = load_camera_intrinsics(record)
    valid = mask & np.isfinite(depth) & (depth > 0.0)
    if int(valid.sum()) < 10:
        raise DatasetContractError(
            f"too few valid apple depth pixels in {record.depth_path}"
        )
    ys, xs = np.nonzero(valid)
    radial_depth = depth[ys, xs]
    ray_x = (xs - intrinsics.cx) / intrinsics.fx
    ray_y = (ys - intrinsics.cy) / intrinsics.fy
    ray_norm = np.sqrt(ray_x * ray_x + ray_y * ray_y + 1.0)
    points_x = radial_depth * ray_x / ray_norm
    points_y = radial_depth * ray_y / ray_norm
    extent_x = np.percentile(points_x, 99.8) - np.percentile(points_x, 0.2)
    extent_y = np.percentile(points_y, 99.8) - np.percentile(points_y, 0.2)
    return float(max(extent_x, extent_y) * 1000.0)


def letterbox_rgb(image, size: int = 640):
    from PIL import Image

    image = image.convert("RGB")
    scale = min(size / image.width, size / image.height)
    resized = image.resize(
        (max(1, round(image.width * scale)), max(1, round(image.height * scale))),
        Image.Resampling.BILINEAR,
    )
    canvas = Image.new("RGB", (size, size), (114, 114, 114))
    canvas.paste(resized, ((size - resized.width) // 2, (size - resized.height) // 2))
    return canvas


def _letterbox_mask(mask, size: int):
    import numpy as np
    from PIL import Image

    image = Image.fromarray(np.asarray(mask, dtype=np.uint8) * 255, mode="L")
    scale = min(size / image.width, size / image.height)
    resized = image.resize(
        (max(1, round(image.width * scale)), max(1, round(image.height * scale))),
        Image.Resampling.NEAREST,
    )
    canvas = Image.new("L", (size, size), 0)
    canvas.paste(resized, ((size - resized.width) // 2, (size - resized.height) // 2))
    return np.asarray(canvas) > 0


def _load_binary_mask(path: Path, expected_shape: tuple[int, int]):
    import numpy as np
    from PIL import Image

    value = np.asarray(Image.open(path).convert("L")) > 0
    if value.shape != expected_shape:
        raise DatasetContractError(f"mask dimensions do not match RGB: {path}")
    return value


class AppleQualityTorchDataset:
    """Torch dataset for color/damage segmentation and severe classification."""

    def __init__(self, records: Iterable[AppleDatasetRecord], image_size: int = 640) -> None:
        self.records = tuple(records)
        self.image_size = image_size

    def __len__(self) -> int:
        return len(self.records)

    def __getitem__(self, index: int):
        import numpy as np
        import torch
        from PIL import Image

        record = self.records[index]
        raw_image = Image.open(record.rgb_path).convert("RGB")
        expected_shape = (raw_image.height, raw_image.width)
        surface = load_apple_mask(record)
        if surface.shape != expected_shape:
            raise DatasetContractError(
                f"instance mask dimensions do not match RGB: {record.rgb_path}"
            )
        ignore = (
            _load_binary_mask(record.ignore_mask_path, expected_shape)
            if record.ignore_mask_path
            else np.zeros(expected_shape, dtype=bool)
        )
        color = (
            _load_binary_mask(record.target_color_mask_path, expected_shape)
            if record.target_color_mask_path
            else np.zeros(expected_shape, dtype=bool)
        )
        damage = (
            _load_binary_mask(record.damage_mask_path, expected_shape)
            if record.damage_mask_path
            else np.zeros(expected_shape, dtype=bool)
        )

        image = letterbox_rgb(raw_image, self.image_size)
        pixels = np.asarray(image, dtype=np.float32) / 255.0
        image_tensor = torch.from_numpy(pixels).permute(2, 0, 1).contiguous()
        mask_targets = torch.from_numpy(
            np.stack(
                (
                    _letterbox_mask(color & surface, self.image_size),
                    _letterbox_mask(damage & surface, self.image_size),
                )
            ).astype(np.float32)
        )
        valid_surface = torch.from_numpy(
            _letterbox_mask(surface & ~ignore, self.image_size)
        )
        target_valid = torch.tensor(
            (
                record.target_color_mask_path is not None,
                record.damage_mask_path is not None,
                record.severe_defect is not None,
            ),
            dtype=torch.bool,
        )
        severe_target = torch.tensor(
            float(record.severe_defect) if record.severe_defect is not None else 0.0,
            dtype=torch.float32,
        )
        return image_tensor, mask_targets, severe_target, target_valid, valid_surface


def main(args: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Audit Isaac Sim apple quality segmentation labels"
    )
    parser.add_argument("dataset", nargs="?", default="apple_data")
    parsed = parser.parse_args(args)
    records = load_dataset_records(parsed.dataset)
    print(
        json.dumps(
            inspect_capabilities(records).to_dict(),
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
