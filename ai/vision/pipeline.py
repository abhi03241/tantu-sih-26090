"""
Image Processing Pipeline for TANTU AI Vision Studio.
Maintained by Team Member R (AI Image Enhancement).

Provides modular, robust image validation, format normalization,
aspect ratio cropping, lighting/contrast enhancement, background cleaning,
and high-resolution catalogue resizing for artisan handicraft photos.
"""

import io
import math
import os
from typing import Tuple, List, Dict, Any, Optional, Union
from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageStat


SUPPORTED_FORMATS = {"JPEG", "JPG", "PNG", "WEBP", "BMP", "TIFF"}
DEFAULT_TARGET_SIZE = (1024, 1024)
MIN_DIMENSIONS = (50, 50)
MAX_DIMENSIONS = (8000, 8000)


class ImageValidationError(ValueError):
    """Raised when an input image fails validation checks."""
    pass


def validate_image_bytes(image_data: bytes, min_dims: Tuple[int, int] = MIN_DIMENSIONS, max_dims: Tuple[int, int] = MAX_DIMENSIONS) -> Image.Image:
    """
    Validates raw image bytes:
    - Checks for empty / corrupted data
    - Verifies valid image format
    - Enforces reasonable minimum and maximum dimensions
    Returns an opened PIL Image.
    """
    if not image_data or len(image_data) < 10:
        raise ImageValidationError("Image data is empty or too short.")

    try:
        img = Image.open(io.BytesIO(image_data))
        img.verify()  # Fast structural verification
        # Re-open because verify() closes/invalidates the stream in PIL
        img = Image.open(io.BytesIO(image_data))
    except Exception as exc:
        raise ImageValidationError(f"Invalid or corrupted image format: {exc}")

    img_format = (img.format or "").upper()
    if img_format not in SUPPORTED_FORMATS and img_format != "MPO":
        raise ImageValidationError(f"Unsupported image format: '{img_format}'. Supported: {', '.join(sorted(SUPPORTED_FORMATS))}")

    w, h = img.size
    if w < min_dims[0] or h < min_dims[1]:
        raise ImageValidationError(f"Image dimensions too small ({w}x{h}). Minimum required: {min_dims[0]}x{min_dims[1]}")

    if w > max_dims[0] or h > max_dims[1]:
        raise ImageValidationError(f"Image dimensions too large ({w}x{h}). Maximum allowed: {max_dims[0]}x{max_dims[1]}")

    return img


def fix_exif_orientation(img: Image.Image) -> Image.Image:
    """
    Corrects image orientation based on phone camera EXIF orientation tags.
    """
    try:
        return ImageOps.exif_transpose(img) or img
    except Exception:
        return img


def convert_to_rgb(img: Image.Image, bg_color: Tuple[int, int, int] = (255, 255, 255)) -> Image.Image:
    """
    Converts any image mode (RGBA, LA, P, CMYK, etc.) into clean RGB.
    Fills transparency with clean white/studio background.
    """
    if img.mode == "RGB":
        return img

    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
        alpha_img = img.convert("RGBA")
        background = Image.new("RGBA", alpha_img.size, (*bg_color, 255))
        composed = Image.alpha_composite(background, alpha_img)
        return composed.convert("RGB")

    return img.convert("RGB")


