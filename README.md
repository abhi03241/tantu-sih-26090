<div align="center">
  <img src="docs/assets/shilpvani_logo.jpg" alt="ShilpVani Logo" width="180" style="border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.15);" />

  # ShilpVani (शिल्पवाणी)

  ### Multilingual Voice-First AI for Artisans

  *"We don't ask artisans to learn e-commerce. We use AI to make e-commerce understand artisans."*

  [![Backend Tests](https://img.shields.io/badge/Backend%20Tests-62%2F62%20PASSED-brightgreen.svg)](file:///d:/SIH2026/tests)
  [![Frontend Build](https://img.shields.io/badge/Frontend%20Build-PASSED%20(1610%20modules)-blue.svg)](file:///d:/SIH2026/frontend)
  [![Vercel Deployment](https://img.shields.io/badge/Vercel-Frontend%20Ready-black.svg)](file:///d:/SIH2026/vercel.json)
  [![SIH Readiness](https://img.shields.io/badge/SIH%20Prototype%20Readiness-70--75%25-orange.svg)](file:///d:/SIH2026/README.md)
</div>

---

## 🌟 Product Positioning

**ShilpVani (शिल्पवाणी)** is a **multilingual, voice-first AI platform** that helps rural and marginalized artisans turn their craft into professional digital catalogues and connect directly with B2B wholesale buyers.

> **Core Innovation**: Reducing the language and digital-literacy barrier between artisans and digital commerce through multilingual, voice-first AI.

---

## 🌐 Multilingual AI Platform

ShilpVani is designed as a **multilingual AI platform** rather than a single language-specific marketplace.

### Supported Interface Languages (Current Prototype)

The current prototype provides complete interface support, speech recognition routing, and translation parity across **seven Indian languages**:

1. **English** (`en`) — English
2. **Hindi** (`hi`) — हिन्दी
3. **Bengali** (`bn`) — বাংলা
4. **Marathi** (`mr`) — मराठी
5. **Assamese** (`as`) — অসমীয়া
6. **Tamil** (`ta`) — தமிழ்
7. **Telugu** (`te`) — తెలుగు

> *Platform Architecture*: The underlying software and AI model orchestration architecture is built for broader multilingual expansion across additional Indic dialects.

---

## 🔁 The AI Product Story & Journey

```text
ARTISAN SPEAKS NATURALLY
   │ (Voice note in native language + Craft Photo)
   ▼
MULTILINGUAL INPUT & SPEECH RECOGNITION
   │ (Speech-to-text + Regional dialect parsing)
   ▼
AI UNDERSTANDS THE CRAFT
   │ (Extracts material, dimensions, duration, heritage story)
   ▼
STRUCTURED PRODUCT DATA & IMAGE ENHANCEMENT
   │ (Bilingual descriptions + Studio backdrop + Fair wage estimation)
   ▼
PROFESSIONAL DIGITAL CATALOGUE
   │ (High-conversion marketplace listing)
   ▼
B2B MARKETPLACE & BULK ORDERS
   │ (Direct wholesale buyer discovery & order lifecycle tracking)
```

---

## 🚀 Cloud Deployment Architecture & Vercel Integration

ShilpVani uses a decoupled deployment model:

```text
┌────────────────────────────────────────────────────────┐
│                   Vercel Edge Network                  │
│  React 18 + Vite 6 Frontend SPA                        │
│  - High-Speed Global CDN Static Distribution          │
│  - SPA Routing Rewrites via vercel.json                │
│  - Configurable Build Env: VITE_API_BASE_URL           │
└───────────────────────────┬────────────────────────────┘
                            │ Cross-Origin HTTPS API Calls
                            ▼
┌────────────────────────────────────────────────────────┐
│               Persistent Python Cloud Host             │
│  FastAPI + Python 3.12 + SQLite + Pillow Asset Storage │
│  - Cloud Host: Render / Railway / Fly.io / AWS EC2     │
│  - Persistent SQLite Database (tantu.db)               │
│  - Persistent /uploads & /enhanced Static Asset Serving│
└────────────────────────────────────────────────────────┘
```

### 1. Frontend Vercel Deployment Guide
* **Vercel Root Directory**: `frontend/` (or repository root)
* **Build Command**: `npm run build` (or `npm run build --prefix frontend`)
* **Output Directory**: `dist` (or `frontend/dist`)
* **Environment Variables**:
  * `VITE_API_BASE_URL`: `https://<YOUR-BACKEND-HOST>.onrender.com`
  * `VITE_BACKEND_URL`: `https://<YOUR-BACKEND-HOST>.onrender.com`
* **Configuration Files**: Root [`vercel.json`](file:///d:/SIH2026/vercel.json) and [`frontend/vercel.json`](file:///d:/SIH2026/frontend/vercel.json) included in repository.

### 2. Backend Hosting Guide (Render / Railway / Fly.io)
* **Runtime**: Python 3.12
* **Build Command**: `pip install -r backend/requirements.txt`
* **Start Command**: `python -m backend.app.main` (or `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`)
* **Environment Variables**: `MOCK_AI=true`, `HOST=0.0.0.0`
* **CORS Middleware**: Pre-configured with `allow_origins=["*"]` to serve Vercel frontend domains.

---

## 📊 SIH Prototype Readiness: ~70–75%

### Core Capabilities Implemented (70–75%)
* ✅ **Multilingual interface & localization architecture** (7 Indic languages)
* ✅ **Voice-first artisan input & transcription routing**
* ✅ **AI-assisted catalogue generation & grounded narrative synthesis**
* ✅ **Studio image enhancement & non-destructive processing**
* ✅ **AI-assisted fair pricing estimation**
* ✅ **B2B marketplace discovery feed**
* ✅ **Bulk-order request submission & quantity pricing**
* ✅ **Order lifecycle state persistence** (`pending` → `accepted` → `fulfilled`)
* ✅ **Vercel frontend deployment configuration & decoupled backend API**

### Future Scope & Production Roadmap (25–30%)
* 🔮 **Additional Indian Languages**: Expanding voice recognition and NLP models to cover Bhojpuri, Maithili, Odia, Dogri, Santhali, and Khasi.
* 🔮 **Advanced Speech Dialect Models**: Fine-tuning whisper/wav2vec models for noisy rural environments and strong regional accents.
* 🔮 **Real Market-Price Datasets**: Integrating live handicraft export pricing datasets and Ministry of Textiles benchmarks.
* 🔮 **Payment & Escrow Systems**: Integrated UPI/Razorpay payment processing with milestone-based escrow payouts protecting artisan earnings.
* 🔮 **Logistics & Shipping Partnerships**: Automated shipping label generation with regional postal and courier partners for door-to-door artisan pickups.
* 🔮 **ONDC & GeM Network Connectors**: Direct integration with Open Network for Digital Commerce (ONDC) and Government e-Marketplace (GeM).
* 🔮 **Phygital Onboarding**: Partnering with Self-Help Groups (SHGs) and NGO cluster leads to onboard non-smartphone artisans through digital champions.

---

## 🛠️ Technology Stack

| Layer | Technology | Details |
|---|---|---|
| **Frontend UI (Vercel)** | React 18 + Vite 6 | SPA with CSS variables, glassmorphism, responsive grid & mobile bottom nav |
| **Backend Framework** | Python 3.12 / FastAPI | Asynchronous REST API server with Pydantic v2 schemas |
| **Database & Persistence** | SQLite 3 (`tantu.db`) | Relational persistence with raw parameterization & auto-seeding |
| **AI & NLP Processing** | Python 3.12 / RegEx / PIL | Devanagari/Indic script digit normalization, PIL image transformation |
| **Icons & Typography** | Lucide React / Google Fonts | Outfit, Noto Sans Devanagari, Rozha One |
| **Testing Suite** | Python `unittest` | Automated backend, NLP, vision, pricing & contract regression tests |

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

## ⚡ Setup & Installation Guide

### Prerequisites
* Python 3.10+ (Python 3.12 recommended)
* Node.js 18+ and `npm`

### 1. Clone & Setup Backend
```bash
git clone https://github.com/abhi03241/tantu-sih-26090.git
cd tantu-sih-26090
git checkout feature/A-backend

python -m pip install -r backend/requirements.txt
python -m backend.app.main
```
* Backend URL: `http://localhost:8000`
* Interactive API Documentation (Swagger): `http://localhost:8000/docs`

### 2. Setup & Run Frontend
```bash
cd frontend
npm install
npm run dev
npm run build
```

---

## 🧪 Automated Testing & Verification

```bash
# Run full python unittest suite
python -m unittest discover -s tests -p "test_*.py" -v
```

### Verified Test Results:
* **Backend & Integration Unittests**: **62/62 PASSED** (0 failures, 0 errors in 1.81s).
* **Frontend Production Build**: `npm run build --prefix frontend` **PASSED** (1610 modules transformed in 1.38s, 0 build errors).
* **Git Whitespace & Format Check**: `git diff --check` **PASSED** (0 whitespace/formatting issues).

---

<div align="center">
  <b>Developed for Smart India Hackathon (SIH 2026) — Problem Statement 26090</b>
</div>
