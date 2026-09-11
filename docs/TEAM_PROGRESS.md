# TANTU Team Progress & Integration Status

This document tracks team member status, backend readiness, and integration contracts for **TANTU** (SIH 26090).

---

## A — Current Status (Tech Lead + Backend + Integration)

* **Current Branch**: `feature/A-backend`
* **Latest Commit Hash**: `3bb68f930d8af226c342b3fa20c03359b52d6baf`
* **Latest Commit Message**: `test: validate integrated TANTU workflow`
* **Backend Status**: **`INTEGRATED & REBRANDED FOR DEMO`** — Core architecture, SQLite database persistence, REST API routes, AI service abstraction layer, full artisan processing flow, and ShilpVani user-facing rebranding are fully implemented, integrated, and verified.
* **Test Results**: **`34/34 PASSED (0 Failed)`** (`tests/test_api.py`, `tests/test_integration.py`, `tests/test_vision.py`).
* **Mock AI Mode**: **`MOCK_AI=true` fully working**. Guarantees 100% demo resilience during live SIH evaluation without external API keys.

### 2026-09-06 — Backend Integration Audit (A)

* **Frontend upload compatibility resolved**: `POST /api/products/{id}/upload-image` now accepts both the documented multipart file upload and the JSON `image_url` payload used by P's frontend branch.
* **Marketplace guard**: `POST /api/orders/request` now rejects draft/processing products with `409`; buyer order requests are restricted to published catalogue entries.
* **Order-status compatibility**: the existing `new_status` query parameter remains supported and a JSON `{ "status": "accepted" }` body is now also supported. Valid values are `pending`, `accepted`, `fulfilled`, and `rejected`.
* **Branch review finding**: M, R, S, P, and Parth branches each include broad edits to shared backend files, including removals of the current orchestration layer in some branches. Do not merge those backend paths wholesale; integrate their AI/frontend modules selectively against this API contract.
* **Environment note**: the current handoff workstation has no Python executable or launcher on PATH, so the backend test suite cannot be executed here until Python 3.10+ is installed/available.

### 2026-09-06 — Controlled Six-Branch Integration (A)

* **Integrated commits**: P `0d2c1d4`, `74c8c97`; M package through `a78a4ce`; R package through `b473655`; S package through `5a5927b`. Parth's regression findings were incorporated as test coverage; its overlapping backend/database rewrites were not merged.
* **Conflict resolution**: P's shared-log conflict was resolved in favor of this up-to-date integration log; P's latest wizard and task log were retained. Shared backend files from M/R/S/Parth were intentionally not merged wholesale.
* **NLP**: the A wrapper now uses M's grounded bilingual pipeline. Voice extraction persists stated dimensions and production time; catalogue requests pass `raw_notes` to NLP.
* **Vision**: R's validation/enhancement pipeline is integrated. `/enhanced` serves collision-safe real-mode output, and A maps stored `/uploads/...` URLs to local files for real processing.
* **Pricing**: S's fair-wage, demo-reference pricing package is integrated. Product pricing now receives `labor_hours`, cost, overhead, quantity, and region; `POST /api/pricing/estimate` and `/reference-data` are available.
* **Frontend**: P's React/Vite UI is integrated. The lifecycle constant was restored for a successful build, and order status changes call the live `PATCH /api/orders/{id}/status` API before using offline fallback.
* **Verification**: `npm ci` completed with 0 vulnerabilities; `npm run build` passed (1609 modules). `git diff --check` passed. Python backend tests remain blocked because no Python runtime, launcher, or package manager is installed on this workstation.

### 2026-09-06 — Final Validation (A)

* **Python**: installed and used CPython `3.12.10` with a repository-local `.venv`; dependencies were installed unchanged from `backend/requirements.txt`.
* **Backend suite**: **17/17 passed**, 0 failed, 0 skipped (`python -m unittest discover -s tests -p "test_*.py" -v`). A first run exposed a test-data assumption: `test_10_order_requests` chose an arbitrary product, which may be unpublished in persistent SQLite state. It now deliberately selects a published buyer-catalogue product, matching the API rule.
* **E2E coverage**: passed artisan draft → upload → voice/NLP → enhancement → catalogue → pricing → publish → buyer feed → bulk order → accepted status, plus unpublished-order rejection, JSON upload/status compatibility, and NLP/pricing persistence checks.
* **Frontend**: `npm run build` passed again (1609 modules).
* **Image verification**: automated upload/enhancement checks passed. A real-mode local `/uploads` image produced `/enhanced/enhanced_studio_c3fe4619f31888b1.jpg`; the mounted URL returned `200 image/jpeg`.

