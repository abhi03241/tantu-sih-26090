# TANTU — Vision & Image Enhancement Task Log (R)

**Developer**: Team Member R (Computer Vision & AI Image Enhancement)  
**Project**: TANTU — AI-Driven Market Linkage & Smart Cataloging for Marginalized Artisans  
**SIH Problem Statement**: 26090  
**Branch**: `feature/R-image-ai`

---

## Checkpoint 1: Image Validation & Pre-flight Integrity Checks

* **What Changed**:
  - Implemented strict pre-flight validation in `ai/vision/pipeline.py` (`validate_image_bytes`).
  - Added magic-byte inspection, format verification (`JPEG`, `PNG`, `WEBP`, `BMP`, `TIFF`), and dimensional boundary enforcement ($50\times 50\text{px}$ to $8000\times 8000\text{px}$).
  - Handled corrupted byte streams, truncated files, and non-image payloads by raising `ImageValidationError`.
* **Files**:
  - `ai/vision/pipeline.py`
  - `tests/test_vision.py` (`test_01`, `test_02`, `test_03`, `test_04`, `test_05`, `test_06`)
* **Image Processing Method**: `PIL.Image.open` + `Image.verify` + Header analysis.
* **API / Interface**: `validate_image_bytes(image_data: bytes, min_dims, max_dims) -> PIL.Image.Image`.
* **Tests Performed**: Valid JPG, valid PNG with alpha, corrupted binary strings, $<50\text{px}$ image, $>3000\text{px}$ image, and non-image PDF bytes.
* **Results**: All validation tests passed cleanly without throwing unhandled exceptions.
* **Issues Encountered**: `PIL.Image.verify()` closes file stream in memory; resolved by re-initializing byte stream for subsequent pipeline stages.
* **Integration Notes**: Shared with backend routers to guarantee input sanitization.

---

## Checkpoint 2: Basic Image Enhancement & Lighting Recovery

* **What Changed**:
  - Implemented EXIF rotation auto-correction for smartphone photos (`fix_exif_orientation`).
  - Converted multi-channel / palette images (`RGBA`, `LA`, `P`, `CMYK`) to standardized `RGB` (`convert_to_rgb`).
  - Implemented dynamic lighting enhancement (`enhance_lighting`):
    - Histogram-adaptive auto-contrast (`ImageOps.autocontrast`) clipping $0.5\%$ outliers.
    - Mean-luminance calculation with shadow-lifting for dark artisan workshops.
    - Saturation/color vibrancy boost ($+15\%$) for vegetable dyes, bamboo gold, and terracotta.
    - Mild texture-preserving unsharp masking (radius=1.5, percent=110, threshold=3) to highlight handloom weaves and wood grains.
* **Files**:
  - `ai/vision/pipeline.py`
* **Image Processing Method**: Adaptive luminance estimation, PIL `ImageEnhance` (`Brightness`, `Contrast`, `Color`), and `ImageFilter.UnsharpMask`.
* **API / Interface**: `enhance_lighting(img: PIL.Image.Image) -> PIL.Image.Image`.
* **Tests Performed**: Verified contrast lift, shadow recovery, and texture preservation on sample artisan crafts.
* **Results**: Noticeable visual transformation without destroying natural craft textures or introducing pixelation.

---

## Checkpoint 3: Product Presentation & E-Commerce Framing

* **What Changed**:
  - Implemented auto-centering and aspect ratio crop (`detect_and_center_crop`) to deliver standardized $1:1$ catalog aspect ratio.
  - Implemented studio background cleanup (`apply_studio_background_cleanup`) applying a soft radial studio gradient to diminish peripheral room/floor clutter.
  - Implemented high-resolution e-commerce catalog resizing (`resize_for_catalog`) to $1024\times 1024\text{px}$ via `Image.Resampling.LANCZOS`.
* **Files**:
  - `ai/vision/pipeline.py`
  - `ai/vision/demo.py`
