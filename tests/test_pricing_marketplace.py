"""
Unit & Integration Tests for TANTU Dynamic Pricing & B2B Marketplace Module
Maintained by Team Member S (Pricing + B2B Marketplace)
SIH Problem Statement 26090
"""

import sys
import os
import unittest
from fastapi.testclient import TestClient

# Add project root to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.main import app
from backend.app.database import init_db
from backend.app.seed_data import seed_demo_data
from ai.pricing.pricing_service import (
    MockPricingService,
    RealPricingService,
    load_demo_market_references
)
from ai.pricing.smart_pricing import calculate_smart_price


class TestPricingAndMarketplace(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        seed_demo_data()
        cls.client = TestClient(app)

    # ==========================================
    # 1. PRICING TESTS
    # ==========================================
    def test_01_pricing_calculation_full_inputs(self):
        """Test pricing calculation with full cost inputs."""
        service = MockPricingService()
        result = service.calculate_price(
            category="Bamboo & Cane Craft",
            material="Natural Assam Bamboo",
            production_time="3 days",
            dimensions="30cm x 30cm",
            raw_material_cost=250.0,
            labor_cost=1200.0,
            overhead=150.0,
            quantity=10
        )
        self.assertIn("suggested_price_min", result)
        self.assertIn("suggested_price_max", result)
        self.assertGreater(result["suggested_price_max"], result["suggested_price_min"])
        self.assertEqual(result["currency"], "INR")
        self.assertEqual(result["confidence"], "demo")
        self.assertIn("AI-assisted suggested price range", result["reason"])
        self.assertIn("handmade_nature", result["pricing_factors"])
        self.assertIn("material", result["pricing_factors"])
        self.assertIn("production_time", result["pricing_factors"])
        self.assertIn("category", result["pricing_factors"])
        self.assertIn("breakdown", result)
        self.assertEqual(result["breakdown"]["raw_material_cost"], 250.0)
        self.assertEqual(result["breakdown"]["labor_cost"], 1200.0)
        self.assertEqual(result["breakdown"]["overhead"], 150.0)
        self.assertEqual(result["breakdown"]["estimated_cost"], 1600.0)

    def test_02_pricing_calculation_missing_inputs(self):
        """Test fallback to demo benchmarks when all optional inputs are missing."""
        service = MockPricingService()
        # All optional fields missing/None
        result = service.calculate_price(
            category="",
            material="",
            production_time=None,
            dimensions=None,
            raw_material_cost=None,
            labor_cost=None,
            labor_hours=None,
            overhead=None,
            quantity=None
        )
        self.assertIsNotNone(result["suggested_price_min"])
        self.assertIsNotNone(result["suggested_price_max"])
        self.assertGreater(result["suggested_price_max"], result["suggested_price_min"])
        self.assertIn("AI-assisted suggested price range", result["reason"])
        self.assertEqual(result["breakdown"]["raw_material_cost_source"], "demo_market_benchmark")
        self.assertEqual(result["breakdown"]["demo_market_reference"], "Demo market reference")

    def test_03_pricing_bulk_discount(self):
        """Test that bulk quantity (100 units) provides unit economies compared to single unit."""
        service = MockPricingService()
        single = service.calculate_price(
            category="Textiles & Handloom",
            material="Chanderi Silk",
            raw_material_cost=700.0,
            quantity=1
        )
        bulk = service.calculate_price(
            category="Textiles & Handloom",
            material="Chanderi Silk",
            raw_material_cost=700.0,
            quantity=100
        )
        self.assertTrue(bulk["pricing_factors"]["bulk_discount_applied"])
        # Bulk unit price upper margin should be adjusted
        self.assertLessEqual(bulk["suggested_price_max"], single["suggested_price_max"])

    def test_04_pricing_mock_and_real_mode_resilience(self):
        """Test that MockPricingService and RealPricingService both return valid responses."""
        real_service = RealPricingService()
        result = real_service.calculate_price(
            category="Pottery & Ceramics",
            material="Terracotta Clay",
            raw_material_cost=300.0
        )
        self.assertIn("suggested_price_min", result)
        self.assertIn("suggested_price_max", result)
        self.assertEqual(result["currency"], "INR")

    def test_05_calculate_smart_price_wrapper(self):
        """Test backward-compatible wrapper calculate_smart_price."""
        res = calculate_smart_price(
            category="Bamboo & Cane Craft",
            material="Natural Bamboo",
            production_time="3 days",
            raw_material_cost=200.0,
            mock=True
        )
        self.assertIn("suggested_price_min", res)
        self.assertIn("suggested_price_max", res)
        self.assertIn("pricing_factors", res)

    def test_06_demo_market_references_dataset(self):
        """Verify demo market reference data includes bamboo basket, pottery, handwoven textile, wooden handicraft."""
        data = load_demo_market_references()
        self.assertEqual(data["dataset_label"], "Demo market reference")
        categories = data["categories"]
        self.assertIn("Bamboo & Cane Craft", categories)
        self.assertIn("Pottery & Ceramics", categories)
        self.assertIn("Textiles & Handloom", categories)
        self.assertIn("Woodcraft", categories)

    # ==========================================
    # 2. MARKETPLACE & BUYER FEED TESTS
    # ==========================================
    def test_07_buyer_product_browse(self):
        """Test GET /api/buyer/products returns catalogue products."""
        res = self.client.get("/api/buyer/products")
        self.assertEqual(res.status_code, 200)
        items = res.json()
        self.assertIsInstance(items, list)
        self.assertGreaterEqual(len(items), 1)

    def test_08_buyer_product_search(self):
        """Test search query filtering on buyer feed."""
        res = self.client.get("/api/buyer/products?q=Bamboo")
        self.assertEqual(res.status_code, 200)
        items = res.json()
        self.assertTrue(all("bamboo" in item["title"].lower() or "bamboo" in item["material"].lower() for item in items))

    def test_09_buyer_category_filtering(self):
        """Test category query filtering on buyer feed."""
        res = self.client.get("/api/buyer/products?category=Textiles")
        self.assertEqual(res.status_code, 200)
        items = res.json()
        for item in items:
            self.assertIn("textile", item["category"].lower())

    # ==========================================
    # 3. ORDER REQUESTS & B2B LINKAGE TESTS
    # ==========================================
    def test_10_bulk_order_request_creation(self):
        """Test submitting a valid B2B bulk order request."""
        # Get first product
        prod_res = self.client.get("/api/products")
        prod = prod_res.json()[0]

        order_payload = {
            "product_id": prod["id"],
            "buyer_name": "FabIndia Sourcing Unit",
            "buyer_contact": "procurement@fabindia.com",
            "quantity": 100,
            "message": "Interested in ordering 100 pieces for our retail stores.",
            "price_offered": 850.0
        }
        res = self.client.post("/api/orders/request", json=order_payload)
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertIn("id", data)
        self.assertEqual(data["status"], "pending")
        self.assertEqual(data["quantity"], 100)
        self.assertEqual(data["message"], order_payload["message"])
        self.assertEqual(data["product_title"], prod["title"])
        self.order_id = data["id"]

    def test_11_invalid_quantity_rejection(self):
        """Test that invalid quantities (<=0), empty buyer name, and non-existent products are rejected."""
        prod_res = self.client.get("/api/products")
        prod = prod_res.json()[0]

        # Quantity = 0
        payload_zero = {
            "product_id": prod["id"],
            "buyer_name": "Invalid Buyer",
            "quantity": 0,
            "message": "Zero quantity test"
        }
        res_zero = self.client.post("/api/orders/request", json=payload_zero)
        self.assertEqual(res_zero.status_code, 422)

        # Quantity = -5
        payload_neg = {
            "product_id": prod["id"],
            "buyer_name": "Invalid Buyer",
            "quantity": -5,
            "message": "Negative quantity test"
        }
        res_neg = self.client.post("/api/orders/request", json=payload_neg)
        self.assertEqual(res_neg.status_code, 422)

        # Empty buyer name
        payload_empty_name = {
            "product_id": prod["id"],
            "buyer_name": "   ",
            "quantity": 10,
            "message": "Empty buyer test"
        }
        res_empty = self.client.post("/api/orders/request", json=payload_empty_name)
        self.assertEqual(res_empty.status_code, 422)

        # Non-existent product ID
        payload_no_prod = {
            "product_id": "prod-non-existent-999",
            "buyer_name": "Valid Buyer",
            "quantity": 10,
            "message": "Non-existent product test"
        }
        res_no_prod = self.client.post("/api/orders/request", json=payload_no_prod)
        self.assertEqual(res_no_prod.status_code, 404)

    def test_12_order_status_update(self):
        """Test updating order status across requested, accepted, rejected, and completed."""
        prod_res = self.client.get("/api/products")
        prod = prod_res.json()[0]

        create_res = self.client.post("/api/orders/request", json={
            "product_id": prod["id"],
            "buyer_name": "Boutique Retailer",
            "quantity": 50,
            "message": "Test inquiry for status transitions."
        })
        order_id = create_res.json()["id"]

        # Fetch single order by ID
        get_res = self.client.get(f"/api/orders/{order_id}")
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.json()["status"], "pending")

        # Set to requested
        patch_req = self.client.patch(f"/api/orders/{order_id}/status", json={"status": "requested"})
        self.assertEqual(patch_req.status_code, 200)
        self.assertEqual(patch_req.json()["status"], "requested")

        # Accept order
        patch_accept = self.client.patch(f"/api/orders/{order_id}/status", json={"status": "accepted"})
        self.assertEqual(patch_accept.status_code, 200)
        self.assertEqual(patch_accept.json()["status"], "accepted")

        # Complete order
        patch_complete = self.client.patch(f"/api/orders/{order_id}/status", json={"status": "completed"})
        self.assertEqual(patch_complete.status_code, 200)
        self.assertEqual(patch_complete.json()["status"], "completed")

        # Reject order
        patch_reject = self.client.patch(f"/api/orders/{order_id}/status", json={"status": "rejected"})
        self.assertEqual(patch_reject.status_code, 200)
        self.assertEqual(patch_reject.json()["status"], "rejected")

        # Invalid status
        patch_invalid = self.client.patch(f"/api/orders/{order_id}/status", json={"status": "invalid_status"})
        self.assertEqual(patch_invalid.status_code, 400)

    # ==========================================
    # 4. DEDICATED PRICING ENDPOINTS
    # ==========================================
    def test_13_pricing_estimate_endpoint(self):
        """Test POST /api/pricing/estimate on-the-fly endpoint."""
        payload = {
            "category": "Pottery & Ceramics",
            "material": "Clay / Terracotta",
            "raw_material_cost": 220.0,
            "labor_hours": 14,
            "quantity": 60
        }
        res = self.client.post("/api/pricing/estimate", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("suggested_price_min", data)
        self.assertIn("suggested_price_max", data)
        self.assertEqual(data["currency"], "INR")
        self.assertEqual(data["confidence"], "demo")

    def test_14_pricing_reference_data_endpoint(self):
        """Test GET /api/pricing/reference-data."""
        res = self.client.get("/api/pricing/reference-data")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["dataset_label"], "Demo market reference")

    # ==========================================
    # 5. FULL ARTISAN -> BUYER WORKFLOW
    # ==========================================
    def test_15_artisan_to_buyer_end_to_end_flow(self):
        """
        Complete flow test:
        1. Artisan creates product
        2. AI calculates and applies suggested price bounds
        3. Product appears in B2B buyer catalogue
        4. B2B buyer selects product and submits bulk order request
        5. Artisan receives order in pending state
        6. Artisan accepts bulk order
        """
        # Step 1: Artisan creates product
        new_prod_payload = {
            "title": "Assam Golden Muga Silk Stole",
            "description_english": "Natural gold-tinted organic wild silk stole handcrafted on ancestral handlooms.",
            "description_hindi": "असम का प्रसिद्ध प्राकृतिक सुनहरा मूगा सिल्क स्टोल।",
            "category": "Textiles & Handloom",
            "material": "Wild Muga Silk",
            "production_time": "6 days",
            "artisan_id": "art-010",
            "artisan_name": "Ananya Barua",
            "location": "Sualkuchi, Assam",
            "image_url": "https://images.unsplash.com/photo-1610030469983-98e550d6193c"
        }
        create_res = self.client.post("/api/products", json=new_prod_payload)
        self.assertEqual(create_res.status_code, 201)
        prod_id = create_res.json()["id"]

        # Step 2: Suggested price calculation
        price_res = self.client.post(f"/api/products/{prod_id}/price", json={
            "raw_material_cost": 850.0,
            "labor_hours": 36
        })
        self.assertEqual(price_res.status_code, 200)
        prod_with_price = price_res.json()
        self.assertIsNotNone(prod_with_price["suggested_price_min"])
        self.assertIsNotNone(prod_with_price["suggested_price_max"])

        # Step 3: B2B Buyer discovers product in feed
        buyer_feed_res = self.client.get("/api/buyer/products?q=Muga")
        self.assertEqual(buyer_feed_res.status_code, 200)
        matched_items = buyer_feed_res.json()
        self.assertGreaterEqual(len(matched_items), 1)
        self.assertEqual(matched_items[0]["id"], prod_id)

        # Step 4: B2B Buyer submits bulk order request
        order_res = self.client.post("/api/orders/request", json={
            "product_id": prod_id,
            "buyer_name": "Heritage Luxury Retailers Ltd",
            "buyer_contact": "orders@heritageretail.com",
            "quantity": 100,
            "message": "Interested in ordering 100 pieces for our Diwali festive collection.",
            "price_offered": prod_with_price["suggested_price_min"]
        })
        self.assertEqual(order_res.status_code, 201)
        order_data = order_res.json()
        self.assertEqual(order_data["status"], "pending")
        self.assertEqual(order_data["quantity"], 100)
        self.assertEqual(order_data["product_id"], prod_id)

        # Step 5: Artisan retrieves orders for this product
        artisan_orders = self.client.get(f"/api/orders?product_id={prod_id}")
        self.assertEqual(artisan_orders.status_code, 200)
        self.assertEqual(len(artisan_orders.json()), 1)

        # Step 6: Artisan accepts the order
        accept_res = self.client.patch(f"/api/orders/{order_data['id']}/status", json={"status": "accepted"})
        self.assertEqual(accept_res.status_code, 200)
        self.assertEqual(accept_res.json()["status"], "accepted")


if __name__ == "__main__":
    unittest.main()
