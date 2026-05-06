from __future__ import annotations

import random
import re
import time
from collections import Counter
from pathlib import Path
import shutil
from typing import Callable

import numpy as np
import pandas as pd
from IPython.display import display
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps
import ipywidgets as widgets


VALID_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}
DAMAGE_POSITIVE_KEYWORDS = {
    "damaged",
    "defect",
    "defective",
    "broken",
    "crack",
    "cracked",
    "scratch",
    "scratched",
    "fault",
    "failed",
    "chip",
    "chipped",
}
DAMAGE_NEGATIVE_KEYWORDS = {
    "not-damaged",
    "not_damaged",
    "undamaged",
    "normal",
    "healthy",
    "good",
    "ok",
    "clean",
    "pass",
    "nominal",
}


def create_progress(title: str, maximum: int) -> tuple[widgets.IntProgress, widgets.HTML]:
    maximum = max(int(maximum), 1)
    bar = widgets.IntProgress(
        value=0,
        min=0,
        max=maximum,
        description=title,
        bar_style="info",
        layout=widgets.Layout(width="650px"),
    )
    status = widgets.HTML(value=f"<b>{title}</b>: waiting to start")
    display(widgets.VBox([status, bar]))
    return bar, status


def update_progress(
    bar: widgets.IntProgress,
    status: widgets.HTML,
    value: int,
    message: str,
    done: bool = False,
) -> None:
    bar.value = min(int(value), int(bar.max))
    bar.bar_style = "success" if done else "info"
    status.value = message


def record_timing(timings: list[dict[str, float]], step: str, started_at: float) -> float:
    elapsed = time.perf_counter() - started_at
    timings.append({"step": step, "seconds": round(elapsed, 3)})
    return elapsed


def timing_frame(timings: list[dict[str, float]]) -> pd.DataFrame:
    if not timings:
        return pd.DataFrame(columns=["step", "seconds"])
    frame = pd.DataFrame(timings)
    frame["seconds"] = frame["seconds"].round(3)
    return frame


def _read_metadata(metadata_path: Path | None) -> pd.DataFrame | None:
    if metadata_path is None or not metadata_path.exists():
        return None

    metadata = pd.read_csv(metadata_path)
    metadata.columns = [col.strip() for col in metadata.columns]
    return metadata


def _normalize_relpath(value: str) -> str:
    return value.replace("\\", "/").strip().lower()


def _infer_damage_status(rel_path: Path) -> str | None:
    parts = [piece.lower() for piece in rel_path.parts]
    joined = " ".join(parts)
    top_level = parts[0] if parts else ""

    if top_level.startswith("device"):
        return "Not-Damaged"

    if any(keyword in joined for keyword in DAMAGE_NEGATIVE_KEYWORDS):
        return "Not-Damaged"
    if any(keyword in joined for keyword in DAMAGE_POSITIVE_KEYWORDS):
        return "Damaged"
    return None


def _infer_device_type(rel_path: Path) -> str | None:
    parts = [piece.lower() for piece in rel_path.parts]
    top_level = parts[0] if parts else ""

    if top_level.startswith("device"):
        return rel_path.parts[0] if rel_path.parts else None

    if top_level == "defect":
        match = re.match(r"^(\d+)", rel_path.stem)
        if match:
            device_id = match.group(1)
            return f"device{device_id}" if device_id == "1" else f"device {device_id}"

    return None


