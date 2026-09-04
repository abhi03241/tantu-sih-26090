# TANTU — AI-Assisted Dynamic Fair Pricing Engine & B2B Marketplace

> **Smart India Hackathon (SIH 2026) — Problem Statement 26090**  
> *AI-Driven Market Linkage and Smart Cataloging Mobile Application for Marginalized Artisans*  
> **Module Owner**: Team Member S (Pricing & B2B Marketplace)

---

## 🌟 Overview

The **TANTU Pricing & B2B Marketplace** module guarantees economic justice and market linkage for rural, marginalized Indian artisans. Traditional artisans frequently face severe exploitation by regional middlemen, receiving as little as 10%–20% of retail value due to lack of transparent market data and direct buyer access.

This module provides two foundational capabilities:
1. **AI-Assisted Dynamic Fair Wage Pricing**: A transparent, cost-plus calculation engine that guarantees an artisan fair hourly wage (benchmark ₹70–₹90/hr) plus healthy margins, benchmarked against curated craft fair data.
2. **Direct B2B Buyer Marketplace Feed & Inquiries**: A clean bulk ordering channel allowing retailers, boutique owners, and corporate procurement teams to discover verified artisan products and place bulk order requests without middleman markups.

---

## 📐 Transparent Prototype Pricing Model

### 1. Pricing Inputs
The pricing engine accepts the following artisan and product inputs:

| Input Field | Type | Description | Fallback Benchmark |
|---|---|---|---|
| `category` | `string` | Craft category (e.g., "Bamboo & Cane Craft", "Textiles & Handloom", "Woodcraft", "Pottery & Ceramics") | "General Handicraft" |
| `material` | `string` | Material used (e.g., "Natural Assam Bamboo", "Chanderi Silk") | "Artisan Grade Natural Material" |
| `production_time` | `string` | Estimated craft duration (e.g., "3 days", "16 hours") | Parsed into working hours (8 hrs/day) |
| `raw_material_cost` | `float` (INR) | Artisan-reported cost of raw materials | Curated category median from demo dataset |
| `labor_cost` | `float` (INR) | Artisan-reported labor cost | `labor_hours * fair_wage_rate_per_hour` |
| `labor_hours` | `integer` | Hours spent crafting the piece | Benchmark hours from demo reference (16–32 hrs) |
| `overhead` | `float` (INR) | Tool wear, studio space, finishing & packaging | 12%–15% of prime cost (`raw_material_cost + labor_cost`) |
| `quantity` | `integer` | Units requested for order (default: 1) | Used to apply bulk economies of scale |
| `region` | `string` | Geographical cluster (e.g., Assam, Madhya Pradesh, UP) | Regional craft benchmark |

---

### 2. Transparent Pricing Formula

For hackathon prototype transparency, we avoid black-box ML models in favor of a cost-plus formula that both artisans and buyers can understand:

```text
1. Prime Cost = raw_material_cost + labor_cost
2. Overhead Cost = overhead (or Prime Cost * overhead_rate [12% - 15%])
3. Estimated Cost = raw_material_cost + labor_cost + overhead_cost

4. Cost-Plus Bounds:
   cost_plus_min = Estimated Cost * (1.0 + margin_min)
   cost_plus_max = Estimated Cost * (1.0 + margin_max)

5. Demo Reference Blending:
   suggested_price_min = 0.80 * cost_plus_min + 0.20 * demo_reference_min
   suggested_price_max = 0.80 * cost_plus_max + 0.20 * demo_reference_max
```

#### Bulk Order Adjustment
When a B2B buyer places a bulk order (e.g., $\ge 50$ units):
- Marginal production economies reduce unit overhead.
- Margins adjust slightly (5%–10% concession) while strictly preserving the artisan's base fair wage floor.

---

### 3. Curated Demo Reference Dataset (`data/demo_market_prices.json`)

To prevent misleading claims of real-time market scrapers, reference benchmarks are curated from public cottage industry standards (NEHHDC, KVIC, WSC, Export Promotion Council for Handicrafts) and strictly labeled as **"Demo market reference"**:

