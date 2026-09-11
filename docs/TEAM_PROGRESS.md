# TANTU — Team Progress & Module Integration Status

**SIH Problem Statement 26090**: AI-Driven Market Linkage and Smart Cataloging Mobile Application for Marginalized Artisans

---

## Module Status Overview

| Module | Team Member | Branch | Status | Integration Endpoint |
| :--- | :--- | :--- | :--- | :--- |
| **Backend & Core API** | **A** | `feature/A-backend` | ✅ Active / Seeded | `POST /api/products`, `GET /api/products` |
| **Frontend Mobile App** | **P** | `feature/P-frontend` | 🔄 In Progress | Mobile UI & Studio Views |
| **NLP & Storytelling** | **M** | `feature/M-nlp` | ✅ Active | `POST /api/products/{id}/voice`, `/generate-catalogue` |
| **Vision & Image AI** | **R** | `feature/R-image-ai` | ✅ **Completed & Verified** | `POST /api/products/{id}/enhance-image` |
| **Pricing & B2B Feeds** | **S** | `feature/S-pricing` | ✅ Active | `POST /api/products/{id}/price` |
| **Database & Testing** | **Parth** | `feature/Parth-db-test`| ✅ Active | SQLite + Unit Test Suite |

---

## 🎨 Vision & Image AI Module Summary (Team Member R)

- **Owner**: R
- **Branch**: `feature/R-image-ai`
- **Location**: `ai/vision/`
- **Capabilities Delivered**:
  1. **Image Pre-flight Validation**: Strict format, size, and corruption checks for JPEG, PNG, WEBP, BMP.
  2. **Phone Photo Normalization**: Auto-orientation from EXIF and RGBA-to-RGB flattening.
  3. **Auto-Centering & 1:1 Aspect Framing**: Center-crops artisan photos for standard e-commerce catalog squares.
  4. **Dynamic Lighting & Shadow Recovery**: Auto-contrast and luminance balancing designed specifically for dark rural workshops.
  5. **Craft Texture Preservation**: Saturation boost for natural vegetable dyes, terracotta, and bamboo + texture unsharp masking for handloom weaves and wood carvings.
  6. **Studio Background Cleanup**: Soft radial gradient to attenuate room/floor clutter and spotlight the handicraft.
  7. **Standard E-Commerce Resizing**: $1024\times 1024\text{px}$ high-resolution Lanczos output.
  8. **Zero-Crash Resilience**: Resilient `MockImageService` fallback when `MOCK_AI=true` or offline.
- **Contract Compatibility**:
  - Updates `enhanced_image_url` while preserving raw `image_url`.
  - Real-mode assets are now served at `/enhanced/...`; frontend clients should resolve this relative path against the API base URL. Mock mode continues to return remote demo URLs.
  - Conforms to standard product schema and REST contract.
- **Test Coverage**: 18 vision unit/integration tests in `tests/test_vision.py` passing ($100\%$, 28/28 suite total).
- **Visual Demo**: Run `python ai/vision/demo.py` to see side-by-side Before/After transformations on 4 sample artisan crafts (Bamboo, Terracotta, Silk Handloom, Wood Carving).

### ShilpVani Rebranding & Asset Audit Verification (R)

- **Audit Completed**: Verified that existing product image uploads, JPEG/PNG pipelines, adaptive lighting/texture enhancement, collision-safe hashed URLs (`/enhanced/...`), EXIF orientation normalization, and original raw image preservation remain 100% functional.
- **Logo Display**: Confirmed that ShilpVani branding/logo assets can be safely displayed with preserved aspect ratio without distortion or forced non-uniform scaling.
- **Test Results**: All 28 unit and integration tests passing in `<5.0s`.
- **Scope Compliance**: No modifications made to NLP, pricing, database, marketplace, backend architecture, or frontend branding.

### Mobile Camera & Gallery Ingestion Safety Audit (R)

- **Pipeline Verification**: Confirmed complete end-to-end compatibility for mobile camera and gallery captures (`Camera/Gallery -> Frontend image -> Upload API -> Vision Enhancement -> Enhanced Image -> Static Serving & Display`).
- **Validated Checks**:
  - Full JPEG and PNG alpha/transparency support.
  - High-res mobile camera dimension handling ($4032\times 3024$ and up to $8000\times 8000$).
  - EXIF orientation auto-transpose.
  - Universal RGB conversion for all color modes.
  - Base64 Data URL, binary bytes, HTTP/HTTPS URL, and file path upload compatibility.
  - Non-destructive processing with SHA-256 hashed outputs served via `/enhanced` static mount.
  - Frontend display retrieval verified via backend static asset route.
- **Regression Status**: 28/28 tests passing cleanly across vision and core API suites.
