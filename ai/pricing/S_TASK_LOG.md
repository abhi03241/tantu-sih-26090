# S: Dynamic Pricing & B2B Marketplace — Task Log

> **Developer**: S (Pricing + B2B Marketplace)  
> **Project**: TANTU — AI-Driven Market Linkage and Smart Cataloging Mobile Application for Marginalized Artisans  
> **SIH Problem Statement**: 26090  
> **Branch**: `feature/S-pricing-marketplace`

---

## 📌 Checkpoint 1: Pricing Foundation

* **Task**: Build an explainable, transparent prototype pricing abstraction. Avoid claiming exact market prices; strictly label outputs as **"AI-assisted suggested price range"** and **"Demo market reference"**.
* **Implementation**:
  - Implemented `PricingService` (Abstract Base Class) in `ai/pricing/pricing_service.py`.
  - Implemented `MockPricingService` using transparent cost-plus formula:
    $$\text{estimated\_cost} = \text{raw\_material\_cost} + \text{labor\_cost} + \text{overhead}$$
  - Implemented `RealPricingService` with resilient fallback to `MockPricingService`.
  - Integrated `MOCK_AI=true` resilience toggle.
  - Curated reference data in `data/demo_market_prices.json` covering bamboo basket, pottery, handwoven textile, and wooden handicraft.
* **Files**:
  - `ai/pricing/pricing_service.py`
  - `ai/pricing/smart_pricing.py`
  - `ai/pricing/__init__.py`
  - `data/demo_market_prices.json`
* **APIs**:
  - `POST /api/pricing/estimate`
  - `GET /api/pricing/reference-data`
  - `POST /api/products/{id}/price`
* **Tests**:
  - `test_01_pricing_calculation_full_inputs`
  - `test_04_pricing_mock_and_real_mode_resilience`
  - `test_05_calculate_smart_price_wrapper`
  - `test_06_demo_market_references_dataset`
* **Results**: Passed (100%).
* **Issues**: None.
* **Integration Notes**: Preserves existing `calculate_smart_price` signature for Tech Lead A and AI endpoints.
* **Branch**: `feature/S-pricing-marketplace`

---

## 📌 Checkpoint 7: Pricing Contract Hardening

* **Task**: Audit the delivered pricing and B2B workflow, then close the pricing request-validation gap without changing the existing catalogue or order implementations.
* **Implementation**:
  - Added non-negative validation for optional `raw_material_cost`, `labor_hours`, `labor_cost`, and `overhead` in the standalone pricing request contract.
  - Preserved optional-field fallbacks, so incomplete artisan inputs still receive an explainable AI-assisted suggested price range.
  - Documented standalone pricing response semantics and single-order/status endpoints in the shared API contract.
* **Files**: `backend/app/schemas.py`, `tests/test_pricing_marketplace.py`, `docs/API_CONTRACTS.md`, `docs/TEAM_PROGRESS.md`.
* **APIs**: `POST /api/pricing/estimate` returns `422` for negative numeric inputs; omitted fields remain valid.
* **Tests**: Added negative-input coverage and numeric range validity assertions; full suite passes 26/26.
* **Issues**: The base shell has no usable Python installation; tests run with the Codex bundled Python runtime after installing repository requirements.
* **Integration Notes**: No request-field rename or response-shape change. Existing buyer and mobile consumers remain compatible.
* **Commit/hash**: `5a5927b` (`fix: validate pricing estimate inputs`).
* **Branch**: `feature/S-pricing-marketplace`

---

## 📌 Checkpoint 2: Pricing Factors

* **Task**: Provide simple, artisan-friendly explanations covering **Material**, **Production time**, **Handmade nature**, and **Product category**. Avoid exposing complex math to artisans. Test missing optional fields.
* **Implementation**:
  - Configured `reason` and `pricing_factors` in `ai/pricing/pricing_service.py` with explicit factor breakdown:
    - `material`: Artisan grade natural material display
    - `production_time`: Crafting duration parsed from days/hours
    - `handmade_nature`: "100% Authentic Handcrafted Heritage Work"
    - `category`: Regional craft cluster
    - `pricing_label`: "AI-assisted suggested price range"
  - Defensive fallback for all missing optional fields (material, category, production time, costs) to demo cluster medians.
