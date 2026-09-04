# TANTU Team Progress & Integration Audit Matrix

> **Smart India Hackathon (SIH 2026) — Problem Statement 26090**  
> *AI-Driven Market Linkage and Smart Cataloging Mobile Application for Marginalized Artisans*  
> **Prepared by: Parth (Database + Testing + Integration Support)**

---

## 1. 📊 Team Progress & Integration Status

| Member | Role | Assigned Subsystem | Current Status | Integration Compatibility |
|---|---|---|---|---|
| **A (Abhishek)** | Tech Lead + Backend | FastAPI, SQLite Persistence, Routers | ✅ Fully Functional & Tested | Shared Product Schema synchronized across all repositories and routes. |
| **P (Frontend)** | Frontend / Mobile UI | Mobile App, Artisan & Buyer Feeds | 🔄 Ready for Integration | API contracts updated with profiles, status patch, and publish endpoints. |
| **M (NLP)** | AI / NLP / Voice | Voice-to-Text, Bilingual Story, Sentiment | ✅ Validated with Fallback | Mock & live responses conform strictly to `ProductResponse` schema. |
| **R (Vision)** | AI Vision / Enhancer | Studio Backdrop Cleanup & 2x Upscale | ✅ Validated with Fallback | Output maps cleanly to `enhanced_image_url`. |
| **S (Pricing)** | Pricing & Marketplace | Fair Wage Pricing, B2B Order Flow | ✅ Validated with Fallback | Fair pricing bounds map to `suggested_price_min`/`max`. |
| **Parth (Self)** | DB + QA + Integration | SQLite DB, Seed Data, Test Suites | ✅ 100% Passed (21 tests + smoke) | Automated regression & integration test pipeline operational. |

---

## 2. 🔍 Integration Audit & Issues Discovered

### Issue 1: Hardcoded Artisan Profile Response
* **Problem**: `GET /api/artisan/profile/{artisan_id}` returned "Lakshmi Devi" for all artisan IDs (including Ramesh Ansari, Suresh Sharma, etc.).
* **Affected Module**: `backend/app/routers/artisan.py`
* **Owner**: Tech Lead (A) / Parth (DB Lead)
* **Expected Behavior**: Profile lookup should query `ArtisanRepository.get_by_id(artisan_id)` and return 404 if not found.
* **Resolution**: Implemented `ArtisanRepository` in `database.py` and updated `artisan.py` to perform dynamic database queries. Verified in `test_16_artisan_and_buyer_profiles`.

### Issue 2: Unvalidated Order Quantities
* **Problem**: `POST /api/orders/request` accepted `quantity: 0` or negative values.
* **Affected Module**: `backend/app/schemas.py`, `backend/app/routers/orders.py`
* **Owner**: Backend (A) / Pricing (S)
* **Expected Behavior**: Quantity must be strictly greater than 0 (`gt=0`), returning `422 Unprocessable Entity` for invalid quantities.
* **Resolution**: Added `gt=0` validation to `OrderRequestCreate.quantity`. Verified in `test_12_invalid_order_quantity`.

### Issue 3: Missing Product Lifecycle Status & Publishing Workflow
* **Problem**: Products had no status field (`draft`, `published`, `archived`), meaning unfinished artisan drafts immediately appeared in the buyer marketplace feed.
* **Affected Module**: `backend/app/schemas.py`, `backend/app/routers/products.py`, `backend/app/routers/buyer.py`
* **Owner**: Backend (A) / Frontend (P)
* **Expected Behavior**: Products start as `draft`. Only after the artisan reviews and clicks `Publish` does the product appear in `GET /api/buyer/products`.
* **Resolution**: Added `status` column with default `'draft'` and schema migration. Added `POST /api/products/{id}/publish` and `PATCH /api/products/{id}/status`. Buyer feed defaults to `status="published"`. Verified in `test_17_product_publish_and_status_transitions` and `test_18_buyer_marketplace_published_filtering`.

### Issue 4: Narrow Search Query Scope
* **Problem**: `ProductRepository.get_all(query=q)` only searched `title`, `description_english`, and `material`, ignoring Hindi translations and tags.
* **Affected Module**: `backend/app/database.py`
* **Owner**: Backend (A)
* **Expected Behavior**: Search should search across `title`, `description_english`, `description_hindi`, `material`, and `tags`.
* **Resolution**: Broadened SQL query to search across all five fields.

### Issue 5: Missing Order Status Lifecycle Endpoints
* **Problem**: Once an order was submitted, neither the artisan nor the buyer could retrieve the order by ID or update its status.
* **Affected Module**: `backend/app/routers/orders.py`
* **Owner**: Backend (A) / Pricing (S)
* **Expected Behavior**: Provide `GET /api/orders/{id}` and `PATCH /api/orders/{id}/status` for status lifecycle transitions (`pending` -> `accepted` -> `in_production` -> `fulfilled`).
* **Resolution**: Added endpoints and repository methods. Verified in `test_14_order_status_update`.

---

## 3. 🤝 Recommendations for Next Steps

1. **For Tech Lead (A)**:
   * Review and merge `feature/Parth-db-testing` into `feature/A-backend`.
   * Add GitHub collaborator write permissions for user `Parth10850` to enable direct branch pushing.
2. **For Frontend Lead (P)**:
   * Wire the `Publish` button on the Artisan mobile app to `POST /api/products/{id}/publish`.
   * Wire the Order Management tab on the Artisan dashboard to `PATCH /api/orders/{id}/status`.
   * Fetch registered artisan credentials from `GET /api/artisan/profiles`.
3. **For AI Submodule Leads (M, R, S)**:
   * Keep `MOCK_AI=true` as the safe default for offline SIH judging demos.
   * When connecting live models, ensure outputs adhere strictly to the JSON contracts defined in `docs/API_CONTRACTS.md`.
