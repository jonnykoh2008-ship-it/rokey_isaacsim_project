"""Train measurement heads from ``apple_data`` without inventing labels.

The current capture has no trainable RGB quality head.  Color, damage, and
severe-defect heads become trainable after ``quality_annotations.json`` is supplied.
Diameter remains a depth/intrinsics geometry measurement, not an RGB model head.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from apple_quality_dataset import (
    TARGET_NAMES,
    AppleQualityTorchDataset,
    inspect_capabilities,
    load_dataset_records,
)
from predictor import create_measurement_model


TARGET_SCALES = (0.10, 0.50, 0.25)


def split_records(records, validation_fraction: float, seed: int):
    if not 0.0 < validation_fraction < 1.0:
        raise ValueError("validation_fraction must be between 0 and 1")
    shuffled = list(records)
    random.Random(seed).shuffle(shuffled)
    validation_count = max(1, round(len(shuffled) * validation_fraction))
    return tuple(shuffled[validation_count:]), tuple(shuffled[:validation_count])


def _batch_loss(values, confidences, targets, target_mask):
    import torch
    import torch.nn.functional as functional

    scales = torch.tensor(TARGET_SCALES, device=values.device)
    normalized_error = torch.abs(values - targets) / scales
    continuous_loss = normalized_error.square()
    severe_loss = functional.binary_cross_entropy(
        values[:, 2].clamp(1e-6, 1.0 - 1e-6),
        targets[:, 2],
        reduction="none",
    )
    value_loss = continuous_loss
    value_loss[:, 2] = severe_loss
    confidence_target = torch.exp(-normalized_error.detach()).clamp(0.0, 1.0)
    confidence_loss = (confidences - confidence_target).square()
    valid = target_mask.to(values.dtype)
    denominator = valid.sum().clamp_min(1.0)
    return ((value_loss + 0.25 * confidence_loss) * valid).sum() / denominator


def _evaluate(model, loader, device):
    import torch

    absolute_error = torch.zeros(len(TARGET_NAMES), device=device)
    counts = torch.zeros(len(TARGET_NAMES), device=device)
    model.eval()
    with torch.inference_mode():
        for images, targets, target_mask in loader:
            images = images.to(device)
            targets = targets.to(device)
            target_mask = target_mask.to(device)
            values, _ = model(images)
            absolute_error += (torch.abs(values - targets) * target_mask).sum(dim=0)
            counts += target_mask.sum(dim=0)
    return {
        name: (float((absolute_error[index] / counts[index]).cpu()) if counts[index] else None)
        for index, name in enumerate(TARGET_NAMES)
    }


def train(args) -> dict:
    import torch
    from torch.utils.data import DataLoader

    torch.manual_seed(args.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)
    records = load_dataset_records(args.dataset)
    if args.max_samples:
        records = records[: args.max_samples]
    capabilities = inspect_capabilities(records)
    if args.require_complete_quality_labels and not capabilities.supports_complete_quality_training:
        raise RuntimeError(
            "complete quality training requires color_ratio, damage_area_cm2 and "
            "severe_defect annotations; the current capture contains diameter labels only"
        )

    label_counts = {
        "color_ratio": capabilities.color_ratio_labels,
        "damage_area_cm2": capabilities.damage_area_labels,
        "severe_defect": capabilities.severe_defect_labels,
    }
    trainable_targets = [
        name for name in TARGET_NAMES if label_counts[name] == capabilities.samples
    ]
    if not trainable_targets:
        raise RuntimeError(
            "the dataset has diameter metadata but no RGB quality annotations; "
            "add quality_annotations.json before training color, damage, or severe-defect heads"
        )

    train_records, validation_records = split_records(records, args.validation_fraction, args.seed)
    train_dataset = AppleQualityTorchDataset(train_records, args.image_size)
    validation_dataset = AppleQualityTorchDataset(validation_records, args.image_size)
    loader_options = {
        "batch_size": args.batch_size,
        "num_workers": args.workers,
        "pin_memory": torch.cuda.is_available(),
    }
    train_loader = DataLoader(train_dataset, shuffle=True, **loader_options)
    validation_loader = DataLoader(validation_dataset, shuffle=False, **loader_options)
    device = "cuda" if args.device == "auto" and torch.cuda.is_available() else (
        "cpu" if args.device == "auto" else args.device
    )
    model = create_measurement_model().to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate)

    for epoch in range(1, args.epochs + 1):
        model.train()
        running_loss = 0.0
        batches = 0
        for images, targets, target_mask in train_loader:
            images = images.to(device)
            targets = targets.to(device)
            target_mask = target_mask.to(device)
            optimizer.zero_grad(set_to_none=True)
            values, confidences = model(images)
            loss = _batch_loss(values, confidences, targets, target_mask)
            loss.backward()
            optimizer.step()
            running_loss += float(loss.detach().cpu())
            batches += 1
        metrics = _evaluate(model, validation_loader, device)
        print(
            f"epoch {epoch:03d}/{args.epochs:03d} "
            f"loss={running_loss / max(1, batches):.5f} validation_mae={metrics}"
        )

    trained_targets = trainable_targets
    metrics = _evaluate(model, validation_loader, device)
    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "model_state": model.state_dict(),
            "image_size": args.image_size,
            "trained_targets": trained_targets,
            "validation_mae": metrics,
            "dataset_capabilities": capabilities.to_dict(),
            "seed": args.seed,
        },
        output,
    )

    if args.onnx_output:
        onnx_output = Path(args.onnx_output).expanduser().resolve()
        onnx_output.parent.mkdir(parents=True, exist_ok=True)
        dummy = torch.zeros(1, 3, args.image_size, args.image_size, device=device)
        try:
            torch.onnx.export(
                model,
                dummy,
                onnx_output,
                input_names=["images"],
                output_names=["measurements", "confidences"],
                dynamic_axes={"images": {0: "batch"}, "measurements": {0: "batch"}, "confidences": {0: "batch"}},
                opset_version=17,
            )
        except ModuleNotFoundError as exc:
            raise RuntimeError("install the onnx package before requesting ONNX export") from exc
        onnx_output.with_suffix(onnx_output.suffix + ".json").write_text(
            json.dumps(
                {"image_size": args.image_size, "trained_targets": trained_targets},
                indent=2,
            ),
            encoding="utf-8",
        )

    report = {
        "checkpoint": str(output),
        "device": device,
        "trained_targets": trained_targets,
        "validation_mae": metrics,
        "capabilities": capabilities.to_dict(),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", default="apple_data")
    parser.add_argument("--output", default="quality_grading_system/models/apple_quality_measurements.pt")
    parser.add_argument("--onnx-output")
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--image-size", type=int, default=640)
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    parser.add_argument("--validation-fraction", type=float, default=0.2)
    parser.add_argument("--workers", type=int, default=0)
    parser.add_argument("--seed", type=int, default=20260823)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--max-samples", type=int, default=0)
    parser.add_argument("--require-complete-quality-labels", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> None:
    train(build_parser().parse_args(argv))


if __name__ == "__main__":
    main()
