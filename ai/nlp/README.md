# AI NLP & Multilingual Voice Cataloging Submodule

> **TANTU (तंतु)** — Smart India Hackathon (SIH 2026) | Problem Statement **26090**  
> *AI-Driven Market Linkage and Smart Cataloging Mobile Application for Marginalized Artisans*  
> **Module Lead**: Team Member M (AI / NLP / Voice / Sentiment)

---

## 1. Pipeline Overview

The TANTU NLP pipeline converts informal, spoken regional voice descriptions by rural artisans into structured, multi-lingual, market-ready e-commerce catalog entries.

```text
  [ ARTISAN VOICE ]
         │
         ▼
  [ Speech-to-Text (STT) ] ──────────► Audio bytes/base64 transcribed into raw speech text
         │
         ▼
  [ Language Detection ] ────────────► Identifies Hindi (hi), English (en), or Hinglish
         │
         ▼
  [ Normalization & Translation ] ───► Maps transliterated / regional speech to Hindi & English
         │
         ▼
  [ Product Info Extraction ] ───────► Extracts Title, Category, Material, Dimensions, Production Time, Tags
         │
         ▼
  [ Story & Heritage Extraction ] ───► Extracts artisan's generational heritage, master lineage, community roots
         │
         ▼
  [ Sentiment / Narrative Class. ] ──► Classifies grounded sentiment & narrative categories
         │
         ▼
  [ Structured Output Validation ] ──► Pydantic-validated JSON matching Common Product Contract
```

---

## 2. Supported Languages

| Language | Code | Voice Transcription | Extraction & Cataloging | Status in Prototype |
|---|---|---|---|---|
| **Hindi (हिंदी)** | `hi` | Supported (Devanagari script) | Full (Bilingual output: Hindi + English) | Production Ready |
| **English** | `en` | Supported (Latin script) | Full (Bilingual output: English + Hindi) | Production Ready |
| **Hinglish (Colloquial)** | `hi-Latn` | Supported (Phonetic Latin) | Full (Normalized & mapped to Hindi + English) | Production Ready |
| *Regional Indic (Bengali, Tamil, etc.)* | `bn`, `ta`, `te` | Architecture extensible | Extensible via IndicNLP / LLM tokenizers | Ready for Phase 2 |

*Note: We do not claim unsupported coverage of 20+ languages in this college-level prototype. Hindi, Hinglish, and English are fully supported and verified.*

---

## 3. Sentiment & Heritage Classification

Sentiment analysis in TANTU is an **innovation layer** for cultural preservation, not an exaggerated emotional claim. We strictly avoid ungrounded marketing assertions like *"AI understands human emotions perfectly"*.

Instead, we classify artisan stories into pragmatic, authentic categories:

### Sentiment Categories:
- `positive`: Genuine enthusiasm and creative pride.
- `neutral`: Objective, matter-of-fact product description.
- `heritage`: Longstanding ancestral craft background.
- `family tradition`: Craft learned from parents, grandparents, or elders.
- `craftsmanship pride`: High dedication to precision, fine technique, and handiwork.
- `cultural significance`: Rooted in regional festivals, rituals, or tribal motifs.

### Narrative Types:
- `family_tradition`
- `cultural_heritage`
- `craftsmanship_pride`
- `community_empowerment`
- `standard_narrative`

---

## 4. Input & Output Contract

### A. Input Payload (Artisan Voice / Text)
```json
{
  "audio_transcript": "Ye bamboo ki tokri hai. Isko banane mein mujhe do din lagte hain. Meri maa ne mujhe ye banana sikhaya tha.",
  "language": "hi"
}
```

### B. Output JSON (Shared Product Contract)
The output strictly complies with `ProductBase` in `backend/app/schemas.py`:

```json
{
  "title": "Bamboo Basket",
  "description_english": "Handcrafted eco-friendly bamboo basket woven using traditional regional techniques. Durable, lightweight, and sustainably made from natural bamboo for versatile everyday and decorative utility.",
  "description_hindi": "प्राकृतिक बांस से बनी हस्तनिर्मित पर्यावरण-अनुकूल टोकरी। पारंपरिक तकनीक से तैयार, हल्की और टिकाऊ।",
  "category": "Bamboo & Cane Craft",
  "material": "Bamboo",
  "dimensions": null,
  "production_time": "2 days",
  "tags": [
    "bamboo",
    "handmade",
    "traditional",
    "basket",
    "eco-friendly"
  ],
  "story": "Learned the craft from mother: an inherited craft tradition taught by the artisan's mother.",
  "sentiment": "positive",
  "narrative_type": "family_tradition",
  "detected_language": "hi",
  "raw_transcript": "Ye bamboo ki tokri hai. Isko banane mein mujhe do din lagte hain. Meri maa ne mujhe ye banana sikhaya tha."
}
```

