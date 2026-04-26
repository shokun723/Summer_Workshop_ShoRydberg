import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def compare_preprocessing_with_histograms(image_path):
    img = Image.open(image_path).convert("RGB")
    img_array = np.array(img, dtype=np.float32)

    normalized = img_array / 255.0
    mean = normalized.mean(axis=(0, 1), keepdims=True)
    std = normalized.std(axis=(0, 1), keepdims=True)
    standardized = (normalized - mean) / std

    # Force every stage into the same 0..255 byte display space without
    # stretching each image independently.
    original_display = np.clip(img_array, 0, 255).astype(np.uint8)
    normalized_display = np.clip(normalized, 0, 255).astype(np.uint8)
    standardized_display = np.clip(standardized, 0, 255).astype(np.uint8)

    print("Original image stats:")
    print(f"Shape: {img_array.shape}")
    print(f"Min: {img_array.min():.2f}, Max: {img_array.max():.2f}")
    print(f"Channel means: {img_array.mean(axis=(0, 1))}")
    print(f"Channel stds: {img_array.std(axis=(0, 1))}")

    print("\nNormalized image stats:")
    print(f"Min: {normalized.min():.4f}, Max: {normalized.max():.4f}")
    print(f"Channel means: {normalized.mean(axis=(0, 1))}")
    print(f"Channel stds: {normalized.std(axis=(0, 1))}")

    print("\nStandardized image stats:")
    print(f"Min: {standardized.min():.4f}, Max: {standardized.max():.4f}")
    print(f"Channel means: {standardized.mean(axis=(0, 1))}")
    print(f"Channel stds: {standardized.std(axis=(0, 1))}")

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))

    image_panels = [
        ("Original RGB\nDisplayed as 0..255", original_display),
        ("Normalized RGB\nClipped into 0..255", normalized_display),
        ("Standardized RGB\nClipped into 0..255", standardized_display),
    ]

    hist_panels = [
        ("Original Pixel Distribution", img_array),
        ("Normalized Pixel Distribution", normalized),
        ("Standardized Pixel Distribution", standardized),
    ]

    colors = ["red", "green", "blue"]
    labels = ["Red", "Green", "Blue"]

    for ax, (title, image_data) in zip(axes[0], image_panels):
        ax.imshow(image_data)
        ax.set_title(title)
        ax.axis("off")

    for ax, (title, values) in zip(axes[1], hist_panels):
        flattened = values.reshape(-1, 3)
        for channel in range(3):
            ax.hist(
                flattened[:, channel],
                bins=64,
                alpha=0.45,
                color=colors[channel],
                label=labels[channel],
            )
        ax.set_title(title)
        ax.set_ylabel("Pixel count")
        ax.legend()

    axes[1, 0].set_xlabel("Pixel value (0..255)")
    axes[1, 0].set_xlim(0, 255)

    axes[1, 1].set_xlabel("Pixel value (0..1)")
    axes[1, 1].set_xlim(0, 1)

    axes[1, 2].set_xlabel("Z-score")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    compare_preprocessing_with_histograms("Device_Images_Nelson/device1/1.png")