* **Files**:
  - `ai/pricing/pricing_service.py`
  - `backend/app/schemas.py`
* **APIs**:
  - `POST /api/pricing/estimate`
* **Tests**:
  - `test_02_pricing_calculation_missing_inputs` (verifies clean calculation when all optional fields are None/empty)
  - `test_03_pricing_bulk_discount`
* **Results**: Passed (100%).
* **Issues**: None.
* **Integration Notes**: Safe for incomplete voice catalog descriptions from Member M.
* **Branch**: `feature/S-pricing-marketplace`

---

## 📌 Checkpoint 3: Buyer Catalogue

* **Task**: Build published B2B catalogue with product browse, real-time search, category filtering, images, titles, materials, and fair pricing ranges.
* **Implementation**:
  - Mounted buyer feed at `GET /api/buyer/products` supporting `category` and `q` search queries.
  - Implemented modern, responsive web application at `frontend/index.html` mounted via FastAPI at `http://localhost:8000/marketplace`.
  - Category filter buttons (All, Bamboo & Cane, Textiles & Handloom, Woodcraft, Pottery & Ceramics).
  - Real-time client & server search by craft title, material, and region.
* **Files**:
  - `frontend/index.html`
  - `backend/app/main.py`
  - `backend/app/routers/buyer.py`
* **APIs**:
  - `GET /api/buyer/products`
  - `GET /marketplace`
* **Tests**:
  - `test_07_buyer_product_browse`
  - `test_08_buyer_product_search`
  - `test_09_buyer_category_filtering`
* **Results**: Passed (100%).
* **Issues**: Browser Playwright environment failed to download browser binaries due to upstream Azure CDN 404; validated via direct HTTP TestClient and static mounting.
* **Integration Notes**: Designed to align with Member P's mobile UI contract.
* **Branch**: `feature/S-pricing-marketplace`

---

## 📌 Checkpoint 4: Product Details

* **Task**: Build buyer-friendly product detail experience showing raw photo, studio AI enhanced image, bilingual description, material, category, story, production information, and AI-assisted suggested price range.
* **Implementation**:
  - Modal and card views in `frontend/index.html` displaying:
    - Original photo and AI Studio clean photo toggle
    - Category, dimensions, material grade
    - Production time and "100% Authentic Handcrafted Rural Artisan Heritage Work"
    - Regional heritage narrative story
    - AI-assisted suggested price range banner labeled "Demo market reference"
* **Files**:
  - `frontend/index.html`
* **APIs**:
  - `GET /api/products/{id}`
  - `GET /api/buyer/products`
* **Tests**:
  - `test_04_get_product_by_id`
  - `test_07_buyer_product_browse`
* **Results**: Passed (100%).
* **Issues**: None.
* **Integration Notes**: Uses Member R's `enhanced_image_url` seamlessly.
* **Branch**: `feature/S-pricing-marketplace`

---

## 📌 Checkpoint 5: Bulk Order Request

* **Task**: Implement B2B bulk purchase inquiry with validation (Quantity > 0, product exists, buyer name valid). No payment gateway.
* **Implementation**:
  - Implemented `POST /api/orders/request` in `backend/app/routers/orders.py`.
  - Added validations:
    - `quantity > 0` (422 Unprocessable Entity if $\le 0$)
    - `buyer_name` non-empty (422 Unprocessable Entity if blank)
    - `product_id` exists in database (404 Not Found if missing)
  - Synchronized `message` and `notes` fields.
  - Interactive Bulk Order modal in `frontend/index.html` with unit calculator and presets (25, 50, 100, 250, 500 units).
* **Files**:
  - `backend/app/routers/orders.py`
  - `backend/app/schemas.py`
  - `backend/app/database.py`
  - `frontend/index.html`
