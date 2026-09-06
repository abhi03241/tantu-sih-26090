"""
Pricing Service Layer for TANTU Backend
Abstracts Team Member S's Dynamic Fair Wage & B2B Market Pricing Engine.
"""
import logging
from typing import Dict, Any, Optional
from backend.app.config import settings
from ai.pricing.smart_pricing import calculate_smart_price

logger = logging.getLogger("tantu.pricing_service")


class PricingService:
    """
    Orchestrates fair wage and dynamic market pricing algorithms.
    Computes fair artisan price range based on materials, craft effort, and market demand.
    """

    @classmethod
    def calculate_price(
        cls,
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
    ) -> Dict[str, Any]:
        """
        Calculates suggested price bounds (suggested_price_min, suggested_price_max).
        """
        try:
            result = calculate_smart_price(
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
                mock=settings.MOCK_AI
            )
            return result
        except Exception as e:
            logger.error(f"[PricingService] Error computing smart price: {e}. Falling back to mock Pricing.")
            return calculate_smart_price(
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
                mock=True
            )
