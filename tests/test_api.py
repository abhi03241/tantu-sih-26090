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
            "audio_transcript": "यह हाथ से बना बांस का झूला है जो मजबूत प्राकृतिक बांस से बना है। इसका आकार 120cm x 80cm है और इसे बनाने में 3 दिन लगते हैं।",
            "language": "hi"
        }
        res_voice = self.client.post(f"/api/products/{prod_id}/voice", json=voice_payload)
        self.assertEqual(res_voice.status_code, 200)
        data = res_voice.json()
        self.assertIsNotNone(data["description_hindi"])
        self.assertEqual(data["dimensions"], "120cm x 80cm")
        self.assertEqual(data["production_time"], "3 days")

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

        raw_notes = "This basket is made by our women's group with pride."
        res_cat = self.client.post(
            f"/api/products/{prod_id}/generate-catalogue",
            json={"raw_notes": raw_notes}
        )
        self.assertEqual(res_cat.status_code, 200)
        data = res_cat.json()
        self.assertIsNotNone(data["description_english"])
        self.assertIn(raw_notes, data["description_english"])
        self.assertEqual(data["narrative_type"], "Community-made")

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


if __name__ == "__main__":
    unittest.main()