def load_image_records(
    dataset_root: str | Path,
    metadata_path: str | Path | None = None,
    include_subfolders: bool = True,
) -> pd.DataFrame:
    root = Path(dataset_root).resolve()
    metadata_path = Path(metadata_path).resolve() if metadata_path else None
    metadata = _read_metadata(metadata_path)

    rows: list[dict[str, object]] = []
    metadata_lookup: dict[str, dict[str, object]] = {}
    image_paths: list[Path] = []

    if metadata is not None:
        for row in metadata.to_dict(orient="records"):
            rel_value = (
                row.get("relative_path")
                or row.get("filepath")
                or row.get("file_path")
                or row.get("path")
                or row.get("filename")
            )
            if rel_value:
                rel_key = _normalize_relpath(str(rel_value))
                metadata_lookup[rel_key] = row

                candidate = root / Path(str(rel_value))
                if candidate.exists() and candidate.is_file() and candidate.suffix.lower() in VALID_EXTS:
                    image_paths.append(candidate)

    if not image_paths:
        if include_subfolders:
            image_paths = [path for path in root.rglob("*") if path.is_file() and path.suffix.lower() in VALID_EXTS]
        else:
            image_paths = [path for path in root.glob("*") if path.is_file() and path.suffix.lower() in VALID_EXTS]

    for image_path in sorted(image_paths):
        rel_path = image_path.relative_to(root)
        rel_key = _normalize_relpath(str(rel_path))
        metadata_row = metadata_lookup.get(rel_key, {})

        top_level = rel_path.parts[0] if rel_path.parts else "unknown"
        inferred_device_type = _infer_device_type(rel_path)
        device_type = metadata_row.get("device_type") or metadata_row.get("device_label") or inferred_device_type or top_level
        damage_status = (
            metadata_row.get("damage_status")
            or metadata_row.get("status")
            or metadata_row.get("label")
            or _infer_damage_status(rel_path)
        )
        top_level_normalized = str(top_level).strip().lower()
        is_defect_folder = top_level_normalized == "defect"
        is_device_folder = top_level_normalized.startswith("device")

        rows.append(
            {
                "filepath": str(image_path),
                "relative_path": str(rel_path).replace("\\", "/"),
                "device_type": str(device_type),
                "damage_status": None if pd.isna(damage_status) else damage_status,
                "top_level_folder": top_level,
                "has_damage_label": damage_status is not None and not pd.isna(damage_status),
                "has_device_type_label": device_type is not None and not pd.isna(device_type),
                "device_type_label_source": "filename-prefix" if inferred_device_type and top_level_normalized == "defect" else "folder-or-metadata",
                "is_defect_folder": is_defect_folder,
                "is_standard_device_image": is_device_folder,
                "is_defect_challenge": is_defect_folder,
            }
        )

    return pd.DataFrame(rows)


def target_column_for_mode(target_mode: str) -> str:
    mapping = {
        "device_type": "device_type",
        "damage_status": "damage_status",
    }
    if target_mode not in mapping:
        raise ValueError(f"Unsupported target_mode: {target_mode}")
    return mapping[target_mode]


def available_target_modes(records: pd.DataFrame) -> list[str]:
    available = ["device_type"]
    damage_labels = records["damage_status"].dropna().astype(str).unique().tolist() if "damage_status" in records else []
    if len(damage_labels) >= 2:
        available.append("damage_status")
    return available


def validate_target_mode(records: pd.DataFrame, target_mode: str) -> tuple[bool, str]:
    column = target_column_for_mode(target_mode)

    if records.empty:
        return False, "No images were found in the selected dataset."

    if column not in records.columns:
        return False, f"The target column `{column}` is not available."

    values = records[column].dropna().astype(str)
    unique_values = sorted(values.unique().tolist())

    if len(unique_values) < 2:
        if target_mode == "damage_status":
            return (
                False,
                "Damage-status mode needs at least two labels such as `Damaged` and `Not-Damaged`. "
                "Add defect images or provide a metadata CSV with damage labels, then rerun this notebook.",
            )
        return False, f"The target `{target_mode}` needs at least two classes to train a classifier."

    return True, f"Target `{target_mode}` is ready with classes: {unique_values}"


def safe_stratify_labels(labels: np.ndarray) -> np.ndarray | None:
    counts = Counter(labels.tolist())
    if not counts:
        return None
    if min(counts.values()) < 2:
        return None
    return labels