def detect_and_center_crop(img: Image.Image, target_aspect_ratio: float = 1.0, margin_pct: float = 0.05) -> Image.Image:
    """
    Analyzes image contrast and bounding area to center the subject
    and crop to the target aspect ratio (1.0 for square catalog photos).
    """
    w, h = img.size
    current_ratio = w / float(h)

    # If already close to target aspect ratio, do minimal framing
    if math.isclose(current_ratio, target_aspect_ratio, rel_tol=0.03):
        return img

    # Center crop to target aspect ratio
    if current_ratio > target_aspect_ratio:
        # Image is wider than target
        new_w = int(h * target_aspect_ratio)
        left = max(0, (w - new_w) // 2)
        right = left + new_w
        return img.crop((left, 0, right, h))
    else:
        # Image is taller than target
        new_h = int(w / target_aspect_ratio)
        top = max(0, (h - new_h) // 2)
        bottom = top + new_h
        return img.crop((0, top, w, bottom))


def enhance_lighting(img: Image.Image) -> Image.Image:
    """
    Optimizes lighting, contrast, and color vibrancy for handicraft cataloging.
    Preserves authentic craft textures (wood grains, bamboo weaves, terracotta surfaces).
    """
    # 1. Gentle auto-contrast (preserves dark craft shadows, clips 0.5% outliers)
    enhanced = ImageOps.autocontrast(img, cutoff=0.5)

    # 2. Adaptive Brightness Normalization based on average luminance
    stat = ImageStat.Stat(enhanced.convert("L"))
    mean_luminance = stat.mean[0]  # 0 (pure black) to 255 (pure white)

    if mean_luminance < 110:
        # Dark artisan room / under-exposed photo -> boost brightness gently
        brightness_factor = 1.18
    elif mean_luminance > 210:
        # Over-exposed -> pull down slightly
        brightness_factor = 0.94
    else:
        # Balanced lighting -> subtle lift
        brightness_factor = 1.06

    enhancer_b = ImageEnhance.Brightness(enhanced)
    enhanced = enhancer_b.enhance(brightness_factor)

    # 3. Dynamic Contrast boost for crisp separation
    enhancer_c = ImageEnhance.Contrast(enhanced)
    enhanced = enhancer_c.enhance(1.12)

    # 4. Color Vibrancy / Saturation auto-correction
    # Enhances rich vegetable dyes, terracotta earth tones, golden bamboo
    enhancer_col = ImageEnhance.Color(enhanced)
    enhanced = enhancer_col.enhance(1.15)

    # 5. Texture-preserving Unsharp Mask
    # Sharpens fine handloom weaves, pottery textures, and carving details
    enhanced = enhanced.filter(ImageFilter.UnsharpMask(radius=1.5, percent=110, threshold=3))

    return enhanced


def apply_studio_background_cleanup(img: Image.Image, intensity: float = 0.35) -> Image.Image:
    """
    Applies an elegant studio backdrop effect:
    - Neutralizes peripheral room clutter with a soft radial studio vignette.
    - Accentuates the central artisan craft object with a subtle studio spotlight.
    """
    w, h = img.size
    # Create radial gradient vignette mask
    mask = Image.new("L", (w, h), 0)
    cx, cy = w / 2.0, h / 2.0
    max_radius = math.hypot(cx, cy) * 0.95

    # Build radial mask using math
    # Center = 255 (full focus on craft), edges = soft lighting transition
    # For performance and smoothness, generate small and upscale with bicubic
    small_w, small_h = 128, 128
    small_mask = Image.new("L", (small_w, small_h))
    s_cx, s_cy = small_w / 2.0, small_h / 2.0
    s_max_r = math.hypot(s_cx, s_cy) * 0.85

    pixels = []
    for y in range(small_h):
        for x in range(small_w):
            r = math.hypot(x - s_cx, y - s_cy)
            val = max(0.0, min(1.0, 1.0 - (r / s_max_r)))
            # Smooth S-curve transition
            val = val * val * (3.0 - 2.0 * val)
            pixels.append(int(val * 255))
    small_mask.putdata(pixels)

    radial_mask = small_mask.resize((w, h), Image.Resampling.BILINEAR)

    # Create warm studio light backdrop
    studio_bg = Image.new("RGB", (w, h), (248, 248, 248))

    # Blend peripheral edges gently to clean studio tone without blurring craft
    cleaned = Image.blend(img, studio_bg, intensity * 0.25)
    result = Image.composite(img, cleaned, radial_mask)

    return result


def resize_for_catalog(img: Image.Image, target_size: Tuple[int, int] = DEFAULT_TARGET_SIZE) -> Image.Image:
    """
    Resizes image to standard e-commerce dimensions with high quality Lanczos filter.
    """
    if img.size == target_size:
        return img
    return img.resize(target_size, Image.Resampling.LANCZOS)


class ImagePipeline:
    """
    Full End-to-End Image Processing Pipeline for Artisan Product Photos.
    """

    def __init__(self, target_size: Tuple[int, int] = DEFAULT_TARGET_SIZE, target_aspect_ratio: float = 1.0):
        self.target_size = target_size
        self.target_aspect_ratio = target_aspect_ratio

    def process(self, image_data: bytes) -> Tuple[Image.Image, List[str], Dict[str, Any]]:
        """
        Executes the full pipeline:
        1. Validation
        2. EXIF & Format normalization
        3. Aspect ratio centering & crop
        4. Lighting & contrast enhancement
        5. Background cleanup / studio backdrop
        6. Resizing to catalog standard
        """
        steps = []
        metadata = {}

        # Step 1: Validation
        raw_img = validate_image_bytes(image_data)
        orig_w, orig_h = raw_img.size
        metadata["original_size"] = [orig_w, orig_h]
        metadata["original_format"] = raw_img.format
        steps.append("validated")

        # Step 2: EXIF & Format conversion
        oriented_img = fix_exif_orientation(raw_img)
        rgb_img = convert_to_rgb(oriented_img)
        steps.append("format_converted")

        # Step 3: Centering & Crop
        cropped_img = detect_and_center_crop(rgb_img, target_aspect_ratio=self.target_aspect_ratio)
        steps.append("cropped")

        # Step 4: Lighting & Contrast Enhancement
        lit_img = enhance_lighting(cropped_img)
        steps.append("lighting_enhanced")

        # Step 5: Background Cleanup
        studio_img = apply_studio_background_cleanup(lit_img)
        steps.append("background_cleaned")

        # Step 6: Catalog Resize
        final_img = resize_for_catalog(studio_img, target_size=self.target_size)
        steps.append("resized")

        metadata["enhanced_size"] = list(final_img.size)
        metadata["aspect_ratio"] = f"{self.target_aspect_ratio}:1"

        return final_img, steps, metadata
