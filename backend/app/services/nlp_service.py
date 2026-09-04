"""
Backend NLP Service Integration Layer
Maintained by Team Member M (AI/NLP/Voice/Sentiment) for TANTU (SIH PS 26090)

Exposes clean service abstraction bridging Backend and AI submodules.
Conforms strictly to Common Product Contract in backend/app/schemas.py.
"""
from typing import Dict, Any, Optional
from ai.nlp.service import NLPService, MockNLPService, RealNLPService, get_nlp_service
from ai.nlp.schemas import ProductCatalogNLPOutput


class BackendNLPService:
    """
    Service layer bridging FastAPI backend routes to the AI/NLP pipeline.
    Ensures safe execution, deterministic mock mode, and schema conformity.
    """

    def __init__(self, mock: Optional[bool] = None):
        self._service: NLPService = get_nlp_service(mock=mock)

    def process_artisan_input(
        self,
        text_or_transcript: str,
        language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Processes natural language text from rural artisans into structured catalogue data.
        """
        output: ProductCatalogNLPOutput = self._service.process_transcript(
            transcript=text_or_transcript,
            language=language
        )
        return output.to_product_dict()

    def process_audio(
        self,
        audio_bytes: bytes,
        language: Optional[str] = "hi"
    ) -> Dict[str, Any]:
        """
        Transcribes voice audio and returns structured product catalogue data.
        """
        output: ProductCatalogNLPOutput = self._service.process_voice(
            audio_bytes=audio_bytes,
            language=language
        )
        return output.to_product_dict()

    def generate_catalogue(self, product_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enriches marketing storytelling descriptions and tags for an existing product.
        """
        return self._service.generate_catalogue(product_info)


# Singleton instance helper
nlp_service = BackendNLPService()