def load_images_as_arrays(
    records: pd.DataFrame,
    image_size: int,
    color_mode: str = "rgb",
    progress_title: str = "Load images",
) -> tuple[np.ndarray, np.ndarray]:
    arrays: list[np.ndarray] = []
    valid_indices: list[int] = []
    bar, status = create_progress(progress_title, len(records))

    for index, row in enumerate(records.itertuples(index=False), start=1):
        path = Path(row.filepath)
        with Image.open(path) as image:
            image = image.convert("RGB")
            image = ImageOps.fit(image, (image_size, image_size), method=Image.Resampling.BICUBIC)
            if color_mode.lower() == "grayscale":
                image = image.convert("L")
            arrays.append(np.array(image))
            valid_indices.append(index - 1)

        update_progress(
            bar,
            status,
            index,
            f"Loaded {index} of {len(records)} images",
            done=index == len(records),
        )

    filtered_records = records.iloc[valid_indices].reset_index(drop=True)
    return np.array(arrays), filtered_records


def preview_augmentations(image: Image.Image, seed: int = 42) -> dict[str, Image.Image]:
    random.seed(seed)
    base = image.convert("RGB")
    black_fill_rotation = ImageOps.fit(
        base.rotate(18, resample=Image.Resampling.BICUBIC, expand=True, fillcolor=(0, 0, 0)),
        base.size,
        method=Image.Resampling.BICUBIC,
    )
    previews = {
        "Original": base,
        "Mirror": ImageOps.mirror(base),
        "Flip": ImageOps.flip(base),
        "Rotate (edge crop)": crop_dark_augmentation_edges(black_fill_rotation),
        "Rotate + crop": rotate_and_center_crop(base, 18),
        "Crop + Resize": random_crop_resize(base.copy()),
        "Shift": random_translate(base.copy()),
        "Color Shift": ImageEnhance.Color(base).enhance(1.35),
        "Brightness": ImageEnhance.Brightness(base).enhance(1.18),
        "Contrast": ImageEnhance.Contrast(base).enhance(1.15),
        "Blur": base.filter(ImageFilter.GaussianBlur(radius=0.6)),
    }
    return previews


def crop_dark_augmentation_edges(
    img: Image.Image,
    dark_threshold: int = 24,
    max_edge_dark_fraction: float = 0.0,
    min_crop_fraction: float = 0.45,
) -> Image.Image:
    """Trim dark edge bands created by rotations/translations, then restore size."""
    img = img.convert("RGB")
    w, h = img.size
    pixels = np.asarray(img)
    dark_pixels = pixels.max(axis=2) <= dark_threshold

    top, bottom = 0, h
    left, right = 0, w
    min_width = max(1, int(w * min_crop_fraction))
    min_height = max(1, int(h * min_crop_fraction))

    changed = True
    while changed:
        changed = False
        if bottom - top > min_height and dark_pixels[top, left:right].mean() > max_edge_dark_fraction:
            top += 1
            changed = True
        if bottom - top > min_height and dark_pixels[bottom - 1, left:right].mean() > max_edge_dark_fraction:
            bottom -= 1
            changed = True
        if right - left > min_width and dark_pixels[top:bottom, left].mean() > max_edge_dark_fraction:
            left += 1
            changed = True
        if right - left > min_width and dark_pixels[top:bottom, right - 1].mean() > max_edge_dark_fraction:
            right -= 1
            changed = True

    if top == 0 and bottom == h and left == 0 and right == w:
        return img

    if (right - left) <= 0 or (bottom - top) <= 0:
        return img

    cropped = img.crop((left, top, right, bottom))
    return cropped.resize((w, h), Image.Resampling.BICUBIC)


def rotate_and_center_crop(
    img: Image.Image,
    angle: float,
    crop_scale: float = 0.94,
) -> Image.Image:
    """Rotate an image, then crop slightly to remove rotation borders."""
    w, h = img.size
    rotated = img.rotate(
        angle,
        resample=Image.Resampling.BICUBIC,
        expand=True,
        fillcolor=(0, 0, 0),
    )
    fitted = ImageOps.fit(rotated, (w, h), method=Image.Resampling.BICUBIC)
    fitted = crop_dark_augmentation_edges(fitted)
    if crop_scale >= 1:
        return fitted

    crop_w = max(1, int(w * crop_scale))
    crop_h = max(1, int(h * crop_scale))
    left = (w - crop_w) // 2
    top = (h - crop_h) // 2
    cropped = fitted.crop((left, top, left + crop_w, top + crop_h))
    return cropped.resize((w, h), Image.Resampling.BICUBIC)


