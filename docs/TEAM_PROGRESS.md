# TANTU — Team Progress & Integration Matrix

**SIH Problem Statement 26090**: *AI-Driven Market Linkage and Smart Cataloging Mobile Application for Marginalized Artisans*

---

## 1. Overall Team Status Overview

| Team Member | Domain | Branch | Status | Key Deliverables / Shared Contracts |
|---|---|---|---|---|
| **A (Tech Lead & Backend)** | Core Architecture, SQLite DB, REST APIs | `feature/A-backend` | **Completed** | FastAPI server at port 8000, SQLite tables (`products`, `orders`), CORS enabled, Swagger `/docs`, Common Product Contract. |
| **P (Frontend / Mobile UI)** | Artisan & Buyer Experience | `feature/P-frontend` | **Completed** | Mobile-first React 18 + Vite 6 app, Add Product Wizard (Photo, Voice, AI Processing, Smart Catalogue, Save Draft/Publish), Artisan Dashboard, My Products with status filters, and Buyer Marketplace. |
| **M (AI / NLP & Voice)** | Multilingual Voice-to-Text, 7-Language NLP & UI Translation | `feature/M-ai-nlp` | **Completed** | 7-Language NLP (`en`, `hi`, `bn`, `mr`, `as`, `ta`, `te`), `POST /api/products/{id}/voice`, `POST /api/products/{id}/generate-catalogue` |
| **R (Computer Vision)** | Studio Lighting & Background Cleanup | `feature/R-vision` | Backend Hooks Ready | `POST /api/products/{id}/enhance-image` |
| **S (Pricing & B2B)** | Cost-Plus Fair Pricing & Wholesale Marketplace | `feature/S-pricing` | Backend Hooks Ready | `POST /api/products/{id}/price`, `POST /api/orders/request`, `GET /api/orders` |
| **Parth (DB & QA)** | Database Testing & Contract Validation | `feature/testing` | Ready | SQLite persistence & integration tests |

---

## 2. Frontend (P) Integration Details

- **Frontend Port**: `http://localhost:5173/`
- **Backend API URL**: `http://localhost:8000/` (proxied via `/api` in Vite)
- **Shared Product Schema Compatibility**:
  - `id`: Unique string ID
  - `title`: English/Hindi craft title
  - `description_english`: Marketing copy
  - `description_hindi`: Regional vernacular description
  - `category`: Craft category
  - `material`: Primary raw material
  - `dimensions`: Measurements
  - `production_time`: Crafting duration
  - `tags`: Array of keywords
  - `story`: Artisan generational lineage narrative
  - `sentiment`: Tone and emotional archetype
  - `narrative_type`: E.g. "Cultural Heritage", "Artisanal Mastery"
  - `image_url`: Raw craft photograph
  - `enhanced_image_url`: Studio-enhanced photo
  - `suggested_price_min`: Fair trade lower price bound
  - `suggested_price_max`: Fair trade upper price bound
  - `status`: Lifecycle state (`draft`, `processing`, `ready`, `published`, `failed`)
  - `artisan_id`: Foreign key to artisan profile
  - `artisan_name`: Display name
  - `location`: Artisan village and state

- **Resilience Guarantee**:
  - The frontend dynamically pings `/api/health`.
  - When backend is active, live API endpoints are utilized.
  - When backend is inactive, a transparent `localStorage` mock database powers the complete demonstration without crashing.

---

## 3. Member M Progress & Multilingual NLP/Voice Verification

### M — NLP and Voice: Mobile/APK Verification (2026-09-10)
- Inspected the existing `Voice/Text → NLP → Catalogue Fields → Product` route.
- The mobile-compatible request remains `{ "audio_transcript": string, "language": "hi" | "en" }`; no product JSON contract change was made.
- The voice endpoint persists only explicitly extracted dimensions and production time, preventing missing voice details from overwriting known product data.
- Verified English, Hindi (including `3 दिन`), raw narrative notes, dimensions, production time, and underspecified input.
- Executed the full existing suite: **26/26 passed**.

### M — ShilpVani Multilingual NLP & Voice Flow Audit (2026-09-11)
- Audited complete `Text/Voice → NLP → Catalogue` pipeline for both English and Hindi under the ShilpVani project rebranding.
- Verified test cases:
  - Normal English product description (hand-carved teak wood elephant: title, material, time, sentiment, narrative, bilingual descriptions).
  - Normal Hindi product description (bamboo basket, Chanderi silk: material, time, sentiment, narrative, bilingual descriptions).
  - Hindi duration parsing: `3 दिन` correctly extracted as `3 days` (along with `15 din`, `4 ghante`, `2 hafte`).
  - Raw notes: accurately integrated into catalogue descriptions without inventing unstated narratives.
  - Dimensions & production time: explicit specs extracted accurately; unstated specs remain `null` to avoid hallucination.
  - Underspecified inputs: empty and generic inputs handled gracefully with `null` specs/story and `Neutral` sentiment.
- Integrity verified: zero invented facts, artisan info strictly preserved, correct catalogue schema conformity, and established sentiment/narrative cues maintained.
- Test suite executed: **26/26 unit and API integration tests passed**; dedicated 10-point audit script passed.
