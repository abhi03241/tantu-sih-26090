import sys
import os
import unittest
from fastapi.testclient import TestClient

# Add project root to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.main import app
from backend.app.database import init_db, ProductRepository
from backend.app.seed_data import seed_demo_data


class TestTantuBackendAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Fresh db initialization and demo seed
        init_db()
        seed_demo_data()
        cls.client = TestClient(app)

    # ==========================================
    # 1. HEALTH & SYSTEM CONFIG TESTS
    # ==========================================
    def test_01_health_and_root(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "online")
        self.assertIn("sih_problem_statement", data)

        res_health = self.client.get("/api/health")
        self.assertEqual(res_health.status_code, 200)
        self.assertEqual(res_health.json()["status"], "healthy")

        res_config = self.client.get("/api/config")
        self.assertEqual(res_config.status_code, 200)
        self.assertIn("mock_ai", res_config.json())

    # ==========================================
    # 2. PRODUCT TESTS (Create, Retrieve, List)
    # ==========================================
    def test_02_create_and_retrieve_product(self):
        payload = {
            "title": "Terracotta Handpainted Festival Diya Set",
            "description_english": "Set of 6 handcrafted clay lamps decorated with eco-friendly acrylic colors.",
            "description_hindi": "६ मिट्टी के सजावटी दीयों का सुंदर सेट।",
            "category": "Pottery & Ceramics",
            "material": "Clay / Terracotta",
            "dimensions": "8cm x 8cm x 3cm",
            "production_time": "2 days",
            "tags": ["diya", "terracotta", "diwali", "festive"],
            "story": "Made by clay artisans in rural Gorakhpur.",
            "sentiment": "Warm, festive",
            "narrative_type": "Heritage Craft",
            "image_url": "https://images.unsplash.com/photo-1605379399642-870262d3d051",
            "artisan_id": "art-005",
            "artisan_name": "Ram Prasad",
            "location": "Gorakhpur, Uttar Pradesh"
        }
        # Create product
        res = self.client.post("/api/products", json=payload)
        self.assertEqual(res.status_code, 201)
        created = res.json()
        self.assertIn("id", created)
        self.assertEqual(created["title"], payload["title"])
        self.assertEqual(created["artisan_id"], "art-005")
        prod_id = created["id"]

        # Retrieve single product by id
        res_single = self.client.get(f"/api/products/{prod_id}")
        self.assertEqual(res_single.status_code, 200)
        self.assertEqual(res_single.json()["id"], prod_id)
        self.assertEqual(res_single.json()["title"], payload["title"])

        # Clean up created product
        del_res = self.client.delete(f"/api/products/{prod_id}")
        self.assertEqual(del_res.status_code, 200)

    def test_03_retrieve_all_products_and_filters(self):
        # Retrieve all products
        res = self.client.get("/api/products")
        self.assertEqual(res.status_code, 200)
        products = res.json()
        self.assertIsInstance(products, list)
        self.assertGreaterEqual(len(products), 4)

        # Filter by category
        res_cat = self.client.get("/api/products?category=Bamboo")
        self.assertEqual(res_cat.status_code, 200)
        bamboo_prods = res_cat.json()
        self.assertTrue(all("bamboo" in p["category"].lower() for p in bamboo_prods))

        # Filter by artisan_id
        res_art = self.client.get("/api/products?artisan_id=art-001")
        self.assertEqual(res_art.status_code, 200)
        self.assertTrue(all(p["artisan_id"] == "art-001" for p in res_art.json()))

        # Filter by search query
        res_search = self.client.get("/api/products?q=chanderi")
        self.assertEqual(res_search.status_code, 200)
        self.assertGreaterEqual(len(res_search.json()), 1)

    def test_04_get_nonexistent_product_returns_404(self):
        res = self.client.get("/api/products/prod-nonexistent-999")
        self.assertEqual(res.status_code, 404)

    # ==========================================
    # 3. CATALOGUE TESTS (Validation & Error Handling)
    # ==========================================
    def test_05_catalogue_required_fields_validation(self):
        # Missing title
        invalid_payload = {
            "description_english": "A basket without title",
            "category": "Bamboo",
            "image_url": "https://example.com/img.jpg"
        }
        res = self.client.post("/api/products", json=invalid_payload)
        self.assertEqual(res.status_code, 422)

        # Missing image_url
        invalid_payload_no_img = {
            "title": "No Image Product",
            "description_english": "Description",
            "description_hindi": "विवरण",
            "category": "Bamboo",
            "material": "Bamboo"
        }
        res_no_img = self.client.post("/api/products", json=invalid_payload_no_img)
        self.assertEqual(res_no_img.status_code, 422)

    def test_06_catalogue_missing_optional_fields(self):
        # Product with only minimal required fields
        minimal_payload = {
            "title": "Minimal Handmade Jute Bag",
            "description_english": "Eco-friendly natural jute bag.",
            "description_hindi": "प्राकृतिक जूट का थैला।",
            "category": "Jute Craft",
            "material": "Raw Jute",
            "image_url": "https://images.unsplash.com/photo-1544816155-12df9643f363"
        }
        res = self.client.post("/api/products", json=minimal_payload)
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertIsNone(data.get("dimensions"))
        self.assertIsNone(data.get("production_time"))
        self.assertEqual(data.get("tags"), [])
        self.assertIsNotNone(data.get("suggested_price_min"))  # auto-filled fallback

        # Clean up
        self.client.delete(f"/api/products/{data['id']}")

    def test_07_catalogue_generation_nlp(self):
        res = self.client.get("/api/products")
        prod_id = res.json()[0]["id"]

        res_cat = self.client.post(f"/api/products/{prod_id}/generate-catalogue")
        self.assertEqual(res_cat.status_code, 200)
        data = res_cat.json()
        self.assertIsNotNone(data["description_english"])
        self.assertIsNotNone(data["story"])
        self.assertIsNotNone(data["sentiment"])
        self.assertIn("narrative_type", data)

    def test_08_voice_processing_malformed_input(self):
        res = self.client.get("/api/products")
        prod_id = res.json()[0]["id"]

        # Missing audio transcript -> 422
        res_malformed = self.client.post(f"/api/products/{prod_id}/voice", json={})
        self.assertEqual(res_malformed.status_code, 422)

        # Empty transcript handled gracefully by fallback
        res_empty = self.client.post(f"/api/products/{prod_id}/voice", json={"audio_transcript": ""})
        self.assertEqual(res_empty.status_code, 200)
        self.assertIsNotNone(res_empty.json()["description_hindi"])

    # ==========================================
    # 4. PRICING TESTS (Inputs, Range Validity)
    # ==========================================
    def test_09_smart_pricing_valid_inputs(self):
        res = self.client.get("/api/products")
        prod_id = res.json()[0]["id"]

        payload = {
            "raw_material_cost": 300.0,
            "labor_hours": 12
        }
        res_price = self.client.post(f"/api/products/{prod_id}/price", json=payload)
        self.assertEqual(res_price.status_code, 200)
        data = res_price.json()
        min_p = data["suggested_price_min"]
        max_p = data["suggested_price_max"]
        self.assertIsNotNone(min_p)
        self.assertIsNotNone(max_p)
        self.assertGreater(min_p, 0)
        self.assertGreaterEqual(max_p, min_p)

    def test_10_smart_pricing_missing_inputs(self):
        res = self.client.get("/api/products")
        prod_id = res.json()[0]["id"]

        # Calling pricing without payload should fall back to category baseline
        res_empty = self.client.post(f"/api/products/{prod_id}/price", json={})
        self.assertEqual(res_empty.status_code, 200)
        data = res_empty.json()
        self.assertGreater(data["suggested_price_min"], 0)
        self.assertGreaterEqual(data["suggested_price_max"], data["suggested_price_min"])

    # ==========================================
    # 5. ORDER TESTS (Bulk, Validation, Status)
    # ==========================================
    def test_11_valid_bulk_order_request(self):
        res = self.client.get("/api/products")
        prod = res.json()[0]
        prod_id = prod["id"]

        order_payload = {
            "product_id": prod_id,
            "buyer_id": "buyer-001",
            "buyer_name": "FabIndia Sourcing & Merchandising Team",
            "buyer_contact": "sourcing.crafts@fabindia.com / +91-11-40001234",
            "quantity": 100,
            "notes": "Urgent procurement for Diwali festive exhibition.",
            "message": "Urgent procurement for Diwali festive exhibition.",
            "price_offered": 850.0
        }
        res_order = self.client.post("/api/orders/request", json=order_payload)
        self.assertEqual(res_order.status_code, 201)
        data = res_order.json()
        self.assertIn("id", data)
        self.assertEqual(data["product_id"], prod_id)
        self.assertEqual(data["buyer_name"], order_payload["buyer_name"])
        self.assertEqual(data["quantity"], 100)
        self.assertEqual(data["status"], "pending")
        self.assertEqual(data["product_title"], prod["title"])

        # Fetch created order by ID
        order_id = data["id"]
        res_get = self.client.get(f"/api/orders/{order_id}")
        self.assertEqual(res_get.status_code, 200)
        self.assertEqual(res_get.json()["id"], order_id)

    def test_12_invalid_order_quantity(self):
        res = self.client.get("/api/products")
        prod_id = res.json()[0]["id"]

        # Quantity = 0 must fail
        zero_payload = {
            "product_id": prod_id,
            "buyer_name": "Test Buyer",
            "buyer_contact": "buyer@test.com",
            "quantity": 0
        }
        res_zero = self.client.post("/api/orders/request", json=zero_payload)
        self.assertEqual(res_zero.status_code, 422)

        # Quantity < 0 must fail
        negative_payload = {
            "product_id": prod_id,
            "buyer_name": "Test Buyer",
            "buyer_contact": "buyer@test.com",
            "quantity": -10
        }
        res_neg = self.client.post("/api/orders/request", json=negative_payload)
        self.assertEqual(res_neg.status_code, 422)

    def test_13_order_missing_product(self):
        missing_payload = {
            "product_id": "prod-nonexistent-404",
            "buyer_name": "Test Buyer",
            "buyer_contact": "buyer@test.com",
            "quantity": 25
        }
        res = self.client.post("/api/orders/request", json=missing_payload)
        self.assertEqual(res.status_code, 404)

    def test_14_order_status_update(self):
        # Create an order
        res = self.client.get("/api/products")
        prod_id = res.json()[0]["id"]

        order_res = self.client.post("/api/orders/request", json={
            "product_id": prod_id,
            "buyer_name": "Status Test Buyer",
            "buyer_contact": "buyer@statustest.com",
            "quantity": 10
        })
        order_id = order_res.json()["id"]
        self.assertEqual(order_res.json()["status"], "pending")

        # Update status to accepted
        res_accept = self.client.patch(f"/api/orders/{order_id}/status", json={"status": "accepted"})
        self.assertEqual(res_accept.status_code, 200)
        self.assertEqual(res_accept.json()["status"], "accepted")

        # Update status to fulfilled
        res_fulfilled = self.client.patch(f"/api/orders/{order_id}/status", json={"status": "fulfilled"})
        self.assertEqual(res_fulfilled.status_code, 200)
        self.assertEqual(res_fulfilled.json()["status"], "fulfilled")

        # Invalid status should return 400
        res_invalid = self.client.patch(f"/api/orders/{order_id}/status", json={"status": "invalid_status_xyz"})
        self.assertEqual(res_invalid.status_code, 400)

    # ==========================================
    # 6. AI MODULE INTEGRATION & CONTRACT VALIDITY
    # ==========================================
    def test_15_ai_modules_conform_to_product_schema(self):
        res = self.client.get("/api/products")
        prod_id = res.json()[0]["id"]

        # Step 1: Voice processing
        voice_res = self.client.post(f"/api/products/{prod_id}/voice", json={
            "audio_transcript": "यह हाथ से बना चंदेरी दुपट्टा है जो रेशम और जरी से बना है।",
            "language": "hi"
        })
        self.assertEqual(voice_res.status_code, 200)
        voice_prod = voice_res.json()
        self.assertIn("title", voice_prod)
        self.assertIn("description_english", voice_prod)
        self.assertIn("description_hindi", voice_prod)

        # Step 2: Image Enhancement
        img_res = self.client.post(f"/api/products/{prod_id}/enhance-image", json={
            "prompt": "Studio warm lighting with clean backdrop"
        })
        self.assertEqual(img_res.status_code, 200)
        img_prod = img_res.json()
        self.assertIsNotNone(img_prod["enhanced_image_url"])

        # Step 3: Smart Pricing
        price_res = self.client.post(f"/api/products/{prod_id}/price", json={
            "raw_material_cost": 400.0,
            "labor_hours": 20
        })
        self.assertEqual(price_res.status_code, 200)
        price_prod = price_res.json()
        self.assertGreater(price_prod["suggested_price_min"], 0)
        self.assertGreaterEqual(price_prod["suggested_price_max"], price_prod["suggested_price_min"])

        # Step 4: Final verification that Product retrieved from DB has all AI enhancements
        final_res = self.client.get(f"/api/products/{prod_id}")
        self.assertEqual(final_res.status_code, 200)
        final_prod = final_res.json()
        self.assertIsNotNone(final_prod["enhanced_image_url"])
        self.assertIsNotNone(final_prod["suggested_price_min"])
        self.assertIsNotNone(final_prod["suggested_price_max"])

    # ==========================================
    # 7. ARTISAN & BUYER PROFILES & FEEDS
    # ==========================================
    def test_16_artisan_and_buyer_profiles(self):
        # List artisan profiles
        art_res = self.client.get("/api/artisan/profiles")
        self.assertEqual(art_res.status_code, 200)
        artisans = art_res.json()
        self.assertGreaterEqual(len(artisans), 4)

        # Get specific artisan profile
        art_profile = self.client.get("/api/artisan/profile/art-001")
        self.assertEqual(art_profile.status_code, 200)
        self.assertEqual(art_profile.json()["artisan_name"], "Lakshmi Devi")
        self.assertIn("Silchar", art_profile.json()["location"])

        # List buyers
        buy_res = self.client.get("/api/buyer/profiles")
        self.assertEqual(buy_res.status_code, 200)
        buyers = buy_res.json()
        self.assertGreaterEqual(len(buyers), 3)

        # Get specific buyer
        buy_profile = self.client.get("/api/buyer/profile/buyer-001")
        self.assertEqual(buy_profile.status_code, 200)
        self.assertIn("FabIndia", buy_profile.json()["buyer_name"])


if __name__ == "__main__":
    unittest.main()
