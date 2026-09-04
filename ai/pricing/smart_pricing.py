"""
Smart Pricing Module
Maintained by Team Member S (Pricing + B2B Marketplace)
Integrated into TANTU Backend core workflow.
"""
from typing import Dict, Any, Optional
from .pricing_service import (
    PricingService,
    MockPricingService,
    RealPricingService,
    get_pricing_service,
    load_demo_market_references
)


def calculate_smart_price(
    category: str,
    material: str,
    production_time: Optional[str] = None,
    dimensions: Optional[str] = None,
    raw_material_cost: Optional[float] = None,
    labor_cost: Optional[float] = None,
    labor_hours: Optional[int] = None,
    overhead: Optional[float] = None,
    quantity: Optional[int] = 1,
    region: Optional[str] = None,
    craft_type: Optional[str] = None,
    mock: bool = True,
    **kwargs: Any
) -> Dict[str, Any]:
    """
    Computes fair artisan price bounds considering material costs, craft complexity, labor duration,
    overhead, bulk quantity, and demo market reference data.

    Preserves 100% backward compatibility with existing backend routers and tests.
    """
    service = get_pricing_service(mock=mock)
    return service.calculate_price(
        category=category,
        material=material,
        production_time=production_time,
        dimensions=dimensions,
        raw_material_cost=raw_material_cost,
        labor_cost=labor_cost,
        labor_hours=labor_hours,
        overhead=overhead,
        quantity=quantity,
        region=region,
        craft_type=craft_type,
        **kwargs
    )
