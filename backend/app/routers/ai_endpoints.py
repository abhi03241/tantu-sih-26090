from fastapi import APIRouter, HTTPException, status
from backend.app.schemas import (
    ProductResponse,
    VoiceProcessingRequest,
    EnhanceImageRequest,
    GenerateCatalogueRequest,
    PricingRequest
)
from backend.app.database import ProductRepository
from backend.app.config import settings
from ai.nlp.voice_and_story import process_voice_transcript, generate_catalogue_nlp
from ai.vision.image_enhancer import enhance_artisan_image
from ai.pricing.smart_pricing import calculate_smart_price

router = APIRouter(prefix="/api/products", tags=["AI Endpoints (M, R, S Integration)"])


@router.post("/{id}/voice", response_model=ProductResponse)
def process_voice_and_update_product(id: str, request: VoiceProcessingRequest):
    """
    POST /api/products/{id}/voice
    Processes artisan voice audio transcript into bilingual descriptions, tags, sentiment, and story.
    Updates the product record in the database.
    Integrated with Team Member M's NLP module.
    """
    product = ProductRepository.get_by_id(id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID '{id}' not found"
        )

    ai_result = process_voice_transcript(
        transcript=request.audio_transcript,
        language=request.language or "hi",
        mock=settings.MOCK_AI
    )

    # Merge AI voice extraction result into product model
    product["title"] = ai_result.get("title", product["title"])
    product["description_english"] = ai_result.get("description_english", product["description_english"])
    product["description_hindi"] = ai_result.get("description_hindi", product["description_hindi"])
    product["category"] = ai_result.get("category", product["category"])
    product["material"] = ai_result.get("material", product["material"])
    # Optional specifications are only updated when the new transcript states them.
    # This preserves known product data and never writes fabricated null/default values.
    if ai_result.get("dimensions") is not None:
        product["dimensions"] = ai_result["dimensions"]
    if ai_result.get("production_time") is not None:
        product["production_time"] = ai_result["production_time"]
    product["tags"] = ai_result.get("tags", product.get("tags", []))
    if ai_result.get("story") is not None:
        product["story"] = ai_result["story"]
    if ai_result.get("sentiment") is not None:
        product["sentiment"] = ai_result["sentiment"]
    if ai_result.get("narrative_type") is not None:
        product["narrative_type"] = ai_result["narrative_type"]

    updated = ProductRepository.save(product)
    return updated


@router.post("/{id}/enhance-image", response_model=ProductResponse)
def enhance_product_image(id: str, request: EnhanceImageRequest = None):
    """
    POST /api/products/{id}/enhance-image
    Enhances artisan raw photo by removing background noise and applying studio lighting.
    Updates `enhanced_image_url` on product.
    Integrated with Team Member R's Vision module.
    """
    product = ProductRepository.get_by_id(id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID '{id}' not found"
        )

    img_to_enhance = (request and request.image_url) or product.get("image_url")
    prompt = request.prompt if request else None

    ai_result = enhance_artisan_image(
        image_url=img_to_enhance,
        prompt=prompt,
        mock=settings.MOCK_AI
    )

    product["enhanced_image_url"] = ai_result.get("enhanced_image_url")
    updated = ProductRepository.save(product)
    return updated


@router.post("/{id}/generate-catalogue", response_model=ProductResponse)
def generate_product_catalogue(id: str, request: GenerateCatalogueRequest = None):
    """
    POST /api/products/{id}/generate-catalogue
    Generates rich marketing description, cultural story, and tags for smart cataloging.
    Integrated with Team Member M's NLP module.
    """
    product = ProductRepository.get_by_id(id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID '{id}' not found"
        )

    catalogue_source = product.copy()
    if request and request.raw_notes:
        catalogue_source["raw_notes"] = request.raw_notes

    ai_result = generate_catalogue_nlp(
        product_info=catalogue_source,
        mock=settings.MOCK_AI
    )

    product["description_english"] = ai_result.get("description_english", product["description_english"])
    product["description_hindi"] = ai_result.get("description_hindi", product["description_hindi"])
    product["tags"] = ai_result.get("tags", product.get("tags", []))
    if ai_result.get("story") is not None:
        product["story"] = ai_result["story"]
    if ai_result.get("sentiment") is not None:
        product["sentiment"] = ai_result["sentiment"]
    if ai_result.get("narrative_type") is not None:
        product["narrative_type"] = ai_result["narrative_type"]

    updated = ProductRepository.save(product)
    return updated


@router.post("/{id}/price", response_model=ProductResponse)
def calculate_product_price(id: str, request: PricingRequest = None):
    """
    POST /api/products/{id}/price
    Calculates fair market value price bounds (`suggested_price_min`, `suggested_price_max`).
    Integrated with Team Member S's Pricing module.
    """
    product = ProductRepository.get_by_id(id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID '{id}' not found"
        )

    raw_cost = request.raw_material_cost if request else None

    ai_result = calculate_smart_price(
        category=product.get("category", "Handicraft"),
        material=product.get("material", "Natural Material"),
        production_time=product.get("production_time"),
        dimensions=product.get("dimensions"),
        raw_material_cost=raw_cost,
        mock=settings.MOCK_AI
    )

    product["suggested_price_min"] = ai_result.get("suggested_price_min")
    product["suggested_price_max"] = ai_result.get("suggested_price_max")

    updated = ProductRepository.save(product)
    return updated
