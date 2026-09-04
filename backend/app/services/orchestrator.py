"""
Product Pipeline Orchestrator for TANTU Backend
Coordinates multi-stage AI workflow: Voice/Text -> NLP -> Vision -> Pricing -> Cataloging.
Serves as the single end-to-end integration orchestrator for SIH demo.
"""
import uuid
import logging
from typing import Dict, Any, Optional
from backend.app.database import ProductRepository
from backend.app.services.nlp_service import NLPService
from backend.app.services.vision_service import VisionService
from backend.app.services.pricing_service import PricingService

logger = logging.getLogger("tantu.orchestrator")


class ProductPipelineOrchestrator:
    """
    Orchestrates the complete product cataloging pipeline:
    Photo + Voice Input -> NLP Engine -> Vision Enhancer -> Pricing Engine -> Complete Database Record.
    """

    @classmethod
    def process_product_pipeline(
        cls,
        product_id: Optional[str] = None,
        audio_transcript: Optional[str] = None,
        image_url: Optional[str] = None,
        raw_material_cost: Optional[float] = None,
        prompt: Optional[str] = None,
        language: str = "hi",
        artisan_id: str = "art-001"
    ) -> Dict[str, Any]:
        """
        Executes end-to-end AI cataloging pipeline for an existing or newly created product.
        """
        # Step 1: Retrieve existing product or initialize a new product record
        product = None
        if product_id and product_id != "new":
            product = ProductRepository.get_by_id(product_id)

        if not product:
            generated_id = product_id if (product_id and product_id != "new") else f"prod-{uuid.uuid4().hex[:8]}"
            product = {
                "id": generated_id,
                "title": "Artisan Craft Product",
                "description_english": "Handcrafted item cataloged via TANTU AI platform.",
                "description_hindi": "TANTU AI प्लेटफॉर्म द्वारा निर्मित हस्तनिर्मित वस्तु।",
                "category": "Handicrafts & Decor",
                "material": "Natural Fiber",
                "dimensions": "Standard Size",
                "production_time": "2 days",
                "tags": ["handicraft", "artisanal"],
                "story": "Crafted using traditional regional artisan methods.",
                "sentiment": "Positive",
                "narrative_type": "Heritage Artisan Story",
                "image_url": image_url or "https://images.unsplash.com/photo-1590736969955-71cc94801759?w=800",
                "enhanced_image_url": None,
                "suggested_price_min": 500.0,
                "suggested_price_max": 900.0,
                "artisan_id": artisan_id,
                "artisan_name": "Lakshmi Devi",
                "location": "Silchar, Assam"
            }

        if image_url:
            product["image_url"] = image_url

        product["status"] = "processing"
        errors = {}

        # Step 2: Voice & Text NLP Processing
        if audio_transcript:
            try:
                nlp_result = NLPService.process_voice(transcript=audio_transcript, language=language)
                product["title"] = nlp_result.get("title", product["title"])
                product["description_english"] = nlp_result.get("description_english", product["description_english"])
                product["description_hindi"] = nlp_result.get("description_hindi", product["description_hindi"])
                product["category"] = nlp_result.get("category", product["category"])
                product["material"] = nlp_result.get("material", product["material"])
                product["tags"] = nlp_result.get("tags", product.get("tags", []))
                product["story"] = nlp_result.get("story", product.get("story"))
                product["sentiment"] = nlp_result.get("sentiment", product.get("sentiment"))
                product["narrative_type"] = nlp_result.get("narrative_type", product.get("narrative_type"))
            except Exception as e:
                logger.error(f"[Orchestrator] NLP Voice processing failed: {e}")
                errors["nlp"] = str(e)

        # Step 3: Catalog Description Enrichment
        try:
            catalogue_result = NLPService.generate_catalogue(product_info=product)
            product["description_english"] = catalogue_result.get("description_english", product["description_english"])
            product["description_hindi"] = catalogue_result.get("description_hindi", product["description_hindi"])
            if catalogue_result.get("tags"):
                existing_tags = set(product.get("tags", []))
                existing_tags.update(catalogue_result["tags"])
                product["tags"] = list(existing_tags)
        except Exception as e:
            logger.error(f"[Orchestrator] NLP Catalogue generation failed: {e}")
            errors["catalogue"] = str(e)

        # Step 4: Vision Image Enhancement
        try:
            img_target = product.get("image_url")
            vision_result = VisionService.enhance_image(image_url=img_target, prompt=prompt)
            product["enhanced_image_url"] = vision_result.get("enhanced_image_url") or product.get("image_url")
        except Exception as e:
            logger.error(f"[Orchestrator] Vision image enhancement failed: {e}")
            errors["vision"] = str(e)

        # Step 5: Pricing Calculation Engine
        try:
            pricing_result = PricingService.calculate_price(
                category=product.get("category", "Handicraft"),
                material=product.get("material", "Natural Material"),
                production_time=product.get("production_time"),
                dimensions=product.get("dimensions"),
                raw_material_cost=raw_material_cost
            )
            product["suggested_price_min"] = pricing_result.get("suggested_price_min", product.get("suggested_price_min"))
            product["suggested_price_max"] = pricing_result.get("suggested_price_max", product.get("suggested_price_max"))
        except Exception as e:
            logger.error(f"[Orchestrator] Pricing calculation failed: {e}")
            errors["pricing"] = str(e)

        # Determine final status
        if errors.get("nlp") and not product.get("title"):
            product["status"] = "failed"
        else:
            product["status"] = "ready"

        # Step 6: Database Persistence
        saved_product = ProductRepository.save(product)
        logger.info(f"[Orchestrator] Completed cataloging pipeline for ID '{saved_product['id']}' with status '{saved_product['status']}'")

        return {
            "id": saved_product["id"],
            "status": saved_product["status"],
            "product": saved_product,
            "errors": errors if errors else None
        }