---

## 5. Architecture & Provider Abstraction (`NLPService`)

To prevent vendor lock-in and guarantee **100% demo uptime** during hackathon judging, the codebase implements an abstraction pattern:

```text
                      [ NLPService (Abstract Interface) ]
                                      ▲
                         ┌────────────┴────────────┐
                         │                         │
               [ MockNLPService ]          [ RealNLPService ]
              (Deterministic Demo)      (Gemini / OpenAI / Whisper)
                         │                         │
                         └────────────┬────────────┘
                                      │
                         [ get_nlp_service() Factory ]
```

### Provider Configuration in `.env`:
```ini
# Mock AI mode: true guarantees 100% uptime with deterministic demo scenarios
MOCK_AI=true

# Optional external credentials (used when MOCK_AI=false)
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### Automatic Fallback Resilience:
If `MOCK_AI=false` is selected but:
- API key is missing or expired,
- Network connection drops,
- Upstream rate limits are hit, or
- Upstream returns invalid JSON,

`RealNLPService` **automatically catches the error and falls back to `MockNLPService`**, ensuring the server never throws an unhandled 500 error during an artisan presentation.

---

## 6. Core Demo Cases

### Case 1: Hindi Bamboo Basket
- **Artisan Voice Input**: `"Ye bamboo ki tokri hai. Isko banane mein mujhe do din lagte hain. Meri maa ne mujhe ye banana sikhaya tha."`
- **Extracted Title**: `Bamboo Basket`
- **Material**: `Bamboo`
- **Production Time**: `2 days`
- **Story**: `Learned the craft from mother: an inherited craft tradition taught by the artisan's mother.`
- **Narrative**: `family_tradition` | **Sentiment**: `positive`

### Case 2: Hindi Handwoven Textile
- **Artisan Voice Input**: `"Yeh haath se buna hua Chanderi silk dupatta hai. Isme paanch din lagte hain. Humari peedhiyan yeh kaam karti aa rahi hain."`
- **Extracted Title**: `Handwoven Chanderi Silk Dupatta`
- **Material**: `Chanderi Silk`
- **Production Time**: `5 days`
- **Story**: `Ancestral weaving craft passed down through multiple generations, continuing a proud regional textile heritage.`
- **Narrative**: `cultural_heritage` | **Sentiment**: `craftsmanship pride`

### Case 3: English Wooden Craft
- **Artisan Voice Input**: `"This is a hand-carved teak wood elephant sculpture. It takes around four days to carve and polish. I learned wood carving from my grandfather with great pride."`
- **Extracted Title**: `Hand-Carved Teak Wood Elephant`
- **Material**: `Teak Wood`
- **Production Time**: `4 days`
- **Story**: `Wood carving technique passed down from grandfather, practiced with deep devotion and artisan pride.`
- **Narrative**: `craftsmanship_pride` | **Sentiment**: `positive`

---

## 7. Error Handling & Edge Cases

| Scenario | System Behavior |
|---|---|
| **Empty Voice / Whitespace** | Returns safe default handcrafted draft with `"neutral"` sentiment and helpful guidance prompts. |
| **Unsupported Language** | Gracefully identifies closest linguistic family (defaults to Hindi/English) without crashing. |
| **Missing Production Time** | Defaults to standard artisan baseline (`"2-3 days"`) or leaves null. |
| **Transcription Failure** | Trapped safely; returns diagnostic notification in response payload. |
| **Malformed AI Provider JSON** | Pydantic validation interceptor catches format issues and fills default fields. |

---

## 8. Limitations & Future Scope

1. **Audio Noise in Rural Markets**: Background ambient noise (bazaars, looms) may degrade raw STT; in Phase 2, a spectral noise subtraction filter will precede transcription.
2. **Dialect Nuances**: Prototype focuses on Standard Hindi, Hinglish, and English. Regional dialects (Bhojpuri, Maithili, Awadhi) are mapped through phonetic heuristics in the current version.
3. **No Heavy Custom Models**: Operates within SIH resource constraints by utilizing lightweight APIs, rule-based heuristics, and standard Python libraries rather than unneeded 10GB local models.
