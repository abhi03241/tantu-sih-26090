"""
Interactive Demo Script for TANTU AI Vision Studio.
Maintained by Team Member R (AI Image Enhancement).

Runs the end-to-end image processing pipeline across artisan handicraft sample images:
1. Bamboo Basket
2. Terracotta Pottery
3. Handwoven Silk Textile
4. Wooden Handicraft Carving

Produces side-by-side Before/After comparisons and outputs JSON contracts.
"""

import os
import sys
import json
import time
from PIL import Image, ImageDraw, ImageFont

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from ai.vision.image_enhancer import enhance_artisan_image
from ai.vision.services import RealImageService, MockImageService
from ai.vision.samples_generator import create_sample_images


def create_side_by_side_comparison(before_path: str, after_path: str, title: str, output_path: str):
    """
    Stitches Before and After photos together with clean labels for SIH demo presentations.
    """
    img_before = Image.open(before_path)
    img_after = Image.open(after_path)

    # Standardize height for comparison
    h = 600
    w_b = int(img_before.width * (h / img_before.height))
    w_a = int(img_after.width * (h / img_after.height))

    img_b_resized = img_before.resize((w_b, h), Image.Resampling.LANCZOS)
    img_a_resized = img_after.resize((w_a, h), Image.Resampling.LANCZOS)

    header_h = 70
    canvas_w = w_b + w_a + 20
    canvas_h = h + header_h + 20

    canvas = Image.new("RGB", (canvas_w, canvas_h), (245, 245, 247))
    draw = ImageDraw.Draw(canvas)

    # Paste images
    canvas.paste(img_b_resized, (10, header_h))
    canvas.paste(img_a_resized, (w_b + 10, header_h))

    # Draw titles and tags
    draw.rectangle([10, 10, canvas_w - 10, header_h - 10], fill=(28, 37, 54))
    draw.text((25, 25), f"TANTU Studio AI - {title}", fill=(255, 255, 255))
    draw.text((w_b - 120, 25), "[ ORIGINAL RAW ]", fill=(255, 180, 100))
    draw.text((canvas_w - 200, 25), "[ TANTU ENHANCED ]", fill=(100, 230, 150))

    canvas.save(output_path, "JPEG", quality=92)
    return output_path


def run_demo():
    print("=" * 70)
    print("      TANTU AI VISION STUDIO — ARTISAN IMAGE ENHANCER DEMO      ")
    print("=" * 70)

    samples_dir = os.path.join(os.path.dirname(__file__), "samples")
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    sample_files = [
        ("bamboo_basket.jpg", "North-East Bamboo Utility Basket"),
        ("terracotta_pottery.jpg", "Handcrafted Terracotta Diya Pot"),
        ("handwoven_textile.jpg", "Chanderi Handloom Silk Dupatta"),
        ("wooden_handicraft.png", "Saharanpur Carved Wooden Elephant")
    ]

    # Ensure samples exist
    if not all(os.path.exists(os.path.join(samples_dir, f[0])) for f in sample_files):
        create_sample_images(samples_dir)

    results = []

    for filename, label in sample_files:
        raw_path = os.path.join(samples_dir, filename)
        print(f"\n[+] Processing: {label} ({filename})")
        t0 = time.time()

        # Run Real local pipeline
        res = enhance_artisan_image(
            image_url=raw_path,
            prompt="Clean professional catalog studio backdrop with warm accent lighting",
            mock=False,
            output_dir=output_dir
        )
        elapsed_ms = (time.time() - t0) * 1000

        print(f"    Status: {res['status']}")
        print(f"    Processing Time: {elapsed_ms:.2f} ms")
        print(f"    Steps Applied: {', '.join(res.get('processing_steps', []))}")
        print(f"    Enhanced Output: {res['enhanced_image_url']}")

        # Generate comparison canvas
        if res.get("enhanced_image_url") and os.path.exists(res["enhanced_image_url"]):
            comp_path = os.path.join(output_dir, f"comparison_{os.path.splitext(filename)[0]}.jpg")
            create_side_by_side_comparison(raw_path, res["enhanced_image_url"], label, comp_path)
            print(f"    Side-by-side Demo saved: {comp_path}")

        results.append({
            "product": label,
            "filename": filename,
            "time_ms": round(elapsed_ms, 2),
            "result": res
        })

    # Test Fallback / Mock Mode
    print("\n" + "-" * 70)
    print("[*] Testing Mock Mode / Fallback Resilience (MOCK_AI=True)...")
    mock_res = enhance_artisan_image(
        image_url="https://images.unsplash.com/photo-1590736969955-71cc94801759",
        mock=True
    )
    print(f"    Mock Status: {mock_res['status']}")
    print(f"    Mock Enhanced URL: {mock_res['enhanced_image_url']}")
    print(f"    Confidence Score: {mock_res['confidence_score']}")
    print("-" * 70)

    print("\n[SUCCESS] AI Vision enhancement demo completed successfully!")
    return results


if __name__ == "__main__":
    run_demo()
