# TANTU — AI Vision & Image Enhancement Studio

> **Problem Statement (SIH 26090)**: AI-Driven Market Linkage and Smart Cataloging Mobile Application for Marginalized Artisans  
> **Module**: AI Vision & Image Studio (`ai/vision/`)  
> **Role / Owner**: Team Member R (Computer Vision / Image AI Developer)

---

## 1. Overview

Artisans often photograph their handcrafted products in dimly lit workshops or home settings using basic smartphones. These photos often suffer from:
- Poor lighting, uneven shadows, or dark background tones
- Workshop/floor clutter distracting from the craft
- Irregular aspect ratios not optimized for modern e-commerce storefronts
- Loss of texture definition (bamboo weaves, pottery carvings, silk zari borders)

The **TANTU AI Vision Studio** transforms these ordinary photographs into **clean, e-commerce-ready, high-resolution catalog images** in milliseconds, preserving authentic craft textures while removing clutter and standardizing framing.

---

## 2. Image Processing Pipeline

```
Raw Artisan Photograph (JPEG / PNG / WEBP)
           │
           ▼
1. Validation & Integrity Check
   - Magic bytes verification, size boundaries (50px to 8000px)
           │
           ▼
2. Format & EXIF Normalization
   - Phone camera orientation auto-correction
   - Alpha channel / RGBA to RGB conversion
           │
           ▼
3. Centering & Aspect Ratio Crop
   - Centers the product with standard 1:1 catalog aspect ratio
           │
           ▼
4. Dynamic Lighting & Texture Enhancement
   - Auto-contrast & shadow recovery
   - Color vibrancy boost (highlights natural dyes & wood/terracotta tones)
   - Unsharp mask sharpening (preserves handloom weaves & textures)
           │
           ▼
5. Background Cleanup & Studio Backdrop
   - Peripheral noise and clutter attenuation via soft radial studio gradient
   - Focus spotlight on the artisan craft
           │
           ▼
6. Resizing & E-Commerce Ready Output
   - High-fidelity Lanczos resampling to standard 1024x1024 resolution
   - High-quality JPEG/PNG artifact generation
```

---

## 3. Architecture & Service Interface

The module uses a clean, decoupled service architecture:

```
                  ┌───────────────────────────────┐
                  │       BaseImageService        │
                  │   (Abstract Service Interface)│
                  └───────────────┬───────────────┘
                                  │
                 ┌────────────────┴────────────────┐
                 │                                 │
                 ▼                                 ▼
   ┌───────────────────────────┐     ┌───────────────────────────┐
   │     RealImageService      │     │     MockImageService      │
   │  - End-to-end CV Pipeline │     │  - Fast, zero-crash demo  │
   │  - PIL image algorithms   │     │  - Resilient SIH fallback │
   └───────────────────────────┘     └───────────────────────────┘
```

### Factory Function

```python
from ai.vision import get_image_enhancement_service, enhance_artisan_image

# Retrieve service instance based on environment or toggle
service = get_image_enhancement_service(mock=False)
result = service.enhance_image("path/to/bamboo_basket.jpg")
```

### High-Level API Facade

```python
from ai.vision import enhance_artisan_image

response = enhance_artisan_image(
    image_url="https://example.com/artisan_photo.jpg",
    prompt="Clean studio backdrop with warm lighting",
    mock=False
)
```

---

## 4. Output Contract

Compatible with both TANTU REST API contracts and frontend requirements:

```json
{
  "original_image_url": "ai/vision/samples/bamboo_basket.jpg",
  "enhanced_image_url": "ai/vision/output/enhanced_studio_eda02ad75e.jpg",
  "status": "success",
  "mock_mode": false,
  "processing_steps": [
    "validated",
    "format_converted",
    "cropped",
    "lighting_enhanced",
    "background_cleaned",
    "resized"
  ],
  "enhancements_applied": [
    "Background clutter removal & studio lighting",
    "Dynamic contrast & exposure correction",
    "Authentic handicraft texture sharpening",
    "Catalogue framing & resize (1024x1024)"
  ],
  "confidence_score": 0.95,
  "metadata": {
    "original_size": [800, 600],
    "enhanced_size": [1024, 1024],
    "aspect_ratio": "1:1",
    "original_format": "JPEG"
  }
}
```

---

## 5. Mock Mode & Fail-Safe Resilience

Set the environment variable:

```bash
MOCK_AI=true
```

In mock mode:
- Instantly returns high-resolution studio-grade catalog photographs mapped to the product craft type.
- Ensures **100% zero-crash guarantee** during live stage presentations even without an internet connection or if third-party endpoints fail.
- Real pipeline automatically fails over to mock mode if an unrecoverable input error is encountered during demo execution.

---

## 6. Supported Formats & Limits

| Parameter | Supported Values |
| :--- | :--- |
| **Input Formats** | JPEG (`.jpg`, `.jpeg`), PNG (`.png`), WEBP (`.webp`), BMP (`.bmp`), TIFF (`.tiff`) |
| **Output Formats** | JPEG (standardized RGB, `q=92`), PNG |
| **Min Resolution** | 50 x 50 px |
| **Max Resolution** | 8000 x 8000 px |
| **Color Modes** | RGB, RGBA (transparency flattened with clean backdrop), Grayscale, CMYK, Palette |

---

## 7. Sample Products & Demonstration

Sample test images are provided in `ai/vision/samples/`:
1. **North-East Bamboo Utility Basket** (`bamboo_basket.jpg`)
2. **Handcrafted Terracotta Diya Pot** (`terracotta_pottery.jpg`)
3. **Chanderi Handloom Silk Dupatta** (`handwoven_textile.jpg`)
4. **Saharanpur Carved Wooden Elephant** (`wooden_handicraft.png`)

### Running the Demo

```bash
python ai/vision/demo.py
```

This processes all sample products, prints benchmark processing times (~150-200ms per image), and produces side-by-side comparison images in `ai/vision/output/`.

---

## 8. Running Unit Tests

```bash
# Run Vision tests
python -m unittest tests/test_vision.py

# Run all project tests
python -m unittest discover tests
```

---

## 9. Dependencies

- `Pillow>=10.0.0` (Core computer vision & image processing)
- `fastapi` & `pydantic` (REST endpoint schemas & integration)
- `httpx` & `requests` (Network fetching)

---

## 10. Limitations & Future Scope

- **Edge Devices**: The current local pipeline is optimized for lightweight CPU execution (<200ms), making it easily deployable on modest cloud instances or embedded edge servers.
- **Segment Anything / Rembg**: For high-end cloud deployments with dedicated GPUs, an optional neural background segmentation node can be plugged into `BaseImageService` without altering backend or frontend integration contracts.
