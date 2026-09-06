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

---

## 🧪 Shared Test Suite Status
- Total automated tests passing: **26 / 26** (`tests/test_api.py` and `tests/test_pricing_marketplace.py`).
