# TANTU — Team Progress & Integration Matrix

**SIH Problem Statement 26090**: *AI-Driven Market Linkage and Smart Cataloging Mobile Application for Marginalized Artisans*

---

## 1. Overall Team Status Overview

| Team Member | Domain | Branch | Status | Key Deliverables / Shared Contracts |
|---|---|---|---|---|
| **A (Tech Lead & Backend)** | Core Architecture, SQLite DB, REST APIs | `feature/A-backend` | **Completed** | FastAPI server at port 8000, SQLite tables (`products`, `orders`), CORS enabled, Swagger `/docs`, Common Product Contract. |
| **P (Frontend / Mobile UI)** | Artisan & Buyer Experience | `feature/P-frontend` | **Completed** | Mobile-first React 18 + Vite 6 app, 9 regional languages, Add Product Wizard (Photo, Voice, AI Processing, Smart Catalogue, Save Draft/Publish), Artisan Dashboard, My Products with status filters, and Buyer Marketplace. |
| **M (AI / NLP & Voice)** | Voice-to-Text & Bilingual Storytelling | `feature/M-nlp` | Backend Hooks Ready | `POST /api/products/{id}/voice`, `POST /api/products/{id}/generate-catalogue` |
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

## 3. Integration Note — P Frontend Audit (2026-09-06)

- The frontend now creates a contract-complete processing product before calling the AI endpoints, then updates that same product for draft/publish. This matches the existing AI endpoint shape (`/api/products/{id}/...`) and prevents live-backend calls against a placeholder ID.
- **Backend contract gap:** `POST /api/orders/request` and `GET /api/orders` are available, but no endpoint exists to accept or otherwise update an order request. The artisan "Accept" control therefore only persists in offline mock mode; a backend order-status update endpoint is needed for live persistence.
- **Backend contract gap:** product lifecycle `status` is used by the frontend, but it is not present in `ProductCreate`, `ProductUpdate`, or `ProductResponse`. Live backend responses consequently cannot preserve draft/ready/published state until the backend schema and persistence layer adopt it.

## 4. Mobile / APK Readiness — P (2026-09-10)

- No Capacitor configuration, Android project, or Capacitor dependency is currently committed; no native scaffolding was added to avoid an unvalidated platform change.
- The frontend now detects a Capacitor shell and requires `VITE_BACKEND_URL` for native API access, avoiding a hardcoded device-local `localhost` target. Browser development behavior and offline mock fallback are unchanged.
- Small-screen safeguards now cover safe-area insets, dynamic viewport modal height, touch scrolling, iOS input zoom prevention, compact header actions, and stacked buyer/catalogue modal fields at narrow widths.

## 5. User-Facing Rebranding to ShilpVani (शिल्पवाणी) — P (2026-09-11)

- Rebranded all user-facing strings, headers, page titles, and assistive TTS prompts from TANTU to **ShilpVani** (Hindi: **शिल्पवाणी**).
- Added `ShilpVaniLogo.jsx` SVG component (Indian loom shuttle and voice resonance motif) to header and onboarding language selection.
- Refined language selector to strictly display the 2 fully-functional languages (Hindi & English), removing stub languages without translation dictionaries.
- Verified that Hindi text preserves all existing responsive card and header layouts without truncation or overflow.
- Preserved all backend schemas, API contracts, table identifiers, and Artisan/Buyer workflows.

## 6. Camera & Microphone Hardware Experience — P (2026-09-11)

- **Camera**:
  - Added in-app live viewfinder modal using `navigator.mediaDevices.getUserMedia` with video frame snapshot capture to canvas (`image/jpeg`).
  - Added camera flip button (front/back facing mode toggle).
  - Added graceful fallback to native device camera (`<input capture="environment">`) for mobile browsers and Android/Capacitor webviews.
  - Implemented camera permission denial states with explicit retry and gallery/file upload fallbacks.
  - Proper MediaStream track cleanup on modal close and component unmount to release camera hardware.
- **Microphone**:
  - Implemented multi-click debouncing (`isMicStarting`) to prevent race conditions during SpeechRecognition initialization.
  - Added microphone permission denial handling (`NotAllowedError` / `not-allowed`) with clear Hindi guidance.
  - Added explicit one-tap "लिखकर बताएं (Switch to Text Fallback)" and "माइक पुनः प्रयास (Retry Mic)" actions.
  - Continuous timer, active audio waveform animation, and transcript audio playback support.


