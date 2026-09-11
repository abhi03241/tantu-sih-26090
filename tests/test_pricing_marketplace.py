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
        self.assertIsInstance(data["suggested_price_min"], (int, float))
        self.assertIsInstance(data["suggested_price_max"], (int, float))
        self.assertGreater(data["suggested_price_max"], data["suggested_price_min"])
        self.assertEqual(data["currency"], "INR")
        self.assertEqual(data["confidence"], "demo")

    def test_14_pricing_estimate_rejects_negative_cost_inputs(self):
        """Negative amounts are invalid inputs, not missing pricing information."""
        base_payload = {
            "category": "Bamboo & Cane Craft",
            "material": "Natural Bamboo"
        }
        for field in ("raw_material_cost", "labor_hours", "labor_cost", "overhead"):
            with self.subTest(field=field):
                payload = {**base_payload, field: -1}
                res = self.client.post("/api/pricing/estimate", json=payload)
                self.assertEqual(res.status_code, 422)

    def test_15_pricing_reference_data_endpoint(self):
        """Test GET /api/pricing/reference-data."""
        res = self.client.get("/api/pricing/reference-data")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["dataset_label"], "Demo market reference")

    # ==========================================
    # 5. FULL ARTISAN -> BUYER WORKFLOW
    # ==========================================
    def test_16_artisan_to_buyer_end_to_end_flow(self):
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

    # ==========================================
    # 6. MARKETPLACE PUBLICATION GUARDS & BULK ORDER LIFECYCLE
    # ==========================================
    def test_17_draft_and_processing_products_excluded_from_buyer_marketplace(self):
        """Confirm draft and processing products are excluded from buyer marketplace, while published appear."""
        # 1. Create a draft product
        draft_payload = {
            "title": "Unpublished Draft Bamboo Lamp",
            "description_english": "Handmade bamboo bedside lamp currently in draft review.",
            "description_hindi": "हाथ से बना बांस का लैंप ड्राफ्ट स्थिति में।",
            "category": "Bamboo & Cane Craft",
            "material": "Assam Bamboo",
            "image_url": "https://example.com/draft_lamp.jpg",
            "status": "draft"
        }
        res_draft = self.client.post("/api/products", json=draft_payload)
        self.assertEqual(res_draft.status_code, 201)
        draft_id = res_draft.json()["id"]

        # 2. Create a processing product
        proc_payload = {
            "title": "AI Processing Madhubani Scarf",
            "description_english": "Madhubani painted handwoven scarf undergoing AI enhancement.",
            "description_hindi": "मधुबनी चित्रकला स्कार्फ एआई संवर्द्धन प्रक्रिया में।",
            "category": "Textiles & Handloom",
            "material": "Tussar Silk",
            "image_url": "https://example.com/proc_scarf.jpg",
            "status": "processing"
        }
        res_proc = self.client.post("/api/products", json=proc_payload)
        self.assertEqual(res_proc.status_code, 201)
        proc_id = res_proc.json()["id"]

        # 3. Create a published product
        pub_payload = {
            "title": "Published Heritage Wooden Coaster Set",
            "description_english": "Set of 4 hand-carved Sheesham wood coasters with brass inlay.",
            "description_hindi": "शीशम की लकड़ी के ४ नक्काशीदार कोस्टर का सेट।",
            "category": "Woodcraft",
            "material": "Sheesham Wood",
            "image_url": "https://example.com/pub_coasters.jpg",
            "status": "published"
        }
        res_pub = self.client.post("/api/products", json=pub_payload)
        self.assertEqual(res_pub.status_code, 201)
        pub_id = res_pub.json()["id"]

        # Verify buyer marketplace feed excludes draft and processing
        buyer_feed = self.client.get("/api/buyer/products").json()
        buyer_ids = [p["id"] for p in buyer_feed]
        self.assertNotIn(draft_id, buyer_ids, "Draft product must NOT be visible in buyer marketplace")
        self.assertNotIn(proc_id, buyer_ids, "Processing product must NOT be visible in buyer marketplace")
        self.assertIn(pub_id, buyer_ids, "Published product MUST appear in buyer marketplace")

        # Product detail works for all
        detail_res = self.client.get(f"/api/products/{pub_id}")
        self.assertEqual(detail_res.status_code, 200)
        detail = detail_res.json()
        self.assertEqual(detail["title"], pub_payload["title"])
        self.assertEqual(detail["image_url"], pub_payload["image_url"])
        self.assertIsNotNone(detail["suggested_price_min"])
        self.assertIsNotNone(detail["suggested_price_max"])

    def test_18_unpublished_product_order_rejection_and_publish_flow(self):
        """Confirm unpublished product cannot receive order, quantity is validated, and order/status persist."""
        # 1. Create a draft product
        draft_res = self.client.post("/api/products", json={
            "title": "Experimental Terracotta Vase",
            "description_english": "Rustic hand-thrown terracotta clay flower vase.",
            "description_hindi": "हाथ से बना मिट्टी का सुंदर फूलदान।",
            "category": "Pottery & Ceramics",
            "material": "Natural Clay",
            "image_url": "https://example.com/vase.jpg",
            "status": "draft"
        })
        self.assertEqual(draft_res.status_code, 201)
        prod_id = draft_res.json()["id"]

        # 2. Attempt bulk order on draft product -> MUST be rejected with 409 Conflict
        order_payload = {
            "product_id": prod_id,
            "buyer_name": "FabIndia Procurement",
            "buyer_contact": "procurement@fabindia.com",
            "quantity": 50,
            "message": "Bulk purchase inquiry for Diwali."
        }
        res_order_draft = self.client.post("/api/orders/request", json=order_payload)
        self.assertEqual(res_order_draft.status_code, 409)
        self.assertIn("published", res_order_draft.json()["detail"].lower())

        # 3. Publish product via publish endpoint
        res_publish = self.client.patch(f"/api/products/{prod_id}/publish")
        self.assertEqual(res_publish.status_code, 200)
        self.assertEqual(res_publish.json()["status"], "published")

        # Check status endpoint
        res_status = self.client.get(f"/api/products/{prod_id}/status")
        self.assertEqual(res_status.status_code, 200)
        self.assertEqual(res_status.json()["status"], "published")

        # 4. Quantity validation: quantity <= 0 rejected with 422
        bad_qty_payload = {**order_payload, "quantity": 0}
        self.assertEqual(self.client.post("/api/orders/request", json=bad_qty_payload).status_code, 422)

        bad_neg_payload = {**order_payload, "quantity": -10}
        self.assertEqual(self.client.post("/api/orders/request", json=bad_neg_payload).status_code, 422)

        # 5. Submit valid bulk order now that product is published
        res_valid_order = self.client.post("/api/orders/request", json=order_payload)
        self.assertEqual(res_valid_order.status_code, 201)
        order_data = res_valid_order.json()
        order_id = order_data["id"]
        self.assertEqual(order_data["status"], "pending")

        # 6. Verify order persists
        res_get = self.client.get(f"/api/orders/{order_id}")
        self.assertEqual(res_get.status_code, 200)
        self.assertEqual(res_get.json()["quantity"], 50)
        self.assertEqual(res_get.json()["product_id"], prod_id)

        # 7. Verify status update persists
        res_patch = self.client.patch(f"/api/orders/{order_id}/status", json={"status": "accepted"})
        self.assertEqual(res_patch.status_code, 200)
        self.assertEqual(res_patch.json()["status"], "accepted")

        # Confirm persisted on re-fetch
        res_get_updated = self.client.get(f"/api/orders/{order_id}")
        self.assertEqual(res_get_updated.json()["status"], "accepted")

    def test_19_pricing_inputs_verification_and_disclaimer(self):
        """Verify pricing accepts material, labor hours, quantity, cost, overhead, region, min < max, and disclaims guaranteed truth."""
        estimate_payload = {
            "category": "Textiles & Handloom",
            "material": "Chanderi Silk Cotton",
            "dimensions": "2.5m x 1m",
            "production_time": "5 days",
            "raw_material_cost": 450.0,
            "labor_hours": 24,
            "labor_cost": 1800.0,
            "overhead": 250.0,
            "quantity": 100,
            "region": "Madhya Pradesh",
            "craft_type": "Handloom Weaving"
        }
        res = self.client.post("/api/pricing/estimate", json=estimate_payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()

        # Numeric min/max and min < max
        self.assertIsInstance(data["suggested_price_min"], (int, float))
        self.assertIsInstance(data["suggested_price_max"], (int, float))
        self.assertGreater(data["suggested_price_max"], data["suggested_price_min"])

        # Labeling must NOT claim guaranteed market truth
        self.assertEqual(data["pricing_label"], "AI-assisted suggested price range")
        self.assertEqual(data["confidence"], "demo")
        self.assertIn("AI-assisted suggested price range", data["reason"])
        self.assertNotIn("guaranteed truth", data["reason"].lower())
        self.assertNotIn("absolute price", data["reason"].lower())

        # Pricing factors present
        factors = data["pricing_factors"]
        self.assertIn("material", factors)
        self.assertIn("production_time", factors)
        self.assertIn("handmade_nature", factors)
        self.assertIn("category", factors)

        # Negative inputs rejected
        bad_cost = {**estimate_payload, "raw_material_cost": -50.0}
        self.assertEqual(self.client.post("/api/pricing/estimate", json=bad_cost).status_code, 422)

        bad_hours = {**estimate_payload, "labor_hours": -5}
        self.assertEqual(self.client.post("/api/pricing/estimate", json=bad_hours).status_code, 422)

        bad_overhead = {**estimate_payload, "overhead": -10.0}
        self.assertEqual(self.client.post("/api/pricing/estimate", json=bad_overhead).status_code, 422)

    def test_20_product_detail_fields_integrity(self):
        """Verify product detail works: image works, price works, and fields are correctly structured."""
        pub_products = self.client.get("/api/buyer/products").json()
        self.assertGreaterEqual(len(pub_products), 1)
        first_prod = pub_products[0]

        detail_res = self.client.get(f"/api/products/{first_prod['id']}")
        self.assertEqual(detail_res.status_code, 200)
        detail = detail_res.json()

        # Image works
        self.assertTrue(bool(detail.get("image_url") or detail.get("enhanced_image_url")))

        # Price works
        self.assertIsNotNone(detail.get("suggested_price_min"))
        self.assertIsNotNone(detail.get("suggested_price_max"))
        self.assertGreater(detail["suggested_price_max"], detail["suggested_price_min"])

        # Core fields work
        self.assertTrue(bool(detail.get("title")))
        self.assertTrue(bool(detail.get("category")))


if __name__ == "__main__":
    unittest.main()
