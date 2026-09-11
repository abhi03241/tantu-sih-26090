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
