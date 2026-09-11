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

### M — 7-Language Multilingual NLP, Voice & UI Support (2026-09-11)
- Implemented functional end-to-end support for **7 target languages**: English (`en`), Hindi (`hi`), Bengali (`bn`), Marathi (`mr`), Assamese (`as`), Tamil (`ta`), Telugu (`te`).
- Language selector filtered to display **ONLY** the 7 functional languages (removed Odia and Gujarati placeholders).
- Implemented authentic, complete UI translation dictionaries across all 7 languages for all 66 application strings in `frontend/src/constants/languages.js`.
- Extended NLP pipeline (`ai/nlp/demo_data.py`, `ai/nlp/service.py`) to extract material, category, production duration, craft title, sentiment, and story cues in all 7 languages into structured product JSON.
- Normalized Indic digits (Devanagari, Bengali, Tamil, Telugu) to ASCII integers via `INDIC_DIGITS_MAP` in duration extraction.
- Enhanced font fallbacks (`Noto Sans Bengali`, `Noto Sans Tamil`, `Noto Sans Telugu`, `Nirmala UI`) in `index.html` and `index.css` for clean typography across Indian scripts.
- Documented voice vs. text capabilities honestly:
  - Text & Audio Transcript NLP: 100% functional across all 7 languages.
  - Web Speech API TTS Reader: Speaks natively in `en-IN`, `hi-IN`, `bn-IN`, `mr-IN`, `ta-IN`, `te-IN`, with `as-IN` falling back to regional speech synthesis.
  - Browser STT: Automatically falls back to text input when microphone speech recognition is unavailable in client browser.
- Executed full test suite: **33/33 unit & API integration tests passed**. Verified live backend `/api/products/{id}/voice` endpoint across all 7 languages (**7/7 passed**). Verified frontend production build (**0 errors**).

### M — ShilpVani Language Selector & Grounded NLP Finalization (2026-09-11)
- Verified active presence of all 7 target languages in the language selector (`LanguageSelection.jsx` and `Header.jsx`).
- Connected native speech recognition locales (`en-IN`, `hi-IN`, `bn-IN`, `mr-IN`, `as-IN`, `ta-IN`, `te-IN`) to `AddProductWizard.jsx`.
- Added regional voice transcripts for all 4 demo sample crafts in `DEMO_SAMPLE_CRAFTS`.
- Fixed keyword boundary matching in `demo_data.py` (`_match_any_keyword`) to eliminate false-positive substring cues in Indic scripts (e.g., `মা` in `মাটির`).
- Verified ephemeral wizard drafts (`new-draft`) in `/api/products/{id}/voice` and `/api/products/{id}/generate-catalogue` for seamless offline/online frontend flow.
- Verified test suite: **37/37 tests passed** (11 backend API tests + 26 NLP pipeline tests).
- Verified production build: `npm run build` in `frontend/` succeeds with **0 errors**.
