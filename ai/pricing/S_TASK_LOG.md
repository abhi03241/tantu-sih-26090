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