### 2026-09-11 — ShilpVani Rebranding & Final Integrated Validation (A)

* **Integrated commits**: P `d72af52`, `976593e`; M `b92cc31`, `453946d`, `ae745db`; R `8cca92e`, `2f395b7`; S `7fb2bb9`, `e61ae72`, `be879aa`; Parth `0cd52e9`.
* **Rebranding**: Successfully integrated user-facing TANTU → ShilpVani / शिल्पवाणी rebranding across UI headers, title tags, language selector, `ShilpVaniLogo.jsx`, and constants. Internal storage keys and technical contracts preserved.
* **Build & Tests**: `npm run build` passed (1610 modules, 0 errors). Backend & integration unittest suite: **34/34 passed** (0 failed, 0 skipped).


---

### Implemented REST APIs

| Category | HTTP Method | Endpoint | Description |
|---|---|---|---|
| **Products** | `POST` | `/api/products` | Create new draft product session |
| | `GET` | `/api/products` | List all products (with category, artisan, query, status filters) |
| | `GET` | `/api/products/{id}` | Get complete product object by ID |
| | `GET` | `/api/products/{id}/status` | Get processing status (`draft`, `processing`, `ready`, `published`, `failed`) |
| | `POST` | `/api/products/{id}/upload-image` | Upload local product photo (`JPG`, `PNG`, `WEBP`) |
| | `POST` | `/api/products/{id}/voice` | Process natural language voice description |
| | `POST` | `/api/products/{id}/process` | **End-to-End AI Orchestrator Pipeline** (Photo + Voice -> NLP -> Vision -> Pricing -> DB) |
| | `PUT` | `/api/products/{id}` | Edit & update catalogue attributes |
| | `PATCH` | `/api/products/{id}/publish` | Transition status from `draft`/`ready` -> `published` |
| | `DELETE` | `/api/products/{id}` | Delete product listing by ID |
| **Artisan** | `GET` | `/api/artisan/products` | Retrieve artisan dashboard product catalog |
| | `GET` | `/api/artisan/profile/{id}` | Retrieve artisan profile details |
| | `POST` | `/api/artisan/profile` | Create/update artisan profile |
| **Buyer** | `GET` | `/api/buyer/products` | Retrieve published buyer marketplace product feed |
| | `GET` | `/api/buyer/profile/{id}` | Retrieve buyer organization profile |
| | `POST` | `/api/buyer/profile` | Create/update buyer profile |
| **B2B Orders**| `POST` | `/api/orders/request` | Submit bulk B2B order request to artisan |
| | `GET` | `/api/orders` | List order requests submitted by buyers |
| | `GET` | `/api/orders/{id}` | Retrieve single order request |
| | `PATCH` | `/api/orders/{id}/status` | Update order request status (`pending`, `accepted`, `fulfilled`, `rejected`) |

---

### AI Service Integration Layer

| Service Class | File Path | Targeted Submodule | Responsibilities |
|---|---|---|---|
| **`NLPService`** | `backend/app/services/nlp_service.py` | `ai/nlp/voice_and_story.py` (Member M) | Voice-to-text, bilingual copy, sentiment analysis, cultural storytelling |
| **`VisionService`** | `backend/app/services/vision_service.py` | `ai/vision/image_enhancer.py` (Member R) | Background clutter removal, studio lighting, upscaling |
| **`PricingService`** | `backend/app/services/pricing_service.py` | `ai/pricing/smart_pricing.py` (Member S) | Material cost-plus algorithm, labor duration, fair price bounds |
| **`ProductPipelineOrchestrator`** | `backend/app/services/orchestrator.py` | Full Pipeline | Orchestrates multi-stage AI workflow with error isolation |

---

### Integration Guide for Team Members

