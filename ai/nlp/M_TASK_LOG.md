# TANTU (SIH 26090) — Team Member M Task Log
**Role**: AI / NLP + Voice + Sentiment Developer  
**Branch**: `feature/M-ai-nlp`  
**Problem Statement**: 26090 — AI-Driven Market Linkage and Smart Cataloging Mobile Application for Marginalized Artisans  

---

## Checkpoint 1: NLP Service Foundation

- **Step**: Checkpoint 1 — NLP Service Foundation
- **Implementation**:
  - Established a robust provider abstraction `NLPService` with `MockNLPService` and `RealNLPService`.
  - Created backend service bridge `backend/app/services/nlp_service.py` to allow clean invocation from both backend routes and standalone AI scripts.
  - Implemented deterministic mock mode (`MOCK_AI=true`) ensuring 100% demo resilience during SIH judging.
  - Verified compatibility with the shared Product schema contract in `backend/app/schemas.py`.
- **Files**:
  - `backend/app/services/nlp_service.py` (Created)
  - `backend/app/services/__init__.py` (Created)
  - `ai/nlp/service.py` (Verified & Integrated)
  - `ai/nlp/M_TASK_LOG.md` (Created)
- **API / Interface**:
  - `BackendNLPService.process_artisan_input(text, language)`
  - `BackendNLPService.process_audio(audio_bytes, language)`
  - `BackendNLPService.generate_catalogue(product_info)`
  - `get_nlp_service(mock: bool) -> NLPService`
- **Tests**:
  - `python -m unittest tests/test_nlp_pipeline.py -v`
  - `python -m unittest tests/test_api.py -v`
- **Results**: 13/13 NLP tests passed; 10/10 API tests passed (23/23 total).
- **Issues**: Remote push to `origin feature/M-ai-nlp` requires GitHub collaborator write permission for user `ikuhu19`.
- **Integration Notes**:
  - Compatible with `POST /api/products/{id}/voice` and `ProductBase`.
- **Commit Message**: `feat: establish artisan NLP service`
- **Commit Hash**: `bca7f86`
- **Branch**: `feature/M-ai-nlp`

---

## Checkpoint 2: Structured Catalogue Generation

- **Step**: Checkpoint 2 — Structured Catalogue Generation
- **Implementation**:
  - Implemented extraction of Title, Description (English & Hindi), Category, Material, Dimensions, Production time, and Tags.
  - Added strict anti-hallucination guarantees: unstated optional fields like `dimensions` and `production_time` remain `None` (`null`) instead of fabricating values.
  - Implemented regex-based dimension extractor for explicit sizes (e.g., `40cm x 40cm x 45cm`, `2.5m x 0.9m`).
  - Added dynamic `extract_craft_title` generating professional titles from artisan craft materials and types without e-commerce jargon.
  - Added new demo scenario for SIH prompt case: *"This is a handwoven cotton dupatta made by our women's group. It takes three days to make and uses traditional weaving patterns."*
- **Files**:
  - `ai/nlp/demo_data.py` (Modified)
  - `ai/nlp/service.py` (Modified)
  - `tests/test_nlp_pipeline.py` (Modified)
  - `ai/nlp/M_TASK_LOG.md` (Modified)
- **API / Interface**:
  - `extract_dimensions(text: str) -> Optional[str]`
  - `extract_craft_title(text: str, material: str, category: str) -> str`
  - `ProductCatalogNLPOutput.to_product_dict()`
- **Tests**:
  - `test_cotton_dupatta_women_group_example`
  - `test_dimensions_extraction_and_no_hallucination`
  - `test_missing_fields_graceful_defaults`
- **Results**: 15/15 NLP tests passed.
- **Issues**: None. Push to remote blocked by GitHub 403 on user `ikuhu19`.
- **Integration Notes**: Output directly populates SQLite database through FastAPI product repository without schema migration.
- **Commit Message**: `feat: structured catalogue generation with anti-hallucination rules`
- **Commit Hash**: Pending commit
- **Branch**: `feature/M-ai-nlp`
