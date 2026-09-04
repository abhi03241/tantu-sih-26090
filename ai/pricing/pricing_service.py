"""
Pricing Service Interface & Implementations
Maintained by Team Member S (Pricing + B2B Marketplace)
Part of TANTU (SIH 26090)
"""

import json
import os
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Tuple


def load_demo_market_references() -> Dict[str, Any]:
    """
    Loads curated demo reference prices from data/demo_market_prices.json.
    Clearly labeled as 'Demo market reference' for prototype transparency.
    """
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "..", "..", "data", "demo_market_prices.json"),
        os.path.join(os.getcwd(), "data", "demo_market_prices.json"),
    ]
    for path in possible_paths:
        abs_path = os.path.abspath(path)
        if os.path.exists(abs_path):
            try:
                with open(abs_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass

    # In-memory fallback if file is missing
    return {
      "dataset_label": "Demo market reference",
      "currency": "INR",
      "categories": {
        "Bamboo & Cane Craft": {
          "benchmark_raw_cost_range": [200.0, 350.0],
          "benchmark_labor_hours": 16,
          "fair_wage_rate_per_hour": 70.0,
          "overhead_rate": 0.12,
          "margin_range_pct": [0.20, 0.45],
          "demo_reference_price_min": 650.0,
          "demo_reference_price_max": 950.0,
        },
        "Pottery & Ceramics": {
          "benchmark_raw_cost_range": [250.0, 450.0],
          "benchmark_labor_hours": 20,
          "fair_wage_rate_per_hour": 75.0,
          "overhead_rate": 0.15,
          "margin_range_pct": [0.22, 0.48],
          "demo_reference_price_min": 750.0,
          "demo_reference_price_max": 1400.0,
        },
        "Textiles & Handloom": {
          "benchmark_raw_cost_range": [600.0, 1100.0],
          "benchmark_labor_hours": 32,
          "fair_wage_rate_per_hour": 90.0,
          "overhead_rate": 0.15,
          "margin_range_pct": [0.25, 0.50],
          "demo_reference_price_min": 1800.0,
          "demo_reference_price_max": 2500.0,
        },
        "Woodcraft": {
          "benchmark_raw_cost_range": [350.0, 650.0],
          "benchmark_labor_hours": 24,
          "fair_wage_rate_per_hour": 85.0,
          "overhead_rate": 0.14,
          "margin_range_pct": [0.20, 0.45],
          "demo_reference_price_min": 1100.0,
          "demo_reference_price_max": 1700.0,
        }
      }
    }


class PricingService(ABC):
    """
    Abstract Base Class for TANTU Fair Wage & Dynamic Pricing Engine.
    """

    @abstractmethod
    def calculate_price(
        self,
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
        **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Calculates suggested minimum and maximum pricing bounds along with
        transparent cost breakdown and confidence indicator.
        """
        pass


class MockPricingService(PricingService):
    """
    Transparent Cost-Plus Prototype Pricing Service.
    Uses:
        estimated_cost = raw_material_cost + labor_cost + overhead
    Then applies fair artisan margin and demo market reference adjustments.
    Clearly labels benchmarks as 'Demo market reference'.
    """

    def __init__(self):
        self.market_data = load_demo_market_references()

    def _resolve_category_benchmark(self, category: str) -> Tuple[str, Dict[str, Any]]:
        categories = self.market_data.get("categories", {})
        cat_lower = category.lower().strip()

        # Direct match or partial keyword matching
        for cat_name, data in categories.items():
            if cat_name.lower() in cat_lower or cat_lower in cat_name.lower():
                return cat_name, data
            # Check keywords
            if "bamboo" in cat_lower or "cane" in cat_lower or "basket" in cat_lower:
                if "Bamboo" in cat_name:
                    return cat_name, data
            if "pottery" in cat_lower or "ceramic" in cat_lower or "terracotta" in cat_lower or "clay" in cat_lower:
                if "Pottery" in cat_name:
                    return cat_name, data
            if "textile" in cat_lower or "handloom" in cat_lower or "dupatta" in cat_lower or "silk" in cat_lower or "saree" in cat_lower:
                if "Textile" in cat_name:
                    return cat_name, data
            if "wood" in cat_lower or "carv" in cat_lower or "elephant" in cat_lower or "timber" in cat_lower:
                if "Wood" in cat_name:
                    return cat_name, data

        # Generic craft benchmark
        return "General Handicraft", {
            "benchmark_raw_cost_range": [300.0, 500.0],
            "benchmark_labor_hours": 18,
            "fair_wage_rate_per_hour": 75.0,
            "overhead_rate": 0.12,
            "margin_range_pct": [0.20, 0.45],
            "demo_reference_price_min": 700.0,
            "demo_reference_price_max": 1300.0,
        }

    def _parse_hours_from_production_time(self, production_time: Optional[str]) -> Optional[int]:
        if not production_time:
            return None
        pt = production_time.lower()
        import re
        nums = re.findall(r"\d+", pt)
        val = int(nums[0]) if nums else None

        if "hour" in pt or "hr" in pt:
            return val or 8
        elif "day" in pt:
            days = val or 3
            return days * 8  # 8 hours/day artisan labor
        elif "week" in pt:
            weeks = val or 1
            return weeks * 48
        return None

    def calculate_price(
        self,
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
        **kwargs: Any
    ) -> Dict[str, Any]:
        matched_category_name, benchmark = self._resolve_category_benchmark(category or craft_type or "Handicraft")

        # 1. Resolve Raw Material Cost
        if raw_material_cost is not None and raw_material_cost > 0:
            resolved_raw_cost = float(raw_material_cost)
            raw_cost_source = "artisan_input"
        else:
            # Fallback to category benchmark median
            min_bench, max_bench = benchmark.get("benchmark_raw_cost_range", [250.0, 400.0])
            resolved_raw_cost = round((min_bench + max_bench) / 2.0, 2)
            raw_cost_source = "demo_market_benchmark"

        # 2. Resolve Labor Hours & Labor Cost
        resolved_hours = labor_hours
        if resolved_hours is None or resolved_hours <= 0:
            parsed_hours = self._parse_hours_from_production_time(production_time)
            resolved_hours = parsed_hours if parsed_hours else benchmark.get("benchmark_labor_hours", 16)

        fair_wage_rate = benchmark.get("fair_wage_rate_per_hour", 75.0)

        if labor_cost is not None and labor_cost > 0:
            resolved_labor_cost = float(labor_cost)
            labor_cost_source = "artisan_input"
        else:
            resolved_labor_cost = round(resolved_hours * fair_wage_rate, 2)
            labor_cost_source = "fair_wage_hourly_calculation"

        # 3. Resolve Overhead (studio, packaging, tool wear)
        overhead_rate = benchmark.get("overhead_rate", 0.12)
        if overhead is not None and overhead >= 0:
            resolved_overhead = float(overhead)
            overhead_source = "artisan_input"
        else:
            resolved_overhead = round((resolved_raw_cost + resolved_labor_cost) * overhead_rate, 2)
            overhead_source = f"{int(overhead_rate * 100)}%_of_prime_cost"

        # 4. Transparent formula: estimated_cost = raw_material_cost + labor_cost + overhead
        estimated_cost = round(resolved_raw_cost + resolved_labor_cost + resolved_overhead, 2)

        # 5. Margin application
        margin_range = benchmark.get("margin_range_pct", [0.20, 0.45])
        margin_min = margin_range[0]
        margin_max = margin_range[1]

        # Bulk quantity adjustment if buyer asks for bulk order (e.g. quantity >= 50)
        q = quantity if (quantity and quantity > 0) else 1
        bulk_discount_applied = False
        bulk_discount_pct = 0.0

        if q >= 50:
            bulk_discount_pct = 0.12
            bulk_discount_applied = True
            # Economies of scale reduce unit overhead and margin slightly while protecting artisan fair wage
            margin_min = max(0.15, margin_min - 0.05)
            margin_max = max(0.25, margin_max - 0.10)
        elif q >= 25:
            bulk_discount_pct = 0.08
            bulk_discount_applied = True
            margin_min = max(0.18, margin_min - 0.03)
            margin_max = max(0.32, margin_max - 0.06)

        # Cost-plus calculations
        suggested_min = round(estimated_cost * (1.0 + margin_min), 2)
        suggested_max = round(estimated_cost * (1.0 + margin_max), 2)

        # Cross-check against demo market reference bounds
        ref_min = benchmark.get("demo_reference_price_min", suggested_min)
        ref_max = benchmark.get("demo_reference_price_max", suggested_max)

        # Blend with demo market reference range (80% cost-plus, 20% reference)
        final_min = round(0.80 * suggested_min + 0.20 * ref_min, 2)
        final_max = round(0.80 * suggested_max + 0.20 * ref_max, 2)

        # Guarantee minimum doesn't exceed maximum and minimum > estimated cost
        if final_min >= final_max:
            final_max = round(final_min * 1.25, 2)
        final_min = max(final_min, round(estimated_cost * 1.10, 2))

        # Build clean, artisan-friendly response
        # Using mandated wording: "AI-assisted suggested price range"
        # Factors: material, production time, handmade nature, product category
        prod_time_display = production_time or f"{resolved_hours} hours"
        mat_display = material or "Artisan Grade Natural Material"
        reason = (
            f"AI-assisted suggested price range based on material ({mat_display}), "
            f"production time ({prod_time_display}), "
            f"handmade nature (authentic rural artisan craft), "
            f"and {matched_category_name} demo market references."
        )

        return {
            "suggested_price_min": float(int(final_min)),
            "suggested_price_max": float(int(final_max)),
            "currency": "INR",
            "confidence": "demo",
            "pricing_label": "AI-assisted suggested price range",
            "reason": reason,
            "pricing_factors": {
                "pricing_label": "AI-assisted suggested price range",
                "category": matched_category_name,
                "material": mat_display,
                "material_grade": mat_display,
                "production_time": prod_time_display,
                "handmade_nature": "100% Authentic Handcrafted Heritage Work",
                "estimated_labor_hours": f"{resolved_hours} hrs",
                "fair_wage_rate": f"₹{fair_wage_rate}/hr",
                "fair_trade_margin": f"{int(margin_min * 100)}% - {int(margin_max * 100)}%",
                "bulk_quantity": q,
                "bulk_discount_applied": bulk_discount_applied,
                "market_reference": "Demo market reference"
            },
            "breakdown": {
                "raw_material_cost": resolved_raw_cost,
                "raw_material_cost_source": raw_cost_source,
                "labor_cost": resolved_labor_cost,
                "labor_cost_source": labor_cost_source,
                "overhead": resolved_overhead,
                "overhead_source": overhead_source,
                "estimated_cost": estimated_cost,
                "margin_min_pct": int(margin_min * 100),
                "margin_max_pct": int(margin_max * 100),
                "demo_market_reference": "Demo market reference",
                "demo_reference_bounds": [ref_min, ref_max]
            },
            "recommendation": (
                f"AI-assisted suggested price range is ₹{int(final_min)} - ₹{int(final_max)} INR. "
                f"This reflects the piece's handmade nature, estimated {prod_time_display} craft duration, "
                f"and fair artisan wage (₹{fair_wage_rate}/hr) under demo market reference guidelines."
            )
        }


class RealPricingService(PricingService):
    """
    Production-ready Pricing Service.
    Wraps external ML/LLM services with a strict fallback to MockPricingService.
    Ensures: Never let an external API failure break the application.
    """

    def __init__(self):
        self.fallback_service = MockPricingService()

    def calculate_price(
        self,
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
        **kwargs: Any
    ) -> Dict[str, Any]:
        try:
            # Here real ML model inference or external LLM API would be invoked.
            # In prototype environment or if external service times out/fails:
            return self.fallback_service.calculate_price(
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
        except Exception:
            # Absolute defensive fallback
            return self.fallback_service.calculate_price(
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


def get_pricing_service(mock: bool = True) -> PricingService:
    """
    Factory function providing the appropriate PricingService instance based on MOCK_AI toggle.
    """
    if mock:
        return MockPricingService()
    return RealPricingService()
