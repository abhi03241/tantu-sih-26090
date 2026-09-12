<div align="center">
  <img src="docs/assets/shilpvani_logo.jpg" alt="ShilpVani Logo" width="180" />

  # ShilpVani (शिल्पवाणी)

  ### Multilingual Voice-First AI for Artisans

  *"We don't ask artisans to learn e-commerce. We use AI to make e-commerce understand artisans."*
</div>

---

## 🌐 Live Project

**[https://shilpvani.vercel.app/](https://shilpvani.vercel.app/)**

---

## 🌟 Product Positioning

**ShilpVani (शिल्पवाणी)** is a multilingual, voice-first AI platform that helps rural and marginalized artisans turn their craft into professional digital catalogues and connect directly with B2B wholesale buyers.

> **Core Innovation:** Reducing the language and digital-literacy barrier between artisans and digital commerce through multilingual, voice-first AI.

## 🌐 Multilingual AI Platform

The current prototype provides complete interface support, speech recognition routing, and translation parity across seven Indian languages:

1. English (`en`)
2. Hindi (`hi`)
3. Bengali (`bn`)
4. Marathi (`mr`)
5. Assamese (`as`)
6. Tamil (`ta`)
7. Telugu (`te`)

The platform architecture is designed for broader multilingual expansion across additional Indic dialects.

---

## 🔁 The AI Product Journey

```text
ARTISAN SPEAKS NATURALLY
   │ Voice note in native language + craft photo
   ▼
MULTILINGUAL INPUT & SPEECH RECOGNITION
   ▼
AI UNDERSTANDS THE CRAFT
   │ Material, dimensions, duration, heritage story
   ▼
STRUCTURED PRODUCT DATA & IMAGE ENHANCEMENT
   ▼
PROFESSIONAL DIGITAL CATALOGUE
   ▼
B2B MARKETPLACE & BULK ORDERS
```

---

## 📋 Implementation Roadmap

**[Download the one-page PDF roadmap](docs/assets/ShilpVani_Implementation_Roadmap.pdf)** - landscape A4 and PPT-ready.

Also available as:

- **[High-resolution PNG preview](docs/assets/ShilpVani_Implementation_Roadmap.png)** - 2339 x 1654 px at 200 DPI
- **[Editable generator source](docs/assets/generate_implementation_roadmap.py)** - recreates the vector PDF and high-error-correction QR code

| Phase | Status label | Focus |
|---|---|---|
| 1 | Current Prototype | AI pipeline, seven-language interface, B2B marketplace, bulk orders, automated testing |
| 2 | Next Implementation | Vercel and Render pilot, persistent storage, authentication, monitoring, real-artisan validation |
| 3 | Intelligence & Scale | Regional price data, stronger NLP, async processing, workers, caching, analytics |
| 4 | Future Scale | ONDC, institutional buyers, partnerships, logistics, payments, community onboarding |

---

## 🚀 Cloud Deployment Architecture & Vercel Integration

ShilpVani uses a decoupled deployment model:

```text
Vercel Edge Network
React 18 + Vite 6 frontend SPA
   │ Cross-origin HTTPS API calls
   ▼
Persistent Python Cloud Host
FastAPI + Python 3.12 + SQLite + Pillow asset storage
```

### Frontend deployment

- **Vercel root directory:** `frontend/` (or repository root)
- **Build command:** `npm run build` (or `npm run build --prefix frontend`)
- **Output directory:** `dist` (or `frontend/dist`)
- **Environment variables:** `VITE_API_BASE_URL` or `VITE_BACKEND_URL`
- **Configuration:** `vercel.json` and `frontend/vercel.json`

### Backend hosting

- **Runtime:** Python 3.12
- **Build command:** `pip install -r backend/requirements.txt`
- **Start command:** `python -m backend.app.main`
- **Environment variables:** `MOCK_AI=true`, `HOST=0.0.0.0`

---

## 📊 SIH Prototype Readiness: ~70-75%

### Core capabilities implemented

- Multilingual interface and localization architecture for seven Indic languages
- Voice-first artisan input and transcription routing
- AI-assisted catalogue generation and image enhancement
- AI-assisted fair pricing estimation
- B2B marketplace discovery and bulk-order requests
- Persistent order lifecycle states
- Vercel deployment configuration and decoupled backend API

### Future scope

- Additional Indian languages and dialect-aware speech models
- Real market-price datasets
- Payments, escrow, and logistics integrations
- ONDC and GeM network connectors
- Community-led artisan onboarding

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React 18 + Vite 6 |
| Backend | Python 3.12 + FastAPI |
| Database | SQLite 3 |
| AI processing | Python, regex, Pillow |
| UI | Lucide React, Outfit, Noto Sans Devanagari, Rozha One |
| Testing | Python `unittest` |

---

## 👥 Team Members & Credits

| Member | Technical role and responsibilities |
|---|---|
| **Abhishek Shukla** | Tech Lead + Backend + Integration |
| **Maanyta** | AI/NLP + Voice + Multilingual Intelligence |
| **Raj** | Computer Vision + Image Enhancement |
| **Pratishtha** | Frontend / Mobile UI |
| **Sanskriti** | Dynamic Pricing + B2B Marketplace |
| **Parth** | Database + Testing + QA / Integration Support |

---

## ⚡ Setup & Installation

```bash
git clone https://github.com/abhi03241/tantu-sih-26090.git
cd tantu-sih-26090

python -m pip install -r backend/requirements.txt
python -m backend.app.main
```

Run the frontend:

```bash
cd frontend
npm install
npm run dev
```

Run automated tests:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

<div align="center">
  <b>Developed for Smart India Hackathon (SIH 2026) - Problem Statement 26090</b>
</div>
