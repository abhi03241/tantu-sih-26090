"""
NLP Service Layer for TANTU Backend
Abstracts Team Member M's Voice-to-Text, Multilingual NLP, and Cultural Storytelling module.
"""
import logging
from typing import Dict, Any, Optional
from backend.app.config import settings
from ai.nlp.voice_and_story import process_voice_transcript, generate_catalogue_nlp

logger = logging.getLogger("tantu.nlp_service")


class NLPService:
    """
    Orchestrates NLP operations: voice transcript analysis, bilingual cataloging,
    sentiment analysis, and cultural storytelling generation.
    """

    @classmethod
    def process_voice(cls, transcript: str, language: str = "hi") -> Dict[str, Any]:
        """
        Converts artisan voice transcript into structured product attributes, bilingual copy,
        and cultural narrative tags.
        """
        try:
            result = process_voice_transcript(
                transcript=transcript,
                language=language,
                mock=settings.MOCK_AI
            )
            return result
        except Exception as e:
            logger.error(f"[NLPService] Error processing voice transcript: {e}. Falling back to mock NLP.")
            return process_voice_transcript(transcript=transcript, language=language, mock=True)

    @classmethod
    def generate_catalogue(cls, product_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates marketing copy, cultural heritage stories, tags, and sentiment scores.
        """
        try:
            result = generate_catalogue_nlp(
                product_info=product_info,
                mock=settings.MOCK_AI
            )
            return result
        except Exception as e:
            logger.error(f"[NLPService] Error generating catalogue: {e}. Falling back to mock NLP.")
            return generate_catalogue_nlp(product_info=product_info, mock=True)
