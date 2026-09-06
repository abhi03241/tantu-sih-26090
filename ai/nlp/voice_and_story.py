"""
NLP & Voice Processing Module
Maintained by Team Member M (AI/NLP/Voice/Sentiment)
Integrated into TANTU Backend core workflow.

Converts rural artisan voice input into structured bilingual product catalog JSON,
cultural storytelling narrative, and sentiment categorization.
"""
from typing import Dict, Any, Optional
from ai.nlp.service import get_nlp_service, NLPService
from ai.nlp.schemas import ProductCatalogNLPOutput


def process_voice_transcript(transcript: str, language: str = "hi", mock: bool = True) -> Dict[str, Any]:
    """
    Converts audio transcript/voice input from rural artisans into structured catalogue data.
    Analyzes sentiment, extracts key attributes, and generates English + Hindi descriptions.

    Maintains 100% backward compatibility with backend/app/routers/ai_endpoints.py.
    """
    service: NLPService = get_nlp_service(mock=mock)
    result: ProductCatalogNLPOutput = service.process_transcript(transcript=transcript, language=language)
    return result.to_product_dict()


def process_voice_audio(audio_bytes: bytes, language: str = "hi", mock: bool = True) -> Dict[str, Any]:
    """
    Full voice-to-catalogue pipeline: Speech-to-Text -> NLP Extraction -> Structured Product JSON.
    """
    service: NLPService = get_nlp_service(mock=mock)
    result: ProductCatalogNLPOutput = service.process_voice(audio_bytes=audio_bytes, language=language)
    return result.to_product_dict()


def generate_catalogue_nlp(product_info: Dict[str, Any], mock: bool = True) -> Dict[str, Any]:
    """
    Generates rich marketing description, cultural story narrative, tags, and sentiment.
    Integrated with Team Member M's NLP module.
    """
    service: NLPService = get_nlp_service(mock=mock)
    return service.generate_catalogue(product_info)
