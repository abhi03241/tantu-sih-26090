"""Standalone pricing endpoints backed by S's transparent demo pricing service."""
from fastapi import APIRouter

from ai.pricing.pricing_service import get_pricing_service, load_demo_market_references
from backend.app.config import settings
from backend.app.schemas import PricingCalculationResponse, PricingRequest


router = APIRouter(prefix="/api/pricing", tags=["Pricing Engine"])


@router.post("/estimate", response_model=PricingCalculationResponse)
def estimate_pricing(request: PricingRequest):
    """Return an AI-assisted suggested range without modifying a product."""
    return get_pricing_service(mock=settings.MOCK_AI).calculate_price(
        category=request.category or request.craft_type or "Handicraft",
        material=request.material or "Natural Material",
        production_time=request.production_time,
        dimensions=request.dimensions,
        raw_material_cost=request.raw_material_cost,
        labor_cost=request.labor_cost,
        labor_hours=request.labor_hours,
        overhead=request.overhead,
        quantity=request.quantity or 1,
        region=request.region,
        craft_type=request.craft_type,
    )


@router.get("/reference-data")
def get_reference_market_data():
    """Return the explicitly labelled demo market reference dataset."""
    return load_demo_market_references()
