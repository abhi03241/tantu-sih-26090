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
  - Conforms to standard product schema and REST contract.
- **Test Coverage**: 13 unit/integration tests in `tests/test_vision.py` passing ($100\%$).
- **Visual Demo**: Run `python ai/vision/demo.py` to see side-by-side Before/After transformations on 4 sample artisan crafts (Bamboo, Terracotta, Silk Handloom, Wood Carving).
