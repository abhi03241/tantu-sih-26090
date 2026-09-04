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
- **Commit Hash**: Pending commit
- **Branch**: `feature/M-ai-nlp`
