<div align="center">
  <img src="docs/assets/shilpvani_logo.jpg" alt="ShilpVani Logo" width="180" style="border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.15);" />

  # ShilpVani (शिल्पवाणी)

  **AI-Driven Market Linkage & Smart Cataloging Mobile Application for Rural Artisans**

  *Your Craft. Your Voice. Your Market.*

  [![Python Unittest](https://img.shields.io/badge/Backend%20Tests-62%2F62%20PASSED-brightgreen.svg)](file:///d:/SIH2026/tests)
  [![Frontend Build](https://img.shields.io/badge/Frontend%20Build-PASSED%20(1610%20modules)-blue.svg)](file:///d:/SIH2026/frontend)
  [![Languages Supported](https://img.shields.io/badge/Languages-7%20Indic%20Languages-orange.svg)](file:///d:/SIH2026/frontend/src/constants/languages.js)
</div>

---

## 🌟 Overview

**ShilpVani (शिल्पवाणी)** is an AI-powered market linkage and smart cataloging mobile application built for Smart India Hackathon (SIH 2026). It bridges the digital divide for rural and marginalized Indian artisans by transforming a simple phone photograph and natural voice speech into studio-grade product listings, AI-assisted suggested fair price ranges, and direct B2B buyer connections across 7 major languages.

---

## 🚨 Problem Statement

Rural and marginalized artisans across India produce exquisite handcrafted heritage items but face severe systemic barriers to online commercial marketplaces:

* **Language Barriers**: E-commerce platforms are overwhelmingly English/Hindi-centric, excluding regional dialect speakers.
* **Digital Literacy Deficit**: Form-heavy listing tools require typing, categorization codes, and complex administrative inputs.
* **Cataloguing Friction**: Writing persuasive marketing text, cultural background, dimensions, and maintenance care instructions is challenging without formal marketing training.
* **Sub-par Product Photography**: Photographs taken on basic smartphones under poor lighting fail to attract urban and international buyers.
* **Pricing Uncertainty**: Artisans often underprice their labor or lack cost-plus pricing frameworks, leading to economic exploitation.
* **Limited Access to B2B Markets**: High dependency on local middlemen, physical seasonal fairs, and regional traders limits income stability.

---

## 💡 The Solution

**Craft → Voice → AI → Catalogue → Pricing → Buyer → Bulk Order**

ShilpVani eliminates complex listing forms. An artisan simply snaps a photo of their creation and speaks naturally in their native language describing what they made. ShilpVani's AI pipeline orchestrates voice transcription, background enhancement, multilingual description generation, cost-plus fair price calculation, and direct publication to a wholesale B2B marketplace.

---

## 🔁 User Journey

```text
Artisan
   │ (Photo Capture + Native Voice Description)
   ▼
AI Pipeline Understanding
   │ (Speech Processing + Image Enhancement + Fair Cost Calculation)
   ▼
Professional Product Listing
   │ (Bilingual Story, Studio Backdrop, Suggested Price Range)
   ▼
B2B Buyer Marketplace
   │ (Direct Wholesale Inquiry & Bulk Order Negotiation)
   ▼
Bulk Order Request & Order Lifecycle Tracking
   │ (Pending → Accepted → Fulfilled)
   ▼
Empowered Artisan
```

---

## ✨ Key Features

* 📷 **AI Image Studio / Image Enhancement**: Auto-corrects mobile captures with lighting balance, edge-preserving studio background cleanup, and SHA-256 hashed asset serving.
* 🎙️ **Voice-First Product Input**: Tap-to-record voice interface supporting regional Indic speech inputs.
* 🗣️ **Multilingual Auto-Cataloguing**: Translates raw artisan voice notes into structured, professional marketing copy, heritage stories, and care guidelines.
* 🌐 **7 Supported Regional Languages**: Full UI navigation, voice recognition, and translation parity across English, Hindi, Bengali, Marathi, Assamese, Tamil, and Telugu.
* 💰 **AI-Assisted Suggested Pricing**: Material cost-plus algorithm, labor hour breakdown, and regional multipliers providing an *AI-assisted suggested price range*.
* 🏢 **B2B Wholesale Marketplace**: Dedicated buyer feed for discovering published artisan products, submitting bulk order requests, and negotiating custom unit prices.
* 📦 **Order Status Tracking**: Persisted order lifecycle state management (`pending` → `accepted` → `fulfilled`).
* 📜 **Cultural Narrative Preservation**: Highlights traditional craft techniques, heritage stories, and human artisan identity.

---

## 🌐 Supported Languages

ShilpVani natively supports **7 fully verified languages**:

1. **English** (`en`) — English
2. **Hindi** (`hi`) — हिन्दी
3. **Bengali** (`bn`) — বাংলা
4. **Marathi** (`mr`) — मराठी
5. **Assamese** (`as`) — অসমীয়া
6. **Tamil** (`ta`) — தமிழ்
7. **Telugu** (`te`) — తెలుగు

---

## 🧠 AI Pipeline Architecture

The ShilpVani AI pipeline consists of specialized submodules orchestrated by a central service coordinator:

1. **Voice Processing & NLP (`ai/nlp/voice_and_story.py`)**:
   * Speech-to-text transcription parsing native dialect speech.
   * Keyword & entity extraction for dimensions, production duration, material type, and craft category.
   * Grounded narrative generation without hallucinating unstated artisan facts.
2. **Vision & Image Enhancement (`ai/vision/image_enhancer.py`)**:
   * EXIF orientation auto-normalization for smartphone photos.
   * Non-destructive studio backdrop enhancement & lighting balance.
   * Content-hash collision protection with static asset serving under `/enhanced`.
3. **AI-Assisted Dynamic Pricing (`ai/pricing/smart_pricing.py`)**:
   * Cost-plus pricing algorithm consuming raw material cost, labor hours, production duration, and regional multipliers.
   * Outputs an **AI-assisted suggested price range** (labeled clearly with a disclaimer; does not guarantee absolute market value).
4. **Product Pipeline Orchestration (`backend/app/services/orchestrator.py`)**:
   * Chains NLP, Vision, and Pricing submodules with step-level fallback isolation, ensuring system resilience even if individual AI steps encounter partial data.

---

## 🛒 B2B Marketplace & Bulk Order Workflow

ShilpVani connects rural artisans directly with verified wholesale buyers, institutions, and retailers:

* **Buyer Feed (`GET /api/buyer/products`)**: Displays strictly published artisan crafts with filtered tags, categories, and region markers.
* **Bulk Order Request (`POST /api/orders/request`)**: Buyers submit wholesale inquiries with custom quantity (units) and proposed unit pricing.
* **Order Status Management (`PATCH /api/orders/{id}/status`)**: Real-time status transitions (`pending` → `accepted` → `fulfilled`) persisted across SQLite backend and local state.

> *Note on Scope*: The current prototype demonstrates wholesale discovery, inquiry submission, and status tracking. External payment gateway integration, escrow holds, ONDC network connection, and logistics fulfillment are designed as future production extensions.

---

## 🛠️ Technology Stack

| Layer | Technology | Details |
|---|---|---|
| **Backend Framework** | Python 3.12 / FastAPI | Asynchronous REST API server with Pydantic v2 schemas |
| **Database & Storage** | SQLite 3 (`tantu.db`) | Relational persistence with raw parameterization & auto-seeding |
| **Frontend UI** | React 18 + Vite 6 | Responsive mobile-first SPA with CSS variables & glassmorphism |
| **Icons & Design** | Lucide React / Google Fonts | Outfit, Noto Sans Devanagari, Rozha One typography |
| **Image Processing** | Pillow (PIL) | Non-destructive EXIF auto-transpose, studio lighting, RGB conversion |
| **Testing Suite** | Python `unittest` | Automated backend, NLP, vision, pricing & contract regression tests |

---

## 📁 Repository Structure

```text
tantu-sih-26090/
├── ai/                              # AI Submodules (Members M, R, S)
│   ├── nlp/                         # Multilingual NLP, Voice & Storytelling (Manyata)
│   ├── vision/                      # Computer Vision & Image Enhancement (Raj)
│   └── pricing/                     # Dynamic Pricing & Fair Wage Engine (Sanskriti)
├── backend/                         # FastAPI Backend & Database (Abhishek Shukla)
│   ├── app/
│   │   ├── main.py                  # Server entry point, CORS & static mounts
│   │   ├── database.py              # SQLite database layer & repositories
│   │   ├── schemas.py               # Pydantic data schemas & contracts
│   │   ├── seed_data.py             # Product database initial seed
│   │   ├── routers/                 # Products, Buyer, Orders & AI API endpoints
│   │   └── services/                # Service layer & Orchestrator pipeline
│   ├── requirements.txt             # Python backend dependencies
│   └── A_TASK_LOG.md                # Backend development & integration log
├── docs/                            # Documentation & Architecture
│   ├── assets/                      # Official ShilpVani branding & logos
│   └── TEAM_PROGRESS.md             # Master team progress & QA sign-off record
├── frontend/                        # Mobile-First Web Application (Pratistha)
│   ├── public/                      # Static web assets & official favicon
│   ├── src/
│   │   ├── components/              # Artisan Wizard, Buyer Feed, Language Modal & Header
│   │   ├── constants/               # 7-language dictionary & craft categories
│   │   ├── context/                 # Application global state provider
│   │   ├── index.css                # Custom CSS design system & micro-animations
│   │   └── services/                # API client & local mock fallbacks
│   ├── package.json                 # Frontend dependencies & scripts
│   └── vite.config.js               # Vite build configuration
├── tests/                           # Automated Test Suite (Parth)
│   ├── test_api.py                  # Core backend API integration tests
│   ├── test_nlp_pipeline.py         # NLP & language contract tests
│   ├── test_vision.py               # Vision module & asset delivery tests
│   └── test_integration.py          # End-to-end multi-module pipeline tests
└── README.md                        # Project documentation
```

---

## ⚡ Setup & Installation Guide

### Prerequisites
* Python 3.10+ (Python 3.12 recommended)
* Node.js 18+ and `npm`

### 1. Clone & Setup Backend
```bash
# Clone the repository & enter workspace
git clone https://github.com/abhi03241/tantu-sih-26090.git
cd tantu-sih-26090
git checkout feature/A-backend

# Install Python dependencies
python -m pip install -r backend/requirements.txt

# Run FastAPI backend server
python -m backend.app.main
```
* Backend URL: `http://localhost:8000`
* Interactive API Documentation (Swagger): `http://localhost:8000/docs`

### 2. Setup & Run Frontend
```bash
# Enter frontend directory
cd frontend

# Install Node modules
npm install

# Start Vite development server
npm run dev

# Build production bundle
npm run build
```

---

## 🧪 Automated Testing & Verification

The repository features a 100% passing automated regression test suite:

```bash
# Run full python unittest suite
python -m unittest discover -s tests -p "test_*.py" -v
```

### Verified Test Results:
* **Backend & Integration Unittests**: **62/62 PASSED** (0 failures, 0 errors in 1.72s).
* **Frontend Production Build**: `npm run build --prefix frontend` **PASSED** (1610 modules transformed in 1.46s, 0 build errors).
* **Git Whitespace & Format Check**: `git diff --check` **PASSED** (0 whitespace/formatting issues).

---

## 👥 Team Members & Credits

| Member | Name | Technical Role & Responsibilities |
|---|---|---|
| **A** | **Abhishek Shukla** | **Tech Lead + Backend + Integration** — Core Architecture, FastAPI, SQLite, Schemas, Orchestrator & Master Integration |
| **P** | **Pratistha** | **Frontend / Mobile UI** — Mobile-first React UI, Artisan Wizard, Buyer Feed & Responsive Design System |
| **M** | **Manyata** | **AI / NLP + Voice + Multilingual Intelligence** — Voice Transcription, Indic Script NLP Parsing & 7-Language Parity |
| **R** | **Raj** | **Computer Vision + Image Enhancement** — Background Removal, Studio Lighting & Image Asset Delivery |
| **S** | **Sanskriti** | **Dynamic Pricing + B2B Marketplace** — Cost-Plus Pricing Engine, Volume Multipliers & Wholesale Order Requests |
| **Parth** | **Parth** | **Database + Testing + QA / Integration Support** — Unit & Integration Test Suite, Database Reliability & QA Auditing |

---

## 🔮 Future Scope & Roadmap

While ShilpVani currently operates as a fully functional demo prototype, future production deployment planned phases include:

* 🌐 **ONDC & GeM Network Integration**: Direct API connectors to list artisan products on Government e-Marketplace (GeM) and Open Network for Digital Commerce (ONDC).
* 💳 **Payment & Escrow Systems**: Integrated UPI/Razorpay payment processing with milestone-based escrow payouts protecting artisan earnings.
* 🚚 **Logistics & Shipping Partnerships**: Automated shipping label generation with regional postal and courier partners for door-to-door artisan pickups.
* 🤝 **Phygital Onboarding Network**: Partnering with Self-Help Groups (SHGs) and NGO cluster leads to onboard non-smartphone artisans through digital champions.
* 🗣️ **Extended Dialects**: Expanding voice recognition models to cover regional sub-dialects (Bhojpuri, Maithili, Odia, Dogri, Santhali).

---

<div align="center">
  <b>Developed for Smart India Hackathon (SIH 2026) — Problem Statement 26090</b>
</div>