def random_crop_resize(img: Image.Image, min_scale: float = 0.72) -> Image.Image:
    w, h = img.size
    scale = random.uniform(min_scale, 1.0)
    crop_w, crop_h = int(w * scale), int(h * scale)
    left = random.randint(0, max(w - crop_w, 0))
    top = random.randint(0, max(h - crop_h, 0))
    cropped = img.crop((left, top, left + crop_w, top + crop_h))
    return cropped.resize((w, h), Image.Resampling.BICUBIC)


def random_translate(img: Image.Image, max_shift_ratio: float = 0.12) -> Image.Image:
    w, h = img.size
    max_dx = int(w * max_shift_ratio)
    max_dy = int(h * max_shift_ratio)
    dx = random.randint(-max_dx, max_dx)
    dy = random.randint(-max_dy, max_dy)
    canvas = Image.new("RGB", (w, h), (0, 0, 0))
    canvas.paste(img, (dx, dy))
    return crop_dark_augmentation_edges(canvas)


def random_cutout(
    img: Image.Image,
    holes_range: tuple[int, int] = (1, 3),
    size_range: tuple[float, float] = (0.06, 0.18),
) -> Image.Image:
    draw = ImageDraw.Draw(img)
    w, h = img.size
    holes = random.randint(*holes_range)
    for _ in range(holes):
        rw = int(w * random.uniform(*size_range))
        rh = int(h * random.uniform(*size_range))
        x1 = random.randint(0, max(w - rw, 1) - 1)
        y1 = random.randint(0, max(h - rh, 1) - 1)
        draw.rectangle([x1, y1, x1 + rw, y1 + rh], fill=(0, 0, 0))
    return img


def augment_one(image: Image.Image, out_size: int | None = 224) -> Image.Image:
    img = image.convert("RGB")
    w, h = img.size

    if random.random() < 0.5:
        img = ImageOps.mirror(img)
    if random.random() < 0.2:
        img = ImageOps.flip(img)
    if random.random() < 0.8:
        angle = random.uniform(-22, 22)
        img = rotate_and_center_crop(img, angle)
    if random.random() < 0.65:
        img = random_crop_resize(img)
    if random.random() < 0.55:
        img = random_translate(img)
    if random.random() < 0.7:
        img = ImageEnhance.Brightness(img).enhance(random.uniform(0.85, 1.18))
        img = ImageEnhance.Contrast(img).enhance(random.uniform(0.9, 1.2))
        img = ImageEnhance.Color(img).enhance(random.uniform(0.8, 1.2))
    if random.random() < 0.2:
        img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.2, 1.0)))
    img = crop_dark_augmentation_edges(img)
    if out_size:
        img = img.resize((out_size, out_size), Image.Resampling.BICUBIC)
    return img


def compute_balanced_targets(
    records: pd.DataFrame,
    label_column: str,
    target_class_size: int | None = None,
) -> dict[str, int]:
    class_counts = records[label_column].value_counts(dropna=True).to_dict()
    if not class_counts:
        return {}
    if target_class_size is None:
        target_class_size = max(class_counts.values())
    return {label: max(target_class_size - count, 0) for label, count in class_counts.items()}