#### 📱 P — Frontend / Mobile UI
- Launch server locally: `python -m backend.app.main` (starts at `http://localhost:8000`).
- Explore interactive API docs: `http://localhost:8000/docs`.
- Standard Artisan Workflow:
  1. Call `POST /api/products` to initialize draft session.
  2. Call `POST /api/products/{id}/upload-image` with image file.
  3. Call `POST /api/products/{id}/process` with voice transcript to run complete AI cataloging.
  4. Call `PUT /api/products/{id}` if artisan edits catalogue fields.
  5. Call `PATCH /api/products/{id}/publish` to publish to marketplace.
- Buyer Feed: Call `GET /api/buyer/products` to fetch published marketplace items.

#### 🎙️ M — AI / NLP / Voice / Sentiment
- Update functions in `ai/nlp/voice_and_story.py`:
  - `process_voice_transcript(transcript, language, mock)`
  - `generate_catalogue_nlp(product_info, mock)`
- `NLPService` automatically routes calls to your code when `MOCK_AI=false`.

#### 🖼️ R — Computer Vision / Image Enhancement
- Update function in `ai/vision/image_enhancer.py`:
  - `enhance_artisan_image(image_url, prompt, mock)`
- `VisionService` automatically routes raw product photo URLs to your model output when `MOCK_AI=false`.

#### 💰 S — Dynamic Pricing & B2B Marketplace
- Update function in `ai/pricing/smart_pricing.py`:
  - `calculate_smart_price(category, material, production_time, dimensions, raw_material_cost, mock)`
- `PricingService` automatically feeds your pricing outputs to product responses and B2B order calculations.

#### 🧪 Parth — Database, Testing & Integration Support
- Test suite location: `tests/` (`test_api.py` and `test_integration.py`). Run with `python -m unittest discover -s tests`.
- Database file: `backend/tantu.db` (SQLite). Schema and repositories located in `backend/app/database.py`.

---

### 2026-09-11 — Targeted Frontend QA Fixes (A, covering for unavailable P)

**P was unavailable for this session. A applied only the four targeted fixes from Parth QA report.**
No backend, database, API, NLP, vision, or pricing code was modified.

#### Issue 1 — Sample Craft Image [FIXED]
- Unsplash wristwatch photo (1590736969955-71cc94801759) replaced with bamboo basket (1558618666-fcd25c85cd64).
- File: frontend/src/constants/categories.js

#### Issue 2 — Hardcoded Language Strings [FIXED]
- ArtisanOrdersList.jsx: filter tab labels (All/Pending/Accepted) now use t() — responds to language switch.
- BuyerHome.jsx: hero badge, title, subtitle, search placeholder, catalogue label, empty state,
  price label, and bulk button now use t() — responds to language switch.
- languages.js: added filterAll/filterPending/filterAccepted + 10 buyer* keys to hi and en dicts.
- M can extend to bn/mr/as/ta/te by adding these keys to those language entries when ready.

#### Issue 3 — Camera capture=environment [FIXED]
- AddProductWizard.jsx now has two separate hidden inputs:
  cameraInputRef (capture=environment) for Camera button,
  fileInputRef (no capture) for Gallery button.
- Desktop file picker, gallery, preview, upload, and image enhancement all unaffected.

#### Issue 4 — Bottom Nav Clipping at 375px [FIXED]
- index.css: flex-shrink:0 on .bottom-nav, min-height:0 on .app-main-content,
  padding-bottom:18px on .device-mode .bottom-nav.

#### Verification
- npm run build: 1610 modules, 0 errors (exit 0).
- git diff --check: Passed.
- Backend unittest suite: 34/34 passed (unchanged).
- 6 frontend files changed, 0 backend files changed.
### M — ShilpVani Language Selector & Grounded NLP Finalization (2026-09-11)
- Verified active presence of all 7 target languages in the language selector (`LanguageSelection.jsx` and `Header.jsx`).
- Connected native speech recognition locales (`en-IN`, `hi-IN`, `bn-IN`, `mr-IN`, `as-IN`, `ta-IN`, `te-IN`) to `AddProductWizard.jsx`.
- Added regional voice transcripts for all 4 demo sample crafts in `DEMO_SAMPLE_CRAFTS`.
- Fixed keyword boundary matching in `demo_data.py` (`_match_any_keyword`) to eliminate false-positive substring cues in Indic scripts (e.g., `মা` in `মাটির`).
- Verified ephemeral wizard drafts (`new-draft`) in `/api/products/{id}/voice` and `/api/products/{id}/generate-catalogue` for seamless offline/online frontend flow.
- Verified test suite: **37/37 tests passed** (11 backend API tests + 26 NLP pipeline tests).
- Verified production build: `npm run build` in `frontend/` succeeds with **0 errors**.
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

