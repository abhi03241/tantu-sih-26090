from fastapi import APIRouter, HTTPException, status
from backend.app.schemas import (
    ProductResponse,
    VoiceProcessingRequest,
    EnhanceImageRequest,
    GenerateCatalogueRequest,
    PricingRequest,
    ProcessProductRequest,
    ProcessProductResponse
)
from backend.app.database import ProductRepository
from backend.app.services.nlp_service import NLPService
from backend.app.services.vision_service import VisionService
from backend.app.services.pricing_service import PricingService
from backend.app.services.orchestrator import ProductPipelineOrchestrator

router = APIRouter(prefix="/api/products", tags=["AI Integration Layer (Orchestration & Services)"])


@router.post("/{id}/process", response_model=ProcessProductResponse)
def process_full_product_pipeline(id: str, request: ProcessProductRequest = None):
    """
    POST /api/products/{id}/process
    Complete Orchestrated AI Pipeline:
    Photo + Voice -> NLP Service -> Vision Enhancer -> Pricing Engine -> Complete Product Record.
    Designed for seamless SIH demo execution.
    """
    if id != "new" and not ProductRepository.get_by_id(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID '{id}' not found"
        )

    req = request or ProcessProductRequest()
    result = ProductPipelineOrchestrator.process_product_pipeline(
        product_id=id,
        audio_transcript=req.audio_transcript,
        image_url=req.image_url,
        raw_material_cost=req.raw_material_cost,
        prompt=req.prompt,
        language=req.language or "hi",
        artisan_id=req.artisan_id or "art-001"
    )
    return result



@router.post("/{id}/voice", response_model=ProductResponse)
def process_voice_and_update_product(id: str, request: VoiceProcessingRequest):
    """
    POST /api/products/{id}/voice
    Processes artisan voice audio transcript into bilingual descriptions, tags, sentiment, and story.
    Updates the product record in the database via NLPService.
    """
    is_ephemeral_draft = False
    product = ProductRepository.get_by_id(id)
    if not product:
        if id in ("new-draft", "draft", "new") or id.startswith("new-"):
            is_ephemeral_draft = True
            product = {
                "id": id,
                "title": "Handcrafted Artisan Craft",
                "description_english": "Handcrafted regional artisan craft.",
                "description_hindi": "कारीगर द्वारा निर्मित पारंपरिक हस्तशिल्प।",
                "category": "Handicrafts & Decor",
                "material": "Natural Artisan Material",
                "image_url": "https://images.unsplash.com/photo-1590736969955-71cc94801759",
                "status": "processing",
                "tags": []
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID '{id}' not found"
            )

    ai_result = NLPService.process_voice(
        transcript=request.audio_transcript,
        language=request.language or "hi"
    )

    product["title"] = ai_result.get("title", product["title"])
    product["description_english"] = ai_result.get("description_english", product["description_english"])
    product["description_hindi"] = ai_result.get("description_hindi", product["description_hindi"])
    product["category"] = ai_result.get("category", product["category"])
    product["material"] = ai_result.get("material", product["material"])
    if ai_result.get("dimensions") is not None:
        product["dimensions"] = ai_result["dimensions"]
    if ai_result.get("production_time") is not None:
        product["production_time"] = ai_result["production_time"]
    product["tags"] = ai_result.get("tags", product.get("tags", []))
    product["story"] = ai_result.get("story", product.get("story"))
    product["sentiment"] = ai_result.get("sentiment", product.get("sentiment"))
    product["narrative_type"] = ai_result.get("narrative_type", product.get("narrative_type"))

    if not is_ephemeral_draft:
        updated = ProductRepository.save(product)
    else:
        updated = product
    return updated


@router.post("/{id}/enhance-image", response_model=ProductResponse)
def enhance_product_image(id: str, request: EnhanceImageRequest = None):
    """
    POST /api/products/{id}/enhance-image
    Enhances artisan raw photo by removing background clutter and applying studio lighting via VisionService.
    """
    product = ProductRepository.get_by_id(id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID '{id}' not found"
        )

    img_to_enhance = (request and request.image_url) or product.get("image_url")
    prompt = request.prompt if request else None

    ai_result = VisionService.enhance_image(
        image_url=img_to_enhance,
        prompt=prompt
    )

    product["enhanced_image_url"] = ai_result.get("enhanced_image_url") or img_to_enhance
    updated = ProductRepository.save(product)
    return updated


@router.post("/{id}/generate-catalogue", response_model=ProductResponse)
def generate_product_catalogue(id: str, request: GenerateCatalogueRequest = None):
    """
    POST /api/products/{id}/generate-catalogue
    Generates rich marketing description, cultural story, and tags for smart cataloging via NLPService.
    """
    is_ephemeral_draft = False
    product = ProductRepository.get_by_id(id)
    if not product:
        if id in ("new-draft", "draft", "new") or id.startswith("new-"):
            is_ephemeral_draft = True
            product = {
                "id": id,
                "title": "Handcrafted Artisan Craft",
                "description_english": "Handcrafted regional artisan craft.",
                "description_hindi": "कारीगर द्वारा निर्मित पारंपरिक हस्तशिल्प।",
                "category": "Handicrafts & Decor",
                "material": "Natural Artisan Material",
                "image_url": "https://images.unsplash.com/photo-1590736969955-71cc94801759",
                "status": "ready",
                "tags": []
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID '{id}' not found"
            )

    catalogue_source = product.copy()
    if request and request.raw_notes:
        catalogue_source["raw_notes"] = request.raw_notes
    ai_result = NLPService.generate_catalogue(product_info=catalogue_source)

    product["description_english"] = ai_result.get("description_english", product["description_english"])
    product["description_hindi"] = ai_result.get("description_hindi", product["description_hindi"])
    product["tags"] = ai_result.get("tags", product.get("tags", []))
    product["story"] = ai_result.get("story", product.get("story"))
    product["sentiment"] = ai_result.get("sentiment", product.get("sentiment"))
    product["narrative_type"] = ai_result.get("narrative_type", product.get("narrative_type"))

    if not is_ephemeral_draft:
        updated = ProductRepository.save(product)
    else:
        updated = product
    return updated


@router.post("/{id}/price", response_model=ProductResponse)
def calculate_product_price(id: str, request: PricingRequest = None):
    """
    POST /api/products/{id}/price
    Calculates fair market value price bounds (`suggested_price_min`, `suggested_price_max`) via PricingService.
    """
    product = ProductRepository.get_by_id(id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID '{id}' not found"
        )

    raw_cost = request.raw_material_cost if request else None

    ai_result = PricingService.calculate_price(
        category=(request.category if request and request.category else product.get("category", "Handicraft")),
        material=(request.material if request and request.material else product.get("material", "Natural Material")),
        production_time=(request.production_time if request and request.production_time else product.get("production_time")),
        dimensions=(request.dimensions if request and request.dimensions else product.get("dimensions")),
        raw_material_cost=raw_cost,
        labor_cost=request.labor_cost if request else None,
        labor_hours=request.labor_hours if request else None,
        overhead=request.overhead if request else None,
        quantity=request.quantity if request else 1,
        region=(request.region if request and request.region else product.get("location")),
    )

    product["suggested_price_min"] = ai_result.get("suggested_price_min")
    product["suggested_price_max"] = ai_result.get("suggested_price_max")

    updated = ProductRepository.save(product)
    return updated