* **Image Processing Method**: Bilinear radial mask attenuation, Lanczos resampling, S-curve center spotlight blending.
* **API / Interface**: `ImagePipeline.process(image_data: bytes) -> Tuple[Image, List[str], Dict[str, Any]]`.
* **Tests Performed**: Processed bamboo basket, pottery, textile, and wood carving samples.
* **Results**: Consistent $1024\times 1024$ output artifacts generated in $\sim 150-200\text{ms}$.

---

## Checkpoint 4: Original vs. Enhanced Image Separation

* **What Changed**:
  - Ensured original image is never modified or overwritten.
  - Enhanced images are saved to separate artifact storage (`data/enhanced/` or designated output directory) with hash-based unique filenames (`enhanced_studio_<hash>.jpg`).
  - Response contract strictly distinguishes `original_image_url` and `enhanced_image_url`.
  - Built side-by-side Before vs. After composite generator in `ai/vision/demo.py`.
* **Files**:
  - `ai/vision/services.py`
  - `ai/vision/demo.py`
  - `tests/test_vision.py` (`test_12_original_preservation`)
* **Image Processing Method**: Non-destructive file I/O with SHA/MD5 asset naming.
* **API / Interface**:
  ```json
  {
    "original_image_url": "path/or/url/to/raw.jpg",
    "enhanced_image_url": "path/or/url/to/enhanced.jpg",
    "status": "success",
    "processing_steps": ["validated", "format_converted", "cropped", "lighting_enhanced", "background_cleaned", "resized"]
  }
  ```
* **Tests Performed**: Asserted original file byte comparison before and after enhancement execution.
* **Results**: Verified $100\%$ preservation of raw artisan originals.

---

## Checkpoint 5: Failure Handling & Resilience Fallback

* **What Changed**:
  - Implemented `MockImageService` providing fast, zero-crash responses for demo resilience.
  - Added automatic failover in `enhance_artisan_image`: If real local processing encounters network timeout or corrupt input during live presentations, it automatically recovers with mock mode and attaches an informative warning.
  - Provided `MOCK_AI=true` environment variable support.
* **Files**:
  - `ai/vision/services.py`
  - `ai/vision/image_enhancer.py`
  - `tests/test_vision.py` (`test_11_missing_or_empty_input`, `test_13_failure_handling_and_fallback`)
* **Image Processing Method**: Safe exception encapsulation, fallback service routing.
* **API / Interface**: `get_image_enhancement_service(mock: bool) -> BaseImageService`.
* **Tests Performed**: Empty strings, `None` values, non-existent URLs, unreadable file paths.
* **Results**: Zero server crashes, structured error/fallback JSON returned.

---

## Checkpoint 6: Full Test Suite & End-to-End Verification

* **What Changed**:
  - Added 13 comprehensive unit and integration tests in `tests/test_vision.py`.
  - Verified interoperability with `backend/app/routers/ai_endpoints.py` (`POST /api/products/{id}/enhance-image`).
  - Created 4 synthetic test craft datasets in `ai/vision/samples/`.
* **Files**:
  - `tests/test_vision.py`
  - `ai/vision/samples_generator.py`
  - `ai/vision/demo.py`
* **Tests Performed**:
  - `test_01_valid_jpeg`: PASSED
  - `test_02_valid_png`: PASSED
  - `test_03_invalid_corrupted_image`: PASSED
  - `test_04_extremely_small_image`: PASSED
  - `test_05_large_high_resolution_image`: PASSED
  - `test_06_unsupported_format`: PASSED
  - `test_07_mock_image_service`: PASSED
  - `test_08_service_factory`: PASSED
  - `test_09_high_level_enhance_function`: PASSED
  - `test_10_api_integration_endpoint`: PASSED
  - `test_11_missing_or_empty_input`: PASSED
  - `test_12_original_preservation`: PASSED
  - `test_13_failure_handling_and_fallback`: PASSED
  - Full suite (`python -m unittest discover tests`): 20/20 PASSED.
* **Results**: All 20 tests in repository passing in $<2.0\text{s}$.