### QA Sign-off & Vision Pipeline Status (R)

- **Parth's QA Audit**: Vision pipeline confirmed operational and production-ready.
- **Frontend Camera Note**: Generic file input on frontend camera UI acknowledged and tracked under Team Member P's frontend tasks.
- **Scope Compliance**: No changes made to frontend language selector, NLP, pricing, marketplace, orders, or database.

---

### Final Master Integration (A) — 2026-09-11

- **Integrated Branch**: `feature/A-backend`
- **Integrated Commits**:
  - `f53ffbd`: A's frontend QA fixes (sample image, language strings, camera capture, bottom nav clipping)
  - `4b71103`: M's ShilpVani 7-language selector & voice transcript integration
  - `8b9137d`: R's vision QA sign-off
- **Multilingual & NLP Fixes**: Updated `demo_data.py` with 7-language script recognition (Devanagari `hi`/`mr`, Bengali `bn`, Assamese `as`, Tamil `ta`, Telugu `te`, English `en`), Indic digit normalization (`0-9`, Devanagari, Bengali, Tamil, Telugu), Indic duration units, and material catalog keywords.
- **Final Test Verification**: **61/61 backend unit & integration tests passed (0 failed, 0 skipped)** (`python -m unittest discover -s tests -p "test_*.py"`).
- **Final Frontend Build**: `npm run build` succeeded with **0 errors** (1610 modules transformed).
- **Status**: **PASS — Integrated & Production Ready**.

---

### Final Pricing, Marketplace & Order QA Sign-off (S) — 2026-09-12

- **Target Commit Tested**: `f7a95b3431aa4b83758fae01f70ac472c2e25318`
- **Branch**: `feature/A-backend`
- **Scope Verified**:
  - **Dynamic Pricing**: Numeric `min < max`, cost/labor hours breakdown wired properly, negative inputs rejected (422), volume discount & regional multiplier working, output labeled as "AI-assisted suggested price range" with demo disclaimer (no claim of guaranteed market truth).
  - **Buyer Marketplace**: Only published products appear; draft/processing products strictly hidden. Product cards load with category/region tags. Product detail (`GET /api/products/{id}`) and image routing (/uploads, /enhanced) verified.
  - **Bulk Orders**: B2B bulk orders submit cleanly (`POST /api/orders/request`), draft/processing orders rejected (409 Conflict), quantity <= 0 rejected (422), order persisted and retrievable by ID.
  - **Order Status**: Status updates persist (`pending` -> `accepted` -> `fulfilled`), reload resilience confirmed.
  - **Mobile Layout**: Responsive at 375×667 and 390×844 with fluid max-width 480px and bottom sheet modal.
- **Fix Applied**: Added `"completed"` and `"requested"` to `OrderStatus` schema in `backend/app/schemas.py` to support legacy records without 500 `ResponseValidationError`.
- **Test Results**: **61/61 unit and integration tests passed (100%)** (`python -m unittest discover -s tests -p "test_*.py"`).
- **Status**: **PASS — DEMO-READY**.

---

### M — ShilpVani 7-Language Selector Verification & QA Resolution (2026-09-12)
- Re-verified all 7 target languages in `LANGUAGES` array (`frontend/src/constants/languages.js`): English (`en`), Hindi (`hi`), Bengali (`bn`), Marathi (`mr`), Assamese (`as`), Tamil (`ta`), Telugu (`te`).
- Verified selector displays all 7 languages in `LanguageSelection.jsx` (2-column mobile card grid) and `Header.jsx` (dropdown language menu).
- Cleaned language selection flow in `AppContext.jsx` to prevent premature unmounting when browsing languages.
- Added automated contract regression test `test_frontend_languages_selector_contract` in `tests/test_nlp_pipeline.py`.
- Automated test results: **38/38 tests passed**.
- Frontend production build: `npm run build` succeeds in 2.79s with **0 errors**.

---

### Final Master Integration & 7-Language Verification (A) — 2026-09-12

