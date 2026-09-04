"""
Pydantic Schemas for AI/NLP Module - TANTU (SIH PS 26090)
Maintained by Team Member M (AI/NLP/Voice/Sentiment)
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class ProductCatalogNLPOutput(BaseModel):
    """
    Structured product catalog output contract generated from artisan voice/text.
    Compatible with the shared TANTU Product contract (ProductBase in backend/app/schemas.py).
    """
    title: str = Field(..., description="Professional, concise product title")
    description_english: str = Field(..., description="Rich English marketing & functional product description")
    description_hindi: str = Field(..., description="Natural Hindi product description for regional buyers/artisans")
    category: str = Field(..., description="Standard craft category, e.g. Bamboo & Cane Craft, Textiles & Handloom, Woodcraft")
    material: str = Field(..., description="Primary craft material, e.g. Bamboo, Chanderi Silk, Teak Wood")
    dimensions: Optional[str] = Field(None, description="Dimensions of the craft if mentioned, otherwise null")
    production_time: Optional[str] = Field(None, description="Estimated production/crafting duration, e.g. '2 days', '5 days'")
    tags: List[str] = Field(default_factory=list, description="Search & discoverability tags in lowercase")
    story: Optional[str] = Field(None, description="Personal or generational narrative behind the handcrafted piece")
    sentiment: Optional[str] = Field(
        None,
        description="Sentiment classification: positive, neutral, heritage, family tradition, craftsmanship pride, cultural significance"
    )
    narrative_type: Optional[str] = Field(
        None,
        description="Narrative type: family_tradition, cultural_heritage, craftsmanship_pride, community_empowerment, standard_narrative"
    )

    # Contextual metadata (non-breaking helpers)
    detected_language: Optional[str] = Field("hi", description="Detected language code (hi, en, etc.)")
    raw_transcript: Optional[str] = Field(None, description="Original artisan input or transcription")

    def to_product_dict(self) -> dict:
        """Export as dictionary matching backend product update fields."""
        return {
            "title": self.title,
            "description_english": self.description_english,
            "description_hindi": self.description_hindi,
            "category": self.category,
            "material": self.material,
            "dimensions": self.dimensions,
            "production_time": self.production_time,
            "tags": self.tags,
            "story": self.story,
            "sentiment": self.sentiment,
            "narrative_type": self.narrative_type,
            "detected_language": self.detected_language,
            "raw_transcript": self.raw_transcript,
        }


class VoiceTranscriptionResult(BaseModel):
    """Result from voice speech-to-text stage."""
    transcript: str
    detected_language: str = "hi"
    confidence: float = 0.95
    duration_seconds: Optional[float] = None


class VoiceInputRequest(BaseModel):
    """Flexible voice payload: accepts raw text transcript or audio base64."""
    audio_transcript: Optional[str] = Field(None, description="Pre-transcribed text in Hindi/English/Hinglish")
    audio_base64: Optional[str] = Field(None, description="Base64-encoded audio bytes for STT")
    language: Optional[str] = Field("hi", description="Artisan preferred or spoken language code")


class CatalogueGenerationRequest(BaseModel):
    """Input payload for generating or enhancing catalogue storytelling."""
    product_id: Optional[str] = None
    title: Optional[str] = None
    category: Optional[str] = None
    material: Optional[str] = None
    raw_notes: Optional[str] = None
    language: Optional[str] = "hi"
