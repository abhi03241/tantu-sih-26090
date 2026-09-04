"""
AI NLP Module - Voice Processing & Catalogue Generation
Maintained by Team Member M (AI/NLP/Voice/Sentiment) for TANTU (SIH PS 26090)
"""
from ai.nlp.schemas import (
    ProductCatalogNLPOutput,
    VoiceTranscriptionResult,
    VoiceInputRequest,
    CatalogueGenerationRequest,
)
from ai.nlp.service import (
    NLPService,
    MockNLPService,
    RealNLPService,
    get_nlp_service,
)
from ai.nlp.voice_and_story import (
    process_voice_transcript,
    process_voice_audio,
    generate_catalogue_nlp,
)

__all__ = [
    "ProductCatalogNLPOutput",
    "VoiceTranscriptionResult",
    "VoiceInputRequest",
    "CatalogueGenerationRequest",
    "NLPService",
    "MockNLPService",
    "RealNLPService",
    "get_nlp_service",
    "process_voice_transcript",
    "process_voice_audio",
    "generate_catalogue_nlp",
]
