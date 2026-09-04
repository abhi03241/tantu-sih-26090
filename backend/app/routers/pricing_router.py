"""
Pricing Router
Maintained by Team Member S (Pricing + B2B Marketplace)
Provides dedicated API endpoints for on-the-fly pricing estimations,
cost-plus breakdowns, and demo reference market dataset access.
"""

from fastapi import APIRouter
from backend.app.schemas import PricingRequest, PricingCalculationResponse
from backend.app.config import settings
from ai.pricing.pricing_service import get_pricing_service, load_demo_market_references

router = APIRouter(prefix="/api/pricing", tags=["Pricing Engine (Member S)"])


@router.post("/estimate", response_model=PricingCalculationResponse)
def estimate_pricing(request: PricingRequest):
    """
    POST /api/pricing/estimate
    Calculates dynamic fair wage price range with transparent breakdown for an artisan product.
    Accepts raw material costs, labor hours/cost, overhead, bulk quantity, and craft category.
    """
    service = get_pricing_service(mock=settings.MOCK_AI)
    result = service.calculate_price(
        category=request.category or "Handicraft",
        material=request.material or "Natural Material",
        production_time=request.production_time,
        dimensions=request.dimensions,
        raw_material_cost=request.raw_material_cost,
        labor_cost=request.labor_cost,
        labor_hours=request.labor_hours,
        overhead=request.overhead,
        quantity=request.quantity or 1,
        region=request.region,
        craft_type=request.craft_type
    )
    return result


@router.get("/reference-data")
def get_reference_market_data():
    """
    GET /api/pricing/reference-data
    Returns curated demo market reference price benchmarks for:
    - Bamboo Basket
    - Pottery & Ceramics
    - Handwoven Textiles
    - Wooden Handicraft
    Clearly labeled as 'Demo market reference' for transparent SIH evaluation.
    """
    return load_demo_market_references()