def export_augmented_dataset(
    records: pd.DataFrame,
    output_root: str | Path,
    label_column: str,
    target_class_size: int | None = None,
    seed: int = 42,
    out_size: int = 224,
    status_prefix: str = "Augment",
    max_generated_images: int = 500,
    allow_large_export: bool = False,
) -> pd.DataFrame:
    random.seed(seed)
    output_root = Path(output_root).resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    # Keep the export directory aligned with the fresh metadata file instead of
    # accumulating stale images across multiple runs.
    for path in output_root.rglob("*"):
        if path.is_file() and path.suffix.lower() in VALID_EXTS:
            path.unlink()
    metadata_output = output_root / "metadata.csv"
    if metadata_output.exists():
        metadata_output.unlink()

    class_targets = compute_balanced_targets(records, label_column, target_class_size=target_class_size)
    planned_new_images = sum(class_targets.values())
    if planned_new_images > max_generated_images and not allow_large_export:
        raise ValueError(
            "Refusing to generate "
            f"{planned_new_images} augmented images because the notebook safety cap is "
            f"{max_generated_images}. Lower `TARGET_CLASS_SIZE`, reduce the dataset scope, "
            "or rerun with `allow_large_export=True` only if you really want a large export."
        )

    total_to_generate = len(records) + sum(class_targets.values())
    bar, status = create_progress(status_prefix, max(total_to_generate, 1))

    generated_rows: list[dict[str, object]] = []
    counter = 0

    original_rows = records.copy()
    original_rows["is_augmented"] = False
    original_rows["source_relative_path"] = original_rows["relative_path"]

    for copy_index, row in enumerate(original_rows.itertuples(index=False), start=1):
        source_path = Path(row.filepath)
        export_path = output_root / Path(row.relative_path)
        export_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, export_path)
        counter += 1
        update_progress(
            bar,
            status,
            counter,
            f"Copying originals: {copy_index} of {len(original_rows)}",
            done=counter == total_to_generate,
        )

    original_rows["filepath"] = original_rows["relative_path"].apply(lambda value: str(output_root / Path(value)))

    for label, needed in class_targets.items():
        if needed <= 0:
            continue

        class_records = records[records[label_column] == label].reset_index(drop=True)
        if class_records.empty:
            continue

        for generated_index in range(needed):
            source_row = class_records.iloc[generated_index % len(class_records)]
            source_path = Path(source_row["filepath"])
            rel_path = Path(source_row["relative_path"])
            export_dir = output_root / rel_path.parent
            export_dir.mkdir(parents=True, exist_ok=True)

            with Image.open(source_path) as image:
                augmented = augment_one(image, out_size=out_size)

            export_name = f"{source_path.stem}_aug_{generated_index + 1:03d}.jpg"
            export_path = export_dir / export_name
            augmented.save(export_path, quality=95)

            generated_rows.append(
                {
                    "filepath": str(export_path),
                    "relative_path": str(export_path.relative_to(output_root)).replace("\\", "/"),
                    "source_relative_path": source_row["relative_path"],
                    "device_type": source_row.get("device_type"),
                    "damage_status": source_row.get("damage_status"),
                    "top_level_folder": source_row.get("top_level_folder"),
                    "has_damage_label": source_row.get("has_damage_label"),
                    "is_defect_folder": source_row.get("is_defect_folder"),
                    "is_standard_device_image": source_row.get("is_standard_device_image"),
                    "is_defect_challenge": source_row.get("is_defect_challenge"),
                    "is_augmented": True,
                }
            )

            counter += 1
            update_progress(
                bar,
                status,
                counter,
                f"Generating class `{label}`: {generated_index + 1} of {needed}",
                done=counter == total_to_generate,
            )

    exported = pd.concat([original_rows, pd.DataFrame(generated_rows)], ignore_index=True, sort=False)
    exported.to_csv(output_root / "metadata.csv", index=False)
    return exported


def apply_to_records(
    records: pd.DataFrame,
    func: Callable[[pd.Series], object],
    progress_title: str,
) -> list[object]:
    outputs: list[object] = []
    bar, status = create_progress(progress_title, len(records))
    for index, (_, row) in enumerate(records.iterrows(), start=1):
        outputs.append(func(row))
        update_progress(
            bar,
            status,
            index,
            f"{progress_title}: {index} of {len(records)}",
            done=index == len(records),
        )
    return outputs
