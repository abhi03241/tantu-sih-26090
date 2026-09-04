import sys
import os
import unittest
from fastapi.testclient import TestClient

# Add project root to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.main import app
from backend.app.database import init_db
from backend.app.seed_data import seed_demo_data


class TestTantuBackendAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        seed_demo_data()
        cls.client = TestClient(app)

    def test_01_health_and_root(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "online")

        res_health = self.client.get("/api/health")
        self.assertEqual(res_health.status_code, 200)
        self.assertEqual(res_health.json()["status"], "healthy")

    def test_02_get_products(self):
        res = self.client.get("/api/products")
        self.assertEqual(res.status_code, 200)
        products = res.json()
        self.assertIsInstance(products, list)
        self.assertGreaterEqual(len(products), 1)

    def test_03_create_product(self):
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
            "image_url": "https://images.unsplash.com/photo-1605379399642-870262d3d051",
            "artisan_id": "art-005",
            "artisan_name": "Ram Prasad",
            "location": "Gorakhpur, Uttar Pradesh"
        }
        res = self.client.post("/api/products", json=payload)
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertIn("id", data)
        self.assertEqual(data["title"], payload["title"])
        self.product_id = data["id"]

    def test_04_get_product_by_id(self):
        # Fetch one of the seeded items
        res = self.client.get("/api/products")
        first_id = res.json()[0]["id"]

        res_single = self.client.get(f"/api/products/{first_id}")
        self.assertEqual(res_single.status_code, 200)
        self.assertEqual(res_single.json()["id"], first_id)

    def test_05_voice_processing(self):
        res = self.client.get("/api/products")
        prod_id = res.json()[0]["id"]

        voice_payload = {
            "audio_transcript": "यह हाथ से बना बांस का झूला है जो मजबूत प्राकृतिक बांस से बना है।",
            "language": "hi"
        }
        res_voice = self.client.post(f"/api/products/{prod_id}/voice", json=voice_payload)
        self.assertEqual(res_voice.status_code, 200)
        data = res_voice.json()
        self.assertIsNotNone(data["description_hindi"])

    def test_06_enhance_image(self):
        res = self.client.get("/api/products")
        prod_id = res.json()[0]["id"]

        res_enhance = self.client.post(f"/api/products/{prod_id}/enhance-image")
        self.assertEqual(res_enhance.status_code, 200)
        data = res_enhance.json()
        self.assertIsNotNone(data["enhanced_image_url"])

    def test_07_generate_catalogue(self):
        res = self.client.get("/api/products")
        prod_id = res.json()[0]["id"]

        res_cat = self.client.post(f"/api/products/{prod_id}/generate-catalogue")
        self.assertEqual(res_cat.status_code, 200)
        data = res_cat.json()
        self.assertIsNotNone(data["description_english"])

    def test_08_smart_pricing(self):
        res = self.client.get("/api/products")
        prod_id = res.json()[0]["id"]

        res_price = self.client.post(f"/api/products/{prod_id}/price")
        self.assertEqual(res_price.status_code, 200)
        data = res_price.json()
        self.assertIsNotNone(data["suggested_price_min"])
        self.assertIsNotNone(data["suggested_price_max"])

    def test_09_artisan_and_buyer_feeds(self):
        res_artisan = self.client.get("/api/artisan/products?artisan_id=art-001")
        self.assertEqual(res_artisan.status_code, 200)

        res_buyer = self.client.get("/api/buyer/products")
        self.assertEqual(res_buyer.status_code, 200)

    def test_10_order_requests(self):
        res = self.client.get("/api/products")
        prod_id = res.json()[0]["id"]

        order_payload = {
            "product_id": prod_id,
            "buyer_name": "FabIndia Procurement Team",
            "buyer_contact": "procurement@fabindia.com",
            "quantity": 100,
            "notes": "Sample bulk order for upcoming festive season.",
            "price_offered": 800.0
        }
        res_order = self.client.post("/api/orders/request", json=order_payload)
        self.assertEqual(res_order.status_code, 201)
        data = res_order.json()
        self.assertEqual(data["status"], "pending")

        res_list = self.client.get("/api/orders")
        self.assertEqual(res_list.status_code, 200)
        self.assertGreaterEqual(len(res_list.json()), 1)

        # Test single order retrieval and status patch
        order_id = data["id"]
        res_get_order = self.client.get(f"/api/orders/{order_id}")
        self.assertEqual(res_get_order.status_code, 200)

        res_patch = self.client.patch(f"/api/orders/{order_id}/status?new_status=accepted")
        self.assertEqual(res_patch.status_code, 200)
        self.assertEqual(res_patch.json()["status"], "accepted")

    def test_11_profiles_and_users(self):
        artisan_payload = {
            "user_id": "art-099",
            "artisan_name": "Sita Devi",
            "craft_type": "Madhubani Painting",
            "location": "Madhubani, Bihar",
            "bio": "Traditional Mithila painter.",
            "phone": "+91-9876500000"
        }
        res_art = self.client.post("/api/artisan/profile", json=artisan_payload)
        self.assertEqual(res_art.status_code, 201)

        res_art_get = self.client.get("/api/artisan/profile/art-099")
        self.assertEqual(res_art_get.status_code, 200)
        self.assertEqual(res_art_get.json()["artisan_name"], "Sita Devi")

        buyer_payload = {
            "user_id": "buyer-099",
            "buyer_name": "Craftsvilla Retail",
            "organization": "Craftsvilla India Pvt Ltd",
            "buyer_type": "Wholesaler",
            "contact_email": "procurement@craftsvilla.com"
        }
        res_buy = self.client.post("/api/buyer/profile", json=buyer_payload)
        self.assertEqual(res_buy.status_code, 201)

        res_buy_get = self.client.get("/api/buyer/profile/buyer-099")
        self.assertEqual(res_buy_get.status_code, 200)

    def test_12_delete_product(self):
        # Create temporary product to delete
        temp_payload = {
            "title": "Temporary Product for Deletion",
            "description_english": "Test desc",
            "description_hindi": "विवरण",
            "category": "Test Category",
            "material": "Test Material",
            "image_url": "https://example.com/test.jpg"
        }
        res_create = self.client.post("/api/products", json=temp_payload)
        prod_id = res_create.json()["id"]

        res_del = self.client.delete(f"/api/products/{prod_id}")
        self.assertEqual(res_del.status_code, 200)

        res_verify = self.client.get(f"/api/products/{prod_id}")
        self.assertEqual(res_verify.status_code, 404)


if __name__ == "__main__":
    unittest.main()