- **Target Commit Integrated**: `c4870ad` (`fix: complete ShilpVani language selector`)
- **Branch**: `feature/A-backend`
- **Scope Verified**:
  - **7-Language Selector**: English (`en`), Hindi (`hi`), Bengali (`bn`), Marathi (`mr`), Assamese (`as`), Tamil (`ta`), Telugu (`te`) fully verified across constants, translation maps, mobile UI grid (`LanguageSelection.jsx`), and header menu (`Header.jsx`).
  - **Preservation of A/R/S/M/Parth Functionality**: Vision enhancement, dynamic pricing, B2B order lifecycle, FastAPI router endpoints, SQLite database models, and multilingual NLP parsing remain 100% operational.
- **Backend Test Results**: **62/62 tests passed (100%)** (`python -m unittest discover -s tests -p "test_*.py"`).
- **Frontend Build Results**: `npm run build` completed in **1.46s with 0 errors** (1610 modules transformed).
- **Git Diff & Whitespace Check**: `git diff --check` passed cleanly with **0 issues**.
- **Status**: **PASS — 100% INTEGRATED & DEMO-READY**.

---

### Final Documentation, Official Logo & Team Credits Finalization — 2026-09-12

- **Branch**: `feature/A-backend`
- **Scope Completed**:
  - **Official Logo Component**: Integrated attached official ShilpVani logo into `ShilpVaniLogo.jsx`, `frontend/public/shilpvani_logo.jpg`, `docs/assets/shilpvani_logo.jpg`, and updated favicon link in `index.html`.
  - **User-Facing Branding Audit**: Replaced all obsolete user-facing `TANTU` / `KarigarAI` strings across all 7 language dictionaries in `frontend/src/constants/languages.js` with `ShilpVani` / `शिल्पवाणी`.
  - **README Update**: Overhauled `README.md` with problem statement, solution workflow (`Craft → Voice → AI → Catalogue → Pricing → Buyer → Bulk Order`), 7 supported languages list, AI pipeline roles, B2B marketplace scope, tech stack, structure, setup guide, testing results, and future roadmap.
  - **Official Team Credits**:
    - **A**: Abhishek Shukla (Tech Lead + Backend + Integration)
    - **P**: Pratistha (Frontend / Mobile UI)
    - **M**: Manyata (AI/NLP + Voice + Multilingual Intelligence)
    - **R**: Raj (Computer Vision + Image Enhancement)
    - **S**: Sanskriti (Dynamic Pricing + B2B Marketplace)
    - **Parth**: Parth (Database + Testing + QA / Integration Support)
- **Backend Test Suite**: **62/62 PASSED (100%)**
- **Frontend Build**: `npm run build --prefix frontend` **PASSED** (1610 modules transformed, 0 errors).
- **Git Check**: `git diff --check` **PASSED** (0 formatting/whitespace issues).
- **Status**: **PASS — SIH 2026 FINALIZED**.

---

### Multilingual Voice-First AI Positioning & Vercel Deployment — 2026-09-12

- **Branch**: `feature/A-backend`
- **Scope Completed**:
  - **Multilingual AI Platform Positioning**: Reframed product framing around *"We don't ask artisans to learn e-commerce. We use AI to make e-commerce understand artisans."* Positioned current 7 Indic languages (en, hi, bn, mr, as, ta, te) with 100% key parity (66/66 keys) as an extensible prototype designed for broader regional Indic dialect expansion.
  - **Vercel Frontend Deployment**: Configured decoupled deployment with root `vercel.json` and `frontend/vercel.json` (Vite SPA rewrites), and added `VITE_API_BASE_URL` resolution in `frontend/src/services/api.js`.
  - **Backend Hosting Architecture**: Audited FastAPI + SQLite + Pillow image processing backend; recommended host environments (Render / Railway / Fly.io / AWS EC2) for persistent SQLite writes and `/enhanced` studio asset serving.
  - **SIH Prototype Evaluation**: Formally evaluated project at **~70–75% SIH Prototype Readiness**, documenting core implemented capabilities vs. future production expansion roadmap.
- **Backend Test Suite**: **62/62 PASSED (100%)** (`python -m unittest discover -s tests -p "test_*.py" -v`).
- **Frontend Production Build**: `npm run build --prefix frontend` **PASSED** (1610 modules transformed, 0 errors).
- **Git Formatting Check**: `git diff --check` **PASSED** (0 formatting/whitespace issues).
- **Status**: **PASS — MULTILINGUAL AI & VERCEL READY**.