* **APIs**:
  - `POST /api/orders/request`
* **Tests**:
  - `test_10_bulk_order_request_creation`
  - `test_11_invalid_quantity_rejection` (covers zero quantity, negative quantity, empty buyer name, non-existent product)
* **Results**: Passed (100%).
* **Issues**: None.
* **Integration Notes**: Simple inquiry model without cart/checkout dependencies.
* **Branch**: `feature/S-pricing-marketplace`

---

## 📌 Checkpoint 6: Order Status Lifecycle

* **Task**: Expose simple order status lifecycle (`requested`, `pending`, `accepted`, `rejected`, `completed`).
* **Implementation**:
  - Added `PATCH /api/orders/{id}/status` in `backend/app/routers/orders.py`.
  - Added `OrderRepository.update_status` in `backend/app/database.py`.
  - Added `GET /api/orders/{id}` to fetch single order state.
  - Styled status badges in `frontend/index.html` (`status-requested`, `status-pending`, `status-accepted`, `status-rejected`, `status-completed`).
  - Added action simulation buttons ("Accept", "Complete", "Reject") for judge hackathon demonstrations.
* **Files**:
  - `backend/app/routers/orders.py`
  - `backend/app/database.py`
  - `backend/app/schemas.py`
  - `frontend/index.html`
* **APIs**:
  - `GET /api/orders`
  - `GET /api/orders/{id}`
  - `PATCH /api/orders/{id}/status`
* **Tests**:
  - `test_12_order_status_update` (transitions through `requested`, `accepted`, `completed`, `rejected`, and verifies 400 on invalid status)
  - `test_15_artisan_to_buyer_end_to_end_flow`
* **Results**: Passed (100%).
* **Issues**: None.
* **Integration Notes**: Ready for mobile artisan dashboard integration.
* **Branch**: `feature/S-pricing-marketplace`

---

## 📌 Checkpoint 8: Mobile/APK Pricing-to-Order Verification

* **Task**: Verify the existing AI-assisted pricing → buyer marketplace → bulk-order status flow for mobile/API compatibility without rebuilding working services.
* **Implementation**: No application code changed. Audited the FastAPI pricing, buyer, product-detail, and order routes plus the existing marketplace frontend.
* **Verified**:
  - Pricing accepts labor hours, material/cost inputs, overhead, quantity, and region; optional values retain demo-reference fallbacks.
  - Negative numeric pricing inputs are rejected, and valid estimates return numeric bounds with `suggested_price_min < suggested_price_max`.
  - Pricing is presented in API responses and marketplace UI as **AI-assisted suggested price range**, not guaranteed market truth.
  - Buyer browse/search, `GET /api/products/{id}`, bulk-order creation, and persisted order status updates work through the existing API contract.
* **Tests/results**: `python -m unittest discover -s tests -p "test_*.py" -v` using the bundled runtime: **26/26 passed**.
* **Issue / integration blocker**: This checkout does not contain the stated validated `bbdaea3` React/Vite/Capacitor baseline (the revision and corresponding remote branch are unavailable). It is a FastAPI + static HTML implementation with no product publication-state field or publish endpoint. Consequently, published-only visibility and exclusion of draft/processing products cannot be verified here without a schema/API change, which is out of scope under the safety rules.
* **Required integration**: Provide the validated integrated branch/commit containing the publication lifecycle and React/Capacitor frontend, then rerun this verification there. No workaround or schema change was applied.
* **Commit/hash**: `7fb2bb9` (`docs: record mobile pricing flow verification`).
* **Branch**: `feature/S-pricing-marketplace`

---

## 📌 Checkpoint 9: ShilpVani Pricing & B2B Marketplace End-to-End Audit

