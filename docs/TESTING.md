# TANTU — Testing & Quality Assurance Guide

> **Smart India Hackathon (SIH 2026) — Problem Statement 26090**  
> *AI-Driven Market Linkage and Smart Cataloging Mobile Application for Marginalized Artisans*  
> **Maintained by Parth (Database + Testing + Integration Lead)**

---

## 🌟 Overview

This document details the automated testing framework, database persistence layer, integration verification workflows, and mock resilience mode for **TANTU**.

---

## 1. 🚀 How to Run Tests

### Prerequisites
Ensure dependencies are installed:
```bash
python -m pip install -r backend/requirements.txt
```

### Run All Unit & Integration Tests
Execute standard Python `unittest` discovery across the `tests/` directory:
```bash
python -m unittest discover -s tests -p "test_*.py"
```

### Run Specific Test Modules
```bash
# Run unit & API contract tests
python -m unittest tests/test_api.py

# Run end-to-end artisan-to-buyer smoke test
python tests/test_smoke_integration.py
```

---

## 2. 🧪 What is Being Tested

### A. Product Entity & Persistence
* **Product Creation (`POST /api/products`)**:
  * Validates JSON schema against the **Common Product Contract**.
  * Auto-generates unique IDs (`prod-xxxxxxxx`) and ISO timestamps.
  * Defaults fallback pricing bounds if omitted by user.
* **Product Retrieval (`GET /api/products/{id}`)**:
  * Fetches complete product details from SQLite database.
  * Returns `404 Not Found` for non-existent product IDs.
* **Catalog Listing & Filtering (`GET /api/products`)**:
  * Category filtering (`?category=Bamboo`).
  * Artisan filtering (`?artisan_id=art-001`).
  * Case-insensitive full-text search across titles, descriptions, Hindi narratives, materials, and tags (`?q=chanderi`).
* **Product Deletion (`DELETE /api/products/{id}`)**:
  * Deletes record cleanly and confirms deletion status.

### B. Catalogue Generation & Validation
* **Required Fields Enforcement**:
  * Missing mandatory fields (`title`, `image_url`) trigger `422 Unprocessable Entity`.
* **Missing Optional Fields**:
  * Optional fields (`dimensions`, `production_time`, `story`, `sentiment`) are handled gracefully without application crashes.
* **Bilingual Storytelling & Tagging (`POST /api/products/{id}/generate-catalogue`)**:
  * NLP module expands raw artisan notes into rich English and Hindi descriptions, cultural heritage narratives, and marketplace tags.
* **Malformed Input Handling (`POST /api/products/{id}/voice`)**:
  * Missing transcript triggers `422`. Empty transcript triggers safe fallback without data corruption.

### C. Smart Fair Wage Pricing Engine
* **Calculated Pricing (`POST /api/products/{id}/price`)**:
  * Computes fair minimum and maximum price bounds (`suggested_price_min`, `suggested_price_max`) based on raw material costs and craft complexity.
* **Missing Inputs**:
  * Empty payload falls back to regional craft category base multipliers.
* **Price Range Validity**:
  * Enforces `suggested_price_min > 0` and `suggested_price_max >= suggested_price_min`.

### D. B2B Order Requests & Linkage
* **Bulk Purchase Submission (`POST /api/orders/request`)**:
  * Generates order ID (`ord-xxxxxxxx`), associates product and artisan, and sets initial status to `pending`.
* **Quantity Validation**:
  * Rejects `quantity <= 0` with `422 Unprocessable Entity`.
* **Missing Product**:
  * Submitting an order for a non-existent product ID returns `404 Not Found`.
* **Order Lifecycle & Status Management (`PATCH /api/orders/{id}/status`)**:
  * Tests status transitions: `pending` -> `accepted` -> `in_production` -> `fulfilled`.
  * Rejects invalid statuses with `400 Bad Request`.

### E. AI Submodule Integration
* **Schema Conformance**:
  * Ensures outputs from Voice (Member M), Vision (Member R), NLP Story (Member M), and Pricing (Member S) integrate directly into the common Product model.
  * Verifies database persistence after each AI transformation step.

---

## 3. 🛡️ Mock AI Resilience Mode (`MOCK_AI=true`)

For hackathon jury evaluations and live demonstrations, external AI APIs (OpenAI, HuggingFace, Stability AI) might experience latency, rate limits, or connectivity failures. 

TANTU includes a **zero-credential deterministic fallback mode**:
* Configured via `.env`: `MOCK_AI=true` (enabled by default).
* **Voice NLP**: Synthesizes structured bilingual descriptions and cultural narratives.
* **Vision**: Generates high-definition studio backdrop URLs with realistic enhancement metadata.
* **Pricing**: Calculates mathematical fair trade pricing based on artisan labor hours and craft categories.
* **Guarantee**: The entire prototype will never crash or fail due to external AI unreachability.

---

## 4. 🔄 End-to-End API Smoke Test

The smoke test (`tests/test_smoke_integration.py`) validates the live 8-step user journey:

```text
[Step 1] Artisan uploads raw product draft
         ↓
[Step 2] Artisan speaks Hindi voice note (Voice NLP processing)
         ↓
[Step 3] AI Vision cleans backdrop and enhances studio photo
         ↓
[Step 4] Smart Pricing calculates fair artisan wage bounds
         ↓
[Step 5] AI generates bilingual marketing catalog & tags
         ↓
[Step 6] B2B Buyer searches marketplace & discovers product
         ↓
[Step 7] Buyer submits bulk purchase request (B2B order)
         ↓
[Step 8] Artisan accepts order and marks in-production
```

Run this anytime to verify the entire system:
```bash
python tests/test_smoke_integration.py
```

---

## 5. ⚠️ Known Limitations & Integration Boundaries

1. **Local SQLite Concurrency**:
   * SQLite is used for prototype simplicity and zero-configuration local execution. Multi-process write concurrency is limited.
2. **Audio File Processing**:
   * Voice endpoints currently accept text audio transcripts (`audio_transcript`). Direct binary `.wav`/`.mp3` upload processing is handled on the mobile frontend client via speech recognition before reaching this endpoint.
3. **Authentication**:
   * For prototype evaluation, user authorization tokens are simplified; artisan and buyer IDs are passed as headers/query parameters.
