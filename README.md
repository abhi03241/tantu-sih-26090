# TANTU (तंतु) — AI-Driven Market Linkage & Smart Cataloging

> **Smart India Hackathon (SIH 2026) — Problem Statement 26090**  
> *AI-Driven Market Linkage and Smart Cataloging Mobile Application for Marginalized Artisans*

---

## 🌟 Overview

**TANTU** is an AI-powered prototype designed to empower rural and marginalized Indian artisans. It bridges the digital divide by transforming raw voice descriptions and basic phone photos into professional, multi-lingual, studio-grade product catalogs with fair market value pricing and direct B2B buyer connections.

---

## 🏗️ Architecture & Project Structure

```text
tantu-sih-26090/
├── frontend/                     # Mobile & Web UI (Member P)
│   └── README.md
├── backend/                      # FastAPI Backend & Persistence (Tech Lead A)
│   ├── app/
│   │   ├── main.py               # Main FastAPI server & CORS middleware
│   │   ├── config.py             # Environment configuration & MOCK_AI mode
│   │   ├── database.py           # SQLite database persistence layer
│   │   ├── schemas.py            # Pydantic validation & Common Product Contract
│   │   ├── seed_data.py          # Auto-seeding sample artisan products
│   │   └── routers/              # Endpoints (products, ai, artisan, buyer, orders)
│   ├── tantu.db                  # Local SQLite database
│   └── requirements.txt          # Dependencies
├── ai/                           # AI Submodules (Members M, R, S)
│   ├── nlp/                      # Voice-to-Text & Multi-lingual Storytelling (Member M)
│   ├── vision/                   # AI Background & Studio Image Enhancer (Member R)
│   └── pricing/                  # Fair Wage & Dynamic Pricing Engine (Member S)
├── data/
│   └── sample_products.json      # Pre-populated demo artisan products
├── docs/
│   ├── ARCHITECTURE.md           # Deep-dive architecture design
│   └── API_CONTRACTS.md          # REST API specifications & JSON contracts
├── tests/
│   └── test_api.py               # Automated unit & integration tests
├── .env.example                  # Environment template
└── README.md
```

---

## 🚀 Team Member Roles & Integration Matrix

| Role | Member | Responsibilities | Key Endpoints / Hooks |
|---|---|---|---|
| **Tech Lead + Backend** | **A** | Core Architecture, DB, API Contracts | FastAPI, SQLite, Pydantic, Routers |
| **Frontend / Mobile UI** | **P** | Mobile UI, Artisan & Buyer Dashboards | `GET /api/artisan/products`, `GET /api/buyer/products` |
| **AI / NLP / Voice** | **M** | Voice Processing, Hindi/English Story NLP | `ai/nlp/voice_and_story.py` -> `/voice`, `/generate-catalogue` |
| **AI Image Enhancement** | **R** | Studio Backdrop Cleanup & Image Upscaling | `ai/vision/image_enhancer.py` -> `/enhance-image` |
| **Pricing & Marketplace** | **S** | Fair Wage Pricing, B2B Order Requests | `ai/pricing/smart_pricing.py` -> `/price`, `/orders/request` |

---

## ⚡ Quickstart Guide

### 1. Prerequisites
- Python 3.10+ installed

### 2. Installation
```bash
# Clone the repository & switch to backend branch
git clone https://github.com/abhi03241/tantu-sih-26090.git
cd tantu-sih-26090
git checkout feature/A-backend

# Install dependencies
python -m pip install -r backend/requirements.txt
```

### 3. Run the Backend Server
```bash
python -m backend.app.main
```
The server will start at: `http://localhost:8000`  
Interactive Swagger API documentation: `http://localhost:8000/docs`

### 4. Run Automated Test Suite
```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## 🛠️ Mock AI Resilience Mode (Crucial for SIH Demo)

In `.env`, set `MOCK_AI=true` (enabled by default):
- Ensures **100% demo uptime** during live judging.
- All AI endpoints (Voice, Image Enhancement, Pricing) return deterministic, realistic sample data without requiring external API keys.
- Can be set to `MOCK_AI=false` when members M, R, and S attach live model endpoints.

---

## 📄 License
Developed for Smart India Hackathon (SIH) 2026.