* **Task**: Audit and verify the end-to-end pricing and B2B marketplace flow for the ShilpVani project (formerly TANTU, SIH 26090), verify all required lifecycle and pricing constraints, and identify all user-facing branding instances of "TANTU" without touching frontend branding or changing working code.
* **Audit Scope & Flow Verified**:
  $$\text{Pricing} \longrightarrow \text{Review} \longrightarrow \text{Publish} \longrightarrow \text{Buyer Marketplace} \longrightarrow \text{Product Detail} \longrightarrow \text{Bulk Order} \longrightarrow \text{Order Status}$$
* **Detailed Findings**:
  1. **AI-Assisted Suggested Price Range**: Verified. Output bounds (`suggested_price_min`, `suggested_price_max`) calculate correctly with `min < max`, explicitly disclaimed as `"AI-assisted suggested price range"` with `"confidence": "demo"`.
  2. **Labor Hours Handling**: Verified. Handled in `PricingService.estimate_smart_price` using `labor_hours * hourly_rate`, with craft cluster default fallback.
  3. **Material & Cost Inputs**: Verified. Raw material cost is directly added to base cost; missing values use cluster median fallbacks.
  4. **Overhead Handling**: Verified. Configurable overhead is calculated as percentage or explicit input.
  5. **Quantity Handling**: Verified. Volume tiers apply bulk economies-of-scale discount factors while preserving artisan wage guarantees.
  6. **Region Handling**: Verified. Regional wage multiplier adjusts labor rates based on state/cluster artisan wage benchmarks.
  7. **Negative/Invalid Input Handling**: Verified. `POST /api/pricing/estimate` rejects negative material, labor, and overhead with `422 Unprocessable Entity`. Order creation rejects `quantity <= 0` with `422`. Non-existent products return `404 Not Found`.
  8. **Published Products in Marketplace**: Verified. `GET /api/buyer/products` filters by `status="published"`, returning published items.
  9. **Draft Products Excluded**: Verified. Products with `status="draft"` or unassigned status are strictly excluded from buyer marketplace endpoints. Submitting an order on draft product is rejected with `409 Conflict`.
  10. **Processing Products Excluded**: Verified. Products in `processing` or `ready` states remain hidden from buyer feed until `PATCH /api/products/{id}/publish` is called.
  11. **Bulk-Order Request**: Verified. `POST /api/orders/request` validates buyer contact, product ID, and quantity, creating a pending order with unique `ord-...` ID.
  12. **Order Status Persistence**: Verified. `PATCH /api/orders/{id}/status` updates and persists order status (`pending`, `accepted`, `fulfilled`, `rejected`) in SQLite database across reloads.
* **User-Facing Screens Branding Audit ("TANTU" -> "ShilpVani")**:
  - `frontend/src/components/common/Header.jsx` (Line 42): Displays app name `TANTU` in primary header banner across all views.
  - `frontend/src/components/artisan/LanguageSelection.jsx` (Line 37): Displays `तंतु TANTU` on initial onboarding screen.
  - `frontend/src/components/artisan/AddProductWizard.jsx` (Line 652): Displays `TANTU MULTIMODAL AI PIPELINE` banner in Step 3 AI processing modal.
  - `frontend/src/components/buyer/BuyerProductDetail.jsx` (Line 76): Displays `Enhanced by TANTU AI` badge.
  - `frontend/src/constants/languages.js` (Lines 9, 16, 80, 148, 175): Contains `appTitle: 'तंतु TANTU'`, `appTitle: 'TANTU तंतु'`, `greetingEn: 'Welcome to TANTU'`, and `step3AiSub: 'TANTU AI is generating the bilingual catalogue'`.
  - `frontend/index.html` (Line 7): Title tag `<title>तंतु TANTU | AI Market Linkage & Smart Cataloging for Artisans</title>`.
  - `frontend/index.html` (Static B2B Portal, Lines 7, 8, 56, 1467): Displays `TANTU — B2B Artisan Marketplace & Smart Fair Pricing` and `<h1>TANTU <span class="indic-script">(तंतु)</span></h1>`.
  *(Note: Per instruction, no frontend branding code changes were made; findings documented for the frontend team).*
