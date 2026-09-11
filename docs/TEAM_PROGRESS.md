# TANTU Team Progress

## M — NLP and Voice: Mobile/APK Verification (2026-09-10)

- Inspected the existing `Voice/Text → NLP → Catalogue Fields → Product` route.
- The mobile-compatible request remains `{ "audio_transcript": string, "language": "hi" | "en" }`; no product JSON contract change was made.
- The voice endpoint persists only explicitly extracted dimensions and production time, preventing missing voice details from overwriting known product data.
- Verified English, Hindi (including `3 दिन`), raw narrative notes, dimensions, production time, and underspecified input.
- Executed the full existing suite: **26/26 passed**.
- No code change was required. The active branch does not include the React/Vite frontend, so native Capacitor speech-recognition behavior remains an integration-level verification item; its text-transcript contract is already compatible with the existing NLP endpoint.

## M — ShilpVani Multilingual NLP & Voice Flow Audit (2026-09-11)

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
- **Code Changes**: **None required.** No code changes made to NLP service, product JSON contract, Vision, Pricing, database, or frontend branding.
