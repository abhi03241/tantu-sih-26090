# TANTU System Architecture

**SIH 2026 Problem Statement 26090**: *AI-Driven Market Linkage and Smart Cataloging Mobile Application for Marginalized Artisans.*

---

## 1. Executive Summary

**TANTU** is a college-level prototype designed for Smart India Hackathon (SIH). It empowers rural and marginalized Indian artisans to digitize, market, price, and sell their traditional handicrafts using voice-driven multi-lingual AI cataloging, studio image enhancement, dynamic fair pricing, and direct B2B market linkage.

The backend is built using **Python, FastAPI, Pydantic, and SQLite** to provide high performance, zero external server dependencies, and maximum resilience during live prototype demonstrations.

---

## 2. Directory Structure

```text
tantu-sih-26090/
├── frontend/                     # Mobile & Web UI (Maintained by Team Member P)
│   └── README.md
├── backend/                      # Core FastAPI Application & APIs (Maintained by Lead A)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py               # Application entrypoint & CORS middleware
│   │   ├── config.py             # Environment settings & MOCK_AI toggle
│   │   ├── database.py           # SQLite database persistence layer
│   │   ├── models.py             # Domain models (Product, User, ArtisanProfile, Buyer, OrderRequest)
│   │   ├── schemas.py            # Pydantic validation schemas & Common Product Contract
│   │   ├── seed_data.py          # Auto-seeding mechanism for demo products
│   │   └── routers/              # API route controllers
│   │       ├── __init__.py
│   │       ├── products.py       # CRUD endpoints for products
│   │       ├── ai_endpoints.py   # Voice, Vision, Catalogue, & Pricing AI hooks
│   │       ├── artisan.py        # Artisan dashboard endpoints
│   │       ├── buyer.py          # Buyer marketplace feed endpoints
│   │       └── orders.py         # B2B order request endpoints
│   ├── tantu.db                  # Local SQLite database file
│   └── requirements.txt          # Python dependencies
├── ai/                           # AI/ML Submodules (Integrated by Members M, R, S)
│   ├── nlp/
│   │   ├── __init__.py
│   │   └── voice_and_story.py    # Voice transcript & multilingual NLP (Member M)
│   ├── vision/
│   │   ├── __init__.py
│   │   └── image_enhancer.py     # AI backdrop cleanup & studio enhancement (Member R)
│   └── pricing/
│       ├── __init__.py
│       └── smart_pricing.py      # Fair wage & market pricing engine (Member S)
├── data/
│   └── sample_products.json      # Demo seed dataset
├── docs/
│   ├── ARCHITECTURE.md           # Technical architecture blueprint
│   └── API_CONTRACTS.md          # Comprehensive REST API specifications
├── tests/
│   ├── __init__.py
│   └── test_api.py               # Unit & Integration test suite
├── README.md                     # Project overview and quickstart guide
├── .env.example                  # Environment configuration template
└── .gitignore                    # Version control ignore rules
```

---

## 3. Team Responsibilities & Integration Matrix

| Role | Team Member | Scope / Component | Backend Hook / API Endpoint |
|---|---|---|---|
| **Tech Lead / Backend** | **A** | Core Architecture, DB, APIs, Integration | FastAPI, SQLite, Pydantic schemas, Routers |
| **Frontend / Mobile UI** | **P** | Artisan App UI, Buyer Storefront | `GET /api/artisan/products`, `GET /api/buyer/products`, `POST /api/orders/request` |
| **AI / NLP / Voice** | **M** | Voice-to-Catalog, Storytelling, Hindi NLP | `ai/nlp/voice_and_story.py` -> `POST /api/products/{id}/voice`, `/generate-catalogue` |
| **AI Image Enhancement** | **R** | Studio Backdrop Cleanup, Super Resolution | `ai/vision/image_enhancer.py` -> `POST /api/products/{id}/enhance-image` |
| **Pricing & B2B Marketplace** | **S** | Fair Wage Pricing, Cost-Plus Algorithm | `ai/pricing/smart_pricing.py` -> `POST /api/products/{id}/price` |

---

## 4. Database Schema (SQLite)

### Products (`products`)
- `id` (TEXT, PK): Unique identifier e.g. `prod-bamboo-001`
- `title` (TEXT): Product headline in English/Hindi
- `description_english` (TEXT): English description
- `description_hindi` (TEXT): Hindi description
- `category` (TEXT): Craft category e.g. "Bamboo & Cane Craft"
- `material` (TEXT): Primary material used
- `dimensions` (TEXT): Size / dimensions e.g. "30cm x 30cm x 20cm"
- `production_time` (TEXT): Time to produce e.g. "3 days"
- `tags` (TEXT): JSON string array e.g. `["bamboo", "handicraft"]`
- `story` (TEXT): Regional heritage & artisan narrative
- `sentiment` (TEXT): Cultural sentiment rating
- `narrative_type` (TEXT): Archetype e.g. "Cultural Heritage"
- `image_url` (TEXT): Original artisan image URL
- `enhanced_image_url` (TEXT): AI enhanced studio backdrop URL
- `suggested_price_min` (REAL): Lower bound of fair price range
- `suggested_price_max` (REAL): Upper bound of fair price range
- `artisan_id` (TEXT): Foreign key to artisan profile
- `artisan_name` (TEXT): Artisan display name
- `location` (TEXT): Artisan village / region
- `created_at` (TEXT): ISO timestamp

### Orders (`orders`)
- `id` (TEXT, PK): Unique order request ID
- `product_id` (TEXT): Target product ID
- `product_title` (TEXT): Snapshot title
- `artisan_id` (TEXT): Target artisan ID
- `buyer_name` (TEXT): Buyer name / business entity
- `buyer_contact` (TEXT): Contact phone/email
- `quantity` (INTEGER): Units requested
- `notes` (TEXT): Custom requests / packaging notes
- `price_offered` (REAL): Proposed unit price (INR)
- `status` (TEXT): Order state (`pending`, `accepted`, `fulfilled`)
- `created_at` (TEXT): ISO timestamp

---

## 5. MOCK_AI Resilience Strategy

To guarantee **100% demo reliability** during hackathon judging, the backend supports `MOCK_AI=true` (enabled by default in `.env`):

- **When `MOCK_AI=true`**:
  - Voice audio inputs simulate instant Indic language transcription and sentiment analysis.
  - Image enhancement returns studio-grade high-resolution images.
  - Pricing calculates instant cost-plus bounds based on category and material rules.
  - **No external API key failure, timeout, or rate-limit can crash the application.**

- **When `MOCK_AI=false`**:
  - AI modules invoke real models (OpenAI/Gemini/HuggingFace) configured by members M, R, and S.

---

## 6. How to Run Backend Locally

```bash
# 1. Clone repository & switch to backend branch
git clone https://github.com/abhi03241/tantu-sih-26090.git
cd tantu-sih-26090
git checkout feature/A-backend

# 2. Install dependencies
python -m pip install -r backend/requirements.txt

# 3. Launch FastAPI server
python -m backend.app.main

# Server starts at http://localhost:8000
# Interactive Swagger Documentation: http://localhost:8000/docs
```