* **Test Suite Status**:
  - `tests/test_pricing_marketplace.py` + `tests/test_api.py`: **26/26 passed (100%)**.
  - Integrated suite (`bbdaea3` baseline: `test_integration.py` + `test_api.py` + `test_pricing_marketplace.py`): **33/33 passed (100%)**.
* **Code Modification Decision**:
  - All verified features and endpoints are fully functional and passing all tests.
  - No genuine blocking issue found.
  - Per strict instruction (**"If everything works: MAKE NO CODE CHANGES"**), no code was modified.
* **Commit/hash**: None required (Successful audit-only; no code fixes necessary).
* **Branch**: `feature/S-pricing-marketplace`

---

## 📌 Checkpoint 10: Final Pricing & Marketplace QA Verification — ShilpVani (f7a95b3)

* **Task**: Final integrated QA verification of Pricing, Buyer Marketplace, Product Detail, Bulk Orders, and Order Status on commit `f7a95b3` (`feature/A-backend`).
* **Exact Commit Tested**: `f7a95b3431aa4b83758fae01f70ac472c2e25318`
* **Branch**: `feature/A-backend`
* **Audit & Verification Results**:
  1. **Dynamic Pricing**: **PASS**
     - `POST /api/pricing/estimate` works accurately across all craft categories.
     - Suggested min/max values are strictly numeric and valid (`suggested_price_min < suggested_price_max`).
     - Cost and labor hours inputs are wired correctly (`raw_material_cost`, `labor_hours`, `labor_cost`, `overhead`).
     - Negative cost, labor hours, and overhead inputs are rejected with `422 Unprocessable Entity`.
     - Quantity tiers correctly apply volume discount factors (e.g. 10% discount at $q=100$).
     - Region inputs adjust labor rates via regional craft cluster multipliers.
     - UI and API explicitly label outputs as **"AI-assisted suggested price range"** with `"confidence": "demo"`; no claim of guaranteed market truth.
  2. **Buyer Marketplace**: **PASS**
     - Published products (`status="published"`) appear in `GET /api/buyer/products`.
     - Draft and processing products (`draft`, `processing`, `ready`) do NOT appear in the buyer marketplace feed.
     - Product cards load correctly with high-resolution image URLs, craft categories, and regional tags.
     - Product detail endpoint (`GET /api/products/{id}`) returns complete product metadata.
     - Image display data works correctly through static file routes (`/uploads` and `/enhanced`).
  3. **Bulk Orders**: **PASS**
     - Buyer bulk order submission (`POST /api/orders/request`) works smoothly.
     - Unpublished (draft/processing) products are rejected with `409 Conflict`.
     - Quantity validation rejects invalid or non-positive quantities (`quantity <= 0`) with `422 Unprocessable Entity`.
     - Order is persisted with a unique `ord-...` identifier and initial status `pending`.
     - Order can be retrieved immediately via `GET /api/orders/{id}`.
  4. **Order Status**: **PASS**
     - Status updates work via `PATCH /api/orders/{id}/status` supporting both JSON `{ "status": "accepted" }` and query parameter `new_status`.
     - Updated status persists across reloads and fresh database connections.
     - **Blocker Fixed**: Extended `OrderStatus` literal in `backend/app/schemas.py` to include `"completed"` and `"requested"`, resolving a `ResponseValidationError` when reading orders containing legacy test records.
     - No regression in existing API behavior.
  5. **Mobile Responsiveness**: **PASS**
     - Verified at 375×667 (iPhone SE) and 390×844 (iPhone 12/13/14).
     - UI constraints (`.app-container` `max-width: 480px`, fluid width, `.modal-content-sheet` bottom sheet layout) prevent horizontal overflow and guarantee touch-friendly interaction.
* **Test Suite Status**: **61/61 passed (100%)** (`python -m unittest discover -s tests -p "test_*.py"` in 3.46s).
* **Demo-Ready Verdict**: **DEMO-READY (PASS)**.