* **Bamboo Basket** (`Bamboo & Cane Craft`):
  * Materials: Natural Assam Bamboo, Cane strips
  * Raw Material Benchmark: ₹200 – ₹350
  * Labor Benchmark: 16 hrs @ ₹70/hr fair wage
  * Demo Reference Bounds: ₹650 – ₹950
* **Pottery & Ceramics** (`Pottery & Ceramics`):
  * Materials: Terracotta Clay, Jaipur Quartz Powder
  * Raw Material Benchmark: ₹250 – ₹450
  * Labor Benchmark: 20 hrs @ ₹75/hr fair wage
  * Demo Reference Bounds: ₹750 – ₹1400
* **Handwoven Textile** (`Textiles & Handloom`):
  * Materials: Chanderi Silk Cotton, Pure Zari
  * Raw Material Benchmark: ₹600 – ₹1100
  * Labor Benchmark: 32 hrs @ ₹90/hr fair wage
  * Demo Reference Bounds: ₹1800 – ₹2500
* **Wooden Handicraft** (`Woodcraft`):
  * Materials: Sheesham Wood, Brass Inlay
  * Raw Material Benchmark: ₹350 – ₹650
  * Labor Benchmark: 24 hrs @ ₹85/hr fair wage
  * Demo Reference Bounds: ₹1100 – ₹1700

---

### 4. Output Format

All pricing requests yield the following schema:

```json
{
  "suggested_price_min": 850.0,
  "suggested_price_max": 1050.0,
  "currency": "INR",
  "confidence": "demo",
  "reason": "Based on material (Natural Assam Bamboo), estimated production effort (16 hrs @ ₹70/hr), and demo market reference data for Bamboo & Cane Craft.",
  "pricing_factors": {
    "category": "Bamboo & Cane Craft",
    "material_grade": "Natural Assam Bamboo",
    "estimated_labor_hours": "16 hrs",
    "fair_wage_rate": "₹70.0/hr",
    "fair_trade_margin": "20% - 45%",
    "bulk_quantity": 100,
    "bulk_discount_applied": true,
    "market_reference": "Demo market reference"
  },
  "breakdown": {
    "raw_material_cost": 250.0,
    "raw_material_cost_source": "artisan_input",
    "labor_cost": 1120.0,
    "labor_cost_source": "fair_wage_hourly_calculation",
    "overhead": 164.4,
    "overhead_source": "12%_of_prime_cost",
    "estimated_cost": 1534.4,
    "margin_min_pct": 15,
    "margin_max_pct": 35,
    "demo_market_reference": "Demo market reference",
    "demo_reference_bounds": [650.0, 950.0]
  },
  "recommendation": "Recommended listing price is ₹850 - ₹1050 to guarantee fair wage (₹70.0/hr) while maintaining retail competitiveness under Demo market reference guidelines."
}
```

---

### 5. Mock Mode & Resilience Architecture (`MOCK_AI=true`)

In high-stakes hackathon demos, network flakiness, rate limits, or expired third-party API keys can crash an application. The pricing engine utilizes a clean Object-Oriented Service Interface:

```text
            +---------------------+
            |   PricingService    |  (Abstract Base Class)
            +---------------------+
                       ▲
          +------------+------------+
          |                         |
+---------------------+   +---------------------+
| MockPricingService  |   | RealPricingService  |
+---------------------+   +---------------------+
(Instant deterministic    (Calls live ML/LLM API
 cost-plus calculations    with automatic fallback
 & demo benchmarks)        to MockPricingService)
```

- **`MOCK_AI=true`** (default): Instantly calculates transparent pricing bounds without external calls.
- **`MOCK_AI=false`**: Attempts real ML/LLM endpoint; if the external API fails, it catches the exception and falls back to `MockPricingService` gracefully. **Zero demo downtime.**

---

## 🛍️ B2B Marketplace & Order Linkage APIs

