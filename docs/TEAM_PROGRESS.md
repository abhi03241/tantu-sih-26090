# TANTU Team Progress & Shared Interface Registry

> **SIH 2026 — Problem Statement 26090**  
> *AI-Driven Market Linkage and Smart Cataloging Mobile Application for Marginalized Artisans*

---

## 👥 Module Ownership & Integration Matrix

| Role | Developer | Branch | Primary Directory | Key Shared Endpoints |
|---|---|---|---|---|
| **Tech Lead / Core Backend** | **A** | `feature/A-backend` | `backend/app/` | `POST /api/products`, `GET /api/products` |
| **Frontend / Mobile UI** | **P** | `feature/P-frontend` | `frontend/` | `GET /api/buyer/products`, `POST /api/orders/request` |
| **NLP & Voice Cataloging** | **M** | `feature/M-nlp` | `ai/nlp/` | `POST /api/products/{id}/voice`, `/generate-catalogue` |
| **AI Vision & Image Enhancement** | **R** | `feature/R-vision` | `ai/vision/` | `POST /api/products/{id}/enhance-image` |
| **Database & Testing** | **Parth** | `feature/Parth-db-tests` | `backend/app/database.py`, `tests/` | SQLite models, Test runner |
| **Dynamic Pricing & B2B Marketplace** | **S** | `feature/S-pricing-marketplace` | `ai/pricing/`, `backend/app/routers/` | `POST /api/pricing/estimate`, `PATCH /api/orders/{id}/status` |

---

## 🔄 Shared API & Interface Updates by Member S

### 1. Pricing Service Interface (`ai/pricing/`)
- Exported from `ai/pricing/__init__.py`:
  - `calculate_smart_price(...)`: Backward-compatible entrypoint used in `ai_endpoints.py`.
  - `PricingService`: Base interface.
  - `MockPricingService` & `RealPricingService`.
  - `load_demo_market_references()`: Access to curated benchmark dataset.
- Added API routes in `backend/app/routers/pricing_router.py`:
  - `POST /api/pricing/estimate`: Standalone on-the-fly pricing breakdown.
  - `GET /api/pricing/reference-data`: Curated demo reference dataset (`data/demo_market_prices.json`).

### 2. Order Request Interface (`backend/app/routers/orders.py`)
- Standardized request payload in `schemas.py`:
  ```json
  {
    "product_id": "prod-bamboo-001",
    "buyer_name": "FabIndia Sourcing Unit",
    "buyer_contact": "procurement@fabindia.com",
    "quantity": 100,
    "message": "Interested in ordering 100 pieces.",
    "price_offered": 850.0
  }
  ```
- Validation rules enforced:
  - `quantity > 0` (422 rejection if $\le 0$).
  - `buyer_name` non-empty (422 rejection if blank).
  - `product_id` must exist in database (404 rejection if missing).
- Status lifecycle:
  - Supported states: `requested`, `pending`, `accepted`, `rejected`, `completed`.
  - Endpoint: `PATCH /api/orders/{id}/status`.

### 3. B2B Marketplace Web Portal
- Available locally at `http://localhost:8000/marketplace`.
- Serves `frontend/index.html` with product browse, search, category filter, bulk inquiry, and order tracking.

### 4. Pricing Input Validation (Member S, 2026-09-06)
- `POST /api/pricing/estimate` now rejects negative raw-material cost, labor hours, labor cost, and overhead with `422 Unprocessable Entity`.
- Optional pricing fields remain optional: omitted values use explainable demo-reference fallbacks.
- Consumers should present pricing only as **AI-assisted suggested price range**, never as exact market truth.

### 5. Mobile/APK Pricing-to-Order Verification (Member S, 2026-09-10)
- Existing pricing, product detail, buyer feed, bulk-order, and status persistence tests pass **26/26** on `feature/S-pricing-marketplace`.
- The requested `bbdaea3` React/Vite/Capacitor baseline is not present in this checkout or configured remotes. This branch has a static marketplace and no `published`/`draft`/`processing` product lifecycle field or publish endpoint.
- Published-only visibility cannot be verified safely on this branch. The integrated baseline/branch is required; no schema, API, pricing, NLP, or Vision code was changed.

### 6. ShilpVani End-to-End Audit & Verification (Member S, 2026-09-11)
- Verified complete flow: `Pricing → Review → Publish → Buyer Marketplace → Product Detail → Bulk Order → Order Status`.
- AI-assisted pricing range verified with bounds calculation, labor hours handling (`labor_hours * rate`), material/cost inputs, overhead, quantity discount tiers, and regional wage adjustments.
- Validation verified: negative costs/labor/overhead reject with `422 Unprocessable Entity`; non-positive order quantities reject with `422`; non-existent products return `404`.
- Lifecycle guards verified: published products appear in buyer marketplace; draft and processing products are excluded; bulk orders on unpublished items return `409 Conflict`.
- Order lifecycle verified: bulk order creation generates pending order; status update endpoint (`PATCH /api/orders/{id}/status`) persists state transitions in SQLite database.
- TANTU -> ShilpVani Branding Audit: Identified occurrences on user-facing screens (`Header.jsx`, `LanguageSelection.jsx`, `AddProductWizard.jsx`, `BuyerProductDetail.jsx`, `languages.js`, `index.html`). No frontend branding code was changed per instructions.
- Test suites passing: **26 / 26** on `feature/S-pricing-marketplace` and **33 / 33** on the integrated `bbdaea3` baseline.
- Decision: All checks passed with zero blocking issues. Per instructions ("If everything works: MAKE NO CODE CHANGES"), no application code was modified.

### 7. Pricing, Marketplace, and Bulk-Order Finalization (Member S, 2026-09-11)
- **Publication Lifecycle & Marketplace Guards**: Product `status` (`draft`, `processing`, `ready`, `published`) added to schema, SQLite tables, and repository. `GET /api/buyer/products` strictly filters for published products, ensuring draft and processing products are excluded from buyer browse.
- **Bulk Order Integrity**: `POST /api/orders/request` guards against unpublished items (rejecting with `409 Conflict`), validates `quantity > 0` and non-empty `buyer_name` (422), persists orders as `pending`, and persists status transitions (`PATCH /api/orders/{id}/status`).
- **Product Status & Publish APIs**: Added `GET /api/products/{id}/status` and `PATCH /api/products/{id}/publish` to transition products from draft/ready to published.
- **Pricing Explanations & Disclaimers**: Pricing range bounds verified (`min < max`), negative inputs rejected (422), and outputs strictly disclaimed as **"AI-assisted suggested price range"** and **"Demo market reference"** (never described as guaranteed market truth).
- **Scope Compliance**: No payments, logistics, GeM, ONDC, NLP, vision, camera, or frontend architecture modified.

---

## 🧪 Shared Test Suite Status
- Automated tests passing: **30 / 30** (`tests/test_api.py` and `tests/test_pricing_marketplace.py`).
- Integrated baseline tests passing: **33 / 33** (`test_api.py`, `test_integration.py`, `test_pricing_marketplace.py`).
