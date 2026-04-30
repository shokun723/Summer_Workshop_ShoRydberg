import argparse
import random
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageDraw

VALID_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}


def is_image_file(path: Path) -> bool:
    return path.suffix.lower() in VALID_EXTS


def random_crop_resize(img: Image.Image, min_scale=0.7) -> Image.Image:
    w, h = img.size
    scale = random.uniform(min_scale, 1.0)
    cw, ch = int(w * scale), int(h * scale)
    left = random.randint(0, w - cw)
    top = random.randint(0, h - ch)
    cropped = img.crop((left, top, left + cw, top + ch))
    return cropped.resize((w, h), Image.Resampling.BICUBIC)


def random_translate(img: Image.Image, max_shift_ratio=0.15) -> Image.Image:
    w, h = img.size
    max_dx = int(w * max_shift_ratio)
    max_dy = int(h * max_shift_ratio)
    dx = random.randint(-max_dx, max_dx)
    dy = random.randint(-max_dy, max_dy)

    canvas = Image.new("RGB", (w, h), (0, 0, 0))
    canvas.paste(img, (dx, dy))
    return canvas


def random_cutout(img: Image.Image, holes_range=(1, 4), size_range=(0.06, 0.2)) -> Image.Image:
    w, h = img.size
    draw = ImageDraw.Draw(img)
    holes = random.randint(*holes_range)
    for _ in range(holes):
        rw = int(w * random.uniform(*size_range))
        rh = int(h * random.uniform(*size_range))
        x1 = random.randint(0, max(0, w - rw))
        y1 = random.randint(0, max(0, h - rh))
        draw.rectangle([x1, y1, x1 + rw, y1 + rh], fill=(0, 0, 0))
    return img


def augment_one(img: Image.Image, out_size=None) -> Image.Image:
    img = img.convert("RGB")
    w, h = img.size

    if random.random() < 0.5:
        img = ImageOps.mirror(img)
    if random.random() < 0.2:
        img = ImageOps.flip(img)

    if random.random() < 0.8:
        angle = random.uniform(-35, 35)
        img = img.rotate(
            angle,
            resample=Image.Resampling.BICUBIC,
            expand=True,
            fillcolor=(0, 0, 0),
        )
        img = ImageOps.fit(img, (w, h), method=Image.Resampling.BICUBIC)

    if random.random() < 0.7:
        img = random_crop_resize(img, min_scale=0.7)

    if random.random() < 0.6:
        img = random_translate(img, max_shift_ratio=0.15)

    if random.random() < 0.6:
        img = ImageEnhance.Brightness(img).enhance(random.uniform(0.8, 1.2))
        img = ImageEnhance.Contrast(img).enhance(random.uniform(0.8, 1.25))
        img = ImageEnhance.Color(img).enhance(random.uniform(0.75, 1.25))

    if random.random() < 0.25:
        img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.4, 1.5)))

    if random.random() < 0.35:
        img = random_cutout(img.copy(), holes_range=(1, 4), size_range=(0.06, 0.2))

    if out_size is not None:
        img = img.resize((out_size, out_size), Image.Resampling.BICUBIC)

    return img


def augment_dataset(input_dir: Path, output_dir: Path, n_aug: int, copy_original: bool, seed: int, out_size: int | None):
    random.seed(seed)

    images = [p for p in input_dir.rglob("*") if p.is_file() and is_image_file(p)]
    if not images:
        print(f"No images found in: {input_dir}")
        return

    for img_path in images:
        rel_parent = img_path.parent.relative_to(input_dir)
        out_folder = output_dir / rel_parent
        out_folder.mkdir(parents=True, exist_ok=True)

        try:
            image = Image.open(img_path).convert("RGB")
        except Exception:
            print(f"Skipping unreadable file: {img_path}")
            continue

        stem = img_path.stem

        if copy_original:
            orig = image.resize((out_size, out_size), Image.Resampling.BICUBIC) if out_size else image
            orig.save(out_folder / f"{stem}_orig.jpg", quality=95)

        for i in range(n_aug):
            aug = augment_one(image.copy(), out_size=out_size)
            aug.save(out_folder / f"{stem}_aug_{i + 1:03d}.jpg", quality=95)

    print(f"Done. Saved augmented images to: {output_dir}")


def main():
    parser = argparse.ArgumentParser(description="Generate augmented images using Pillow only.")
    parser.add_argument("--input_dir", type=str, required=True)
    parser.add_argument("--output_dir", type=str, required=True)
    parser.add_argument("--n_aug", type=int, default=5)
    parser.add_argument("--copy_original", action="store_true")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out_size", type=int, default=224, help="Set 0 to keep original size.")
    args = parser.parse_args()

    out_size = None if args.out_size == 0 else args.out_size

    augment_dataset(
        input_dir=Path(args.input_dir),
        output_dir=Path(args.output_dir),
        n_aug=args.n_aug,
        copy_original=args.copy_original,
        seed=args.seed,
        out_size=out_size,
    )


if __name__ == "__main__":
    main()