### 1. Buyer Feed
* **`GET /api/buyer/products`**
  * Query parameters:
    * `category` (optional): e.g. `Textiles & Handloom`
    * `q` (optional): search query across title, story, and materials
  * Returns: Array of common `ProductResponse` objects with `suggested_price_min`, `suggested_price_max`, `enhanced_image_url`, and artisan details.

### 2. Standalone Pricing Estimator
* **`POST /api/pricing/estimate`**
  * Request Body: `PricingRequest` (contains category, material, raw_material_cost, labor_hours, overhead, quantity).
  * Returns: `PricingCalculationResponse` with full cost-plus breakdown.

* **`GET /api/pricing/reference-data`**
  * Returns the full curated `demo_market_prices.json` reference dataset.

### 3. Product Price Recalculation Hook
* **`POST /api/products/{id}/price`**
  * Updates `suggested_price_min` and `suggested_price_max` directly on the database product record.

### 4. B2B Order Requests
* **`POST /api/orders/request`**
  * Submits a bulk inquiry.
  * Request Body:
    ```json
    {
      "product_id": "prod-bamboo-001",
      "buyer_name": "FabIndia Sourcing Unit",
      "buyer_contact": "procurement@fabindia.com",
      "quantity": 100,
      "message": "Interested in ordering 100 pieces for our retail stores.",
      "price_offered": 850.0
    }
    ```
  * Response: Created order with `id` (`ord-xxxx`), `status: "pending"`, and timestamp.
  * Validation: Rejects `quantity <= 0` with `422 Unprocessable Entity`.

* **`GET /api/orders`**
  * Filter by `product_id` or `artisan_id`.

* **`GET /api/orders/{id}`**
  * Retrieve single order details.

* **`PATCH /api/orders/{id}/status`**
  * Request: `{"status": "accepted"}` or `{"status": "rejected"}`.
  * Allows artisans to accept or decline bulk purchase requests.

---

## 🌐 Web Application (Buyer Experience)

The B2B Marketplace UI is located at `frontend/index.html` and served directly by FastAPI at:
`http://localhost:8000/marketplace`

Key Features:
- **Interactive Catalogue**: Filter by craft category, search titles & materials.
- **Studio Enhancer Toggle**: Switch between raw artisan phone photos and AI studio-enhanced catalog images.
- **Fair Wage Badge**: Displays transparent price range labeled `"Demo market reference"`.
- **Bulk Inquiry Dialog**:
  - Real-time order value range calculator (e.g. 100 units $\times$ unit price).
  - Quick quantity chips (25, 50, 100, 250, 500 units).
  - One-click order inquiry submission.
- **Track Inquiries Drawer**: View submitted orders with real-time status badges (`pending`, `accepted`, `rejected`) and simulation controls for judge demos.
- **Pricing Assistant**: On-the-fly simulator to test custom pricing inputs.

---

## 🧪 Testing

Run all unit & integration tests:
```bash
# Run pricing & marketplace module tests
python -m unittest discover -s tests -p "test_pricing_marketplace.py"

# Run full project test suite
python -m unittest discover -s tests -p "test_*.py"
```

Tested scenarios:
- Complete pricing calculations with full inputs.
- Fallback to demo benchmarks on missing inputs.
- Bulk quantity economy adjustments.
- Mock mode resilience.
- Product browsing, category filtering, and keyword search.
- Bulk order creation with message and notes.
- Validation: rejection of zero or negative quantities.
- Status updates (`pending` -> `accepted` / `rejected`) and rejection of invalid statuses.
- Complete end-to-end artisan cataloging to buyer order fulfillment flow.

---

## ⚠️ Limitations & Future Scope

1. **Prototype Demo Data**: Market reference data is curated from regional handicraft cluster benchmarks; real-time GeM (Government e-Marketplace) and ONDC API connectors are designated for future milestones.
2. **Payment Processing**: Prototype focuses purely on B2B discovery and purchase intent (inquiries); escrow and payment gateways (Razorpay/Stripe) are out of prototype scope.
3. **Advanced ML Training**: Future scope includes training deep learning regression models on large-scale handicraft auction and export datasets.
