"""
NLP Service Interface & Providers for TANTU (SIH PS 26090)
Provides provider abstraction (MockNLPService & RealNLPService) with safe fallbacks.
"""
import os
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

import httpx

from ai.nlp.schemas import (
    ProductCatalogNLPOutput,
    VoiceTranscriptionResult,
)
from ai.nlp.demo_data import (
    DEMO_SCENARIOS,
    detect_language,
    extract_material_and_category,
    extract_production_time,
    extract_dimensions,
    extract_craft_title,
    extract_story_and_sentiment,
    generate_bilingual_descriptions,
)

logger = logging.getLogger(__name__)


# ==========================================================
# BASE NLP SERVICE INTERFACE
# ==========================================================
class NLPService(ABC):
    """
    Abstract interface for TANTU AI/NLP & Voice Processing.
    Enables zero-friction switching between deterministic mock mode and live LLM/STT APIs.
    """

    @abstractmethod
    def transcribe_audio(self, audio_bytes: bytes, language: Optional[str] = "hi") -> VoiceTranscriptionResult:
        """Transcribe raw audio bytes into text."""
        pass

    @abstractmethod
    def process_transcript(self, transcript: str, language: Optional[str] = None) -> ProductCatalogNLPOutput:
        """
        Extracts structured product JSON, storytelling, and sentiment from an artisan speech transcript.
        """
        pass

    @abstractmethod
    def process_voice(
        self,
        audio_bytes: Optional[bytes] = None,
        transcript: Optional[str] = None,
        language: Optional[str] = None
    ) -> ProductCatalogNLPOutput:
        """
        Unified pipeline endpoint: accepts either raw audio or pre-transcribed text.
        """
        pass

    @abstractmethod
    def generate_catalogue(self, product_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates enriched marketing narrative, tags, and bilingual descriptions for an existing product.
        """
        pass


# ==========================================================
# MOCK NLP SERVICE (SIH Resilience Engine)
# ==========================================================
class MockNLPService(NLPService):
    """
    Deterministic & heuristic mock provider.
    Guarantees 100% uptime, zero external API costs, and predictable testable outputs for SIH judging.
    """

    def transcribe_audio(self, audio_bytes: bytes, language: Optional[str] = "hi") -> VoiceTranscriptionResult:
        """
        Simulates accurate STT for college prototype demo.
        """
        if not audio_bytes or len(audio_bytes) == 0:
            return VoiceTranscriptionResult(
                transcript="Ye bamboo ki tokri hai. Isko banane mein mujhe do din lagte hain. Meri maa ne mujhe ye banana sikhaya tha.",
                detected_language="hi",
                confidence=0.98,
                duration_seconds=4.5
            )

        return VoiceTranscriptionResult(
            transcript="Ye bamboo ki tokri hai. Isko banane mein mujhe do din lagte hain. Meri maa ne mujhe ye banana sikhaya tha.",
            detected_language=language or "hi",
            confidence=0.96,
            duration_seconds=3.8
        )

    def process_transcript(self, transcript: str, language: Optional[str] = None) -> ProductCatalogNLPOutput:
        """
        Transforms raw artisan speech or text transcript into structured product catalog JSON.
        Handles demo scenarios, pattern heuristics, and safe fallbacks for edge cases.
        """
        # Edge case: Empty or whitespace-only voice transcript
        if not transcript or not transcript.strip():
            return ProductCatalogNLPOutput(
                title="हस्तनिर्मित पारंपरिक क्राफ्ट (Handcrafted Artisan Craft)",
                description_english="Handcrafted regional artisan craft awaiting voice description. Created using authentic traditional techniques.",
                description_hindi="कारीगर द्वारा निर्मित पारंपरिक हस्तशिल्प। प्रामाणिक क्षेत्रीय तकनीकों से तैयार।",
                category="Handicrafts & Decor",
                material="Natural Artisan Material",
                dimensions=None,
                production_time=None,
                tags=["handcrafted", "artisanal", "authentic", "regional-art", "eco-friendly"],
                story=None,
                sentiment="Neutral",
                narrative_type=None,
                detected_language="hi",
                raw_transcript="",
            )

        clean_text = transcript.strip()
        detected_lang = language or detect_language(clean_text)
        lower = clean_text.lower()

        # Step 1: Check against known SIH demo scenarios
        for key, scenario in DEMO_SCENARIOS.items():
            keywords = scenario["keywords"]
            if any(kw in lower for kw in keywords):
                data = scenario["data"].copy()
                data["raw_transcript"] = clean_text
                data["detected_language"] = language or detect_language(clean_text)
                # If production time is explicitly mentioned differently, extract it
                custom_time = extract_production_time(clean_text)
                data["production_time"] = custom_time
                # If dimensions are explicitly mentioned, extract them
                custom_dim = extract_dimensions(clean_text)
                if custom_dim:
                    data["dimensions"] = custom_dim
                # Narrative and sentiment must come from the current transcript,
                # not from a similarly named demo scenario.
                story, sentiment, narrative_type = extract_story_and_sentiment(clean_text)
                data["story"] = story
                data["sentiment"] = sentiment
                data["narrative_type"] = narrative_type
                data["description_english"], data["description_hindi"] = generate_bilingual_descriptions(
                    clean_text, data["material"], data["category"], data["title"], data["detected_language"]
                )
                return ProductCatalogNLPOutput(**data)

        # Step 2: Intelligent Heuristic Extraction for Arbitrary Artisan Input
        material, category = extract_material_and_category(clean_text)
        prod_time = extract_production_time(clean_text)  # None if not communicated
        dimensions = extract_dimensions(clean_text)      # None if not communicated
        story, sentiment, narrative_type = extract_story_and_sentiment(clean_text)

        # Build Title accurately based on genuine craft attributes
        title = extract_craft_title(clean_text, material, category)

        # Build Descriptions
        desc_en, desc_hi = generate_bilingual_descriptions(
            clean_text=clean_text,
            material=material,
            category=category,
            title=title,
            detected_lang=detected_lang
        )

        tags = [
            category.lower().replace(" & ", "-").replace(" ", "-"),
            material.lower().replace(" ", "-"),
            "handcrafted",
            "traditional",
            "artisan"
        ]

        return ProductCatalogNLPOutput(
            title=title,
            description_english=desc_en,
            description_hindi=desc_hi,
            category=category,
            material=material,
            dimensions=dimensions,
            production_time=prod_time,
            tags=tags,
            story=story,
            sentiment=sentiment,
            narrative_type=narrative_type,
            detected_language=detected_lang,
            raw_transcript=clean_text
        )

    def process_voice(
        self,
        audio_bytes: Optional[bytes] = None,
        transcript: Optional[str] = None,
        language: Optional[str] = None
    ) -> ProductCatalogNLPOutput:
        """
        Unified entrypoint: transcribes audio if needed, then processes text.
        """
        if audio_bytes and not transcript:
            stt_res = self.transcribe_audio(audio_bytes, language=language)
            transcript = stt_res.transcript
            language = stt_res.detected_language

        return self.process_transcript(transcript or "", language=language)

    def generate_catalogue(self, product_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates enriched marketing narrative and storytelling tags.
        """
        title = product_info.get("title", "Handcrafted Artisan Item")
        category = product_info.get("category", "Handicrafts & Decor")
        material = product_info.get("material", "Natural Material")
        raw_notes = product_info.get("raw_notes") or product_info.get("description_english", "")
        story, sentiment, narrative_type = extract_story_and_sentiment(raw_notes)

        return {
            "description_english": f"{title} made from {material}. {raw_notes}".strip(),
            "description_hindi": f"{material} से निर्मित {title}। {raw_notes}".strip(),
            "category": category,
            "material": material,
            "tags": [
                category.lower().replace(" & ", "-").replace(" ", "-"),
                material.lower().replace(" ", "-"),
                "handcrafted"
            ],
            "story": story,
            "sentiment": sentiment,
            "narrative_type": narrative_type,
        }


# ==========================================================
# REAL NLP SERVICE (Live LLM & API Integration with Fallback)
# ==========================================================
class RealNLPService(NLPService):
    """
    Live AI service integration (Gemini / OpenAI / Groq / Whisper).
    Calls external APIs via lightweight HTTP requests.
    Automatically and safely falls back to MockNLPService on network error or missing keys.
    """

    def __init__(self, fallback_service: Optional[NLPService] = None):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.fallback = fallback_service or MockNLPService()

    def transcribe_audio(self, audio_bytes: bytes, language: Optional[str] = "hi") -> VoiceTranscriptionResult:
        """
        Calls OpenAI Whisper API or falls back safely to mock STT.
        """
        if not audio_bytes or len(audio_bytes) == 0:
            return self.fallback.transcribe_audio(audio_bytes, language=language)

        if self.openai_api_key:
            try:
                headers = {"Authorization": f"Bearer {self.openai_api_key}"}
                files = {"file": ("audio.wav", audio_bytes, "audio/wav")}
                data = {"model": "whisper-1", "language": language or "hi"}
                with httpx.Client(timeout=15.0) as client:
                    resp = client.post(
                        "https://api.openai.com/v1/audio/transcriptions",
                        headers=headers,
                        files=files,
                        data=data
                    )
                    if resp.status_code == 200:
                        text = resp.json().get("text", "")
                        return VoiceTranscriptionResult(
                            transcript=text,
                            detected_language=language or "hi",
                            confidence=0.95
                        )
            except Exception as e:
                logger.warning(f"Whisper API call failed, falling back to mock: {e}")

        # Safe fallback
        return self.fallback.transcribe_audio(audio_bytes, language=language)

    def process_transcript(self, transcript: str, language: Optional[str] = None) -> ProductCatalogNLPOutput:
        """
        Uses Gemini or OpenAI API to extract structured product JSON.
        Falls back to MockNLPService on any failure or missing credentials.
        """
        if not transcript or not transcript.strip():
            return self.fallback.process_transcript(transcript, language=language)

        # 1. Try Gemini API if key is present
        if self.gemini_api_key:
            try:
                result = self._call_gemini_extract(transcript, language)
                if result:
                    return result
            except Exception as e:
                logger.warning(f"Gemini API extraction failed, attempting fallback: {e}")

        # 2. Try OpenAI API if key is present
        if self.openai_api_key:
            try:
                result = self._call_openai_extract(transcript, language)
                if result:
                    return result
            except Exception as e:
                logger.warning(f"OpenAI API extraction failed, attempting fallback: {e}")

        # 3. Graceful fallback to deterministic mock engine
        return self.fallback.process_transcript(transcript, language=language)

    def process_voice(
        self,
        audio_bytes: Optional[bytes] = None,
        transcript: Optional[str] = None,
        language: Optional[str] = None
    ) -> ProductCatalogNLPOutput:
        if audio_bytes and not transcript:
            stt_res = self.transcribe_audio(audio_bytes, language=language)
            transcript = stt_res.transcript
            language = stt_res.detected_language

        return self.process_transcript(transcript or "", language=language)

    def generate_catalogue(self, product_info: Dict[str, Any]) -> Dict[str, Any]:
        """Enriches existing product catalogue."""
        return self.fallback.generate_catalogue(product_info)

    # ------------------------------------------------------
    # Internal LLM API Helpers
    # ------------------------------------------------------
    def _get_system_prompt(self) -> str:
        return (
            "You are an AI assistant for TANTU / ShilpVani (SIH 26090), an app empowering rural Indian artisans. "
            "Convert raw artisan voice speech or transcript (in English, Hindi, Bengali, Marathi, Assamese, Tamil, or Telugu) "
            "into structured JSON conforming to this schema:\n"
            "{\n"
            '  "title": "Concise product title",\n'
            '  "description_english": "Professional product description in English",\n'
            '  "description_hindi": "Natural Hindi description for regional buyers/artisans",\n'
            '  "category": "Craft category e.g. Bamboo & Cane Craft, Textiles & Handloom, Woodcraft, Pottery & Ceramics",\n'
            '  "material": "Primary craft material",\n'
            '  "dimensions": null or string,\n'
            '  "production_time": "Production duration e.g. 2 days or null",\n'
            '  "tags": ["list", "of", "tags"],\n'
            '  "story": "Artisan story or family craft tradition or null",\n'
            '  "sentiment": "one of: Pride, Joy, Nostalgia, Passion, Neutral",\n'
            '  "narrative_type": "one of: Family craft, Traditional heritage, Community-made, Cultural identity, Handmade journey, or null",\n'
            '  "detected_language": "one of: en, hi, bn, mr, as, ta, te"\n'
            "}\n"
            "Return ONLY raw JSON, no markdown formatting or commentary."
        )

    def _call_gemini_extract(self, transcript: str, language: Optional[str]) -> Optional[ProductCatalogNLPOutput]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"
        prompt = f"{self._get_system_prompt()}\n\nArtisan Input: {transcript}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json"}
        }
        with httpx.Client(timeout=10.0) as client:
            resp = client.post(url, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                text_content = data["candidates"][0]["content"]["parts"][0]["text"]
                parsed = json.loads(text_content)
                parsed["raw_transcript"] = transcript
                return ProductCatalogNLPOutput(**parsed)
        return None

    def _call_openai_extract(self, transcript: str, language: Optional[str]) -> Optional[ProductCatalogNLPOutput]:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": f"Artisan Input: {transcript}"}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.2
        }
        with httpx.Client(timeout=10.0) as client:
            resp = client.post(url, headers=headers, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                text_content = data["choices"][0]["message"]["content"]
                parsed = json.loads(text_content)
                parsed["raw_transcript"] = transcript
                return ProductCatalogNLPOutput(**parsed)
        return None


# ==========================================================
# SERVICE FACTORY
# ==========================================================
def get_nlp_service(mock: Optional[bool] = None) -> NLPService:
    """
    Factory function providing singleton/configured NLPService instance.
    Defaults to MOCK_AI=True for robust SIH demo uptime.
    """
    if mock is None:
        # Check environment variable
        mock_env = os.getenv("MOCK_AI", "true").lower() == "true"
        mock = mock_env

    if mock:
        return MockNLPService()
    else:
        return RealNLPService()
