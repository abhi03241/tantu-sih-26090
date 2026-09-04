"""
TANTU End-to-End Smoke & Integration Flow Test
Validates the complete Smart India Hackathon (SIH 26090) pipeline:
Artisan Product Draft -> Voice NLP -> Studio Vision Enhancement -> Fair Pricing Engine ->
Catalogue Generation -> Marketplace Showcase -> Buyer B2B Bulk Order -> Order Lifecycle Status.
"""
import sys
import os
import unittest
from fastapi.testclient import TestClient

# Add project root to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Ensure Windows cp1252 stdout handles Hindi / Devanagari text safely
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from backend.app.main import app
from backend.app.database import init_db
from backend.app.seed_data import seed_demo_data


class TestSmokeIntegrationFlow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        seed_demo_data()
        cls.client = TestClient(app)

    def test_complete_end_to_end_artisan_to_buyer_flow(self):
        print("\n" + "="*70)
        print(">>> STARTING TANTU END-TO-END INTEGRATION SMOKE TEST")
        print("="*70)

        # ----------------------------------------------------
        # STEP 1: Artisan Uploads Raw Product Draft
        # ----------------------------------------------------
        print("\n[STEP 1] Artisan creates new raw product listing...")
        draft_payload = {
            "title": "Kashmir Hand-Embroidered Pashmina Shawl",
            "description_english": "Fine cashmere wool shawl with Sozni embroidery hand-stitched by Srinagar artisans.",
            "description_hindi": "श्रीनगर के कारीगरों द्वारा हाथ से काढ़ी गई कश्मीरी पश्मीना शॉल।",
            "category": "Textiles & Handloom",
            "material": "Pure Pashmina Wool",
            "dimensions": "2m x 1m",
            "production_time": "14 days",
            "tags": ["pashmina", "kashmir", "sozni", "shawl", "handloom"],
            "image_url": "https://images.unsplash.com/photo-1607344645866-009c320c5ab8?w=800",
            "artisan_id": "art-002",
            "artisan_name": "Ramesh Ansari",
            "location": "Chanderi, Madhya Pradesh"
        }
        res_create = self.client.post("/api/products", json=draft_payload)
        self.assertEqual(res_create.status_code, 201)
        product = res_create.json()
        prod_id = product["id"]
        print(f"  [OK] Product created successfully! ID: {prod_id}")

        # ----------------------------------------------------
        # STEP 2: Artisan Adds Voice Audio Transcript (NLP Module - M)
        # ----------------------------------------------------
        print("\n[STEP 2] Simulating Artisan Voice Note Processing (NLP)...")
        voice_payload = {
            "audio_transcript": "यह शुद्ध कश्मीरी पश्मीना शॉल है जिसे सोजनी कढ़ाई से 14 दिनों में तैयार किया गया है।",
            "language": "hi"
        }
        res_voice = self.client.post(f"/api/products/{prod_id}/voice", json=voice_payload)
        self.assertEqual(res_voice.status_code, 200)
        product = res_voice.json()
        self.assertIsNotNone(product["description_hindi"])
        self.assertIsNotNone(product["sentiment"])
        print(f"  [OK] Voice processed: Sentiment: '{product.get('sentiment')}'")

        # ----------------------------------------------------
        # STEP 3: AI Studio Image Enhancement (Vision Module - R)
        # ----------------------------------------------------
        print("\n[STEP 3] Triggering AI Studio Image Enhancement (Vision)...")
        res_enhance = self.client.post(f"/api/products/{prod_id}/enhance-image", json={
            "prompt": "Professional boutique lighting with clean white studio background"
        })
        self.assertEqual(res_enhance.status_code, 200)
        product = res_enhance.json()
        self.assertIsNotNone(product["enhanced_image_url"])
        print(f"  [OK] Studio photo enhanced: {product['enhanced_image_url']}")

        # ----------------------------------------------------
        # STEP 4: Smart Fair Wage Pricing Engine (Pricing Module - S)
        # ----------------------------------------------------
        print("\n[STEP 4] Running Smart Fair Wage Pricing Engine...")
        pricing_payload = {
            "raw_material_cost": 2500.0,
            "labor_hours": 45
        }
        res_price = self.client.post(f"/api/products/{prod_id}/price", json=pricing_payload)
        self.assertEqual(res_price.status_code, 200)
        product = res_price.json()
        self.assertGreater(product["suggested_price_min"], 0)
        self.assertGreaterEqual(product["suggested_price_max"], product["suggested_price_min"])
        print(f"  [OK] Fair Wage Suggested Price: INR {product['suggested_price_min']} - {product['suggested_price_max']}")

        # ----------------------------------------------------
        # STEP 5: AI Smart Catalogue Generation (NLP Module - M)
        # ----------------------------------------------------
        print("\n[STEP 5] Generating Multi-Lingual Smart Marketing Copy...")
        res_cat = self.client.post(f"/api/products/{prod_id}/generate-catalogue")
        self.assertEqual(res_cat.status_code, 200)
        product = res_cat.json()
        self.assertIn("sih-artisan", product.get("tags", []))
        print(f"  [OK] Smart marketing narrative: {product.get('story')[:70]}...")

        # ----------------------------------------------------
        # STEP 6: Urban B2B Buyer Marketplace Search (Frontend Feed)
        # ----------------------------------------------------
        print("\n[STEP 6] Urban B2B Buyer searches marketplace for handcrafted artisan products...")
        res_feed = self.client.get("/api/buyer/products?q=handcrafted")
        self.assertEqual(res_feed.status_code, 200)
        found_products = res_feed.json()
        self.assertTrue(any(p["id"] == prod_id for p in found_products))
        print(f"  [OK] Buyer found {len(found_products)} matching products in catalogue.")

        # ----------------------------------------------------
        # STEP 7: B2B Buyer Submits Bulk Order Request
        # ----------------------------------------------------
        print("\n[STEP 7] Buyer submits bulk purchase request...")
        order_payload = {
            "product_id": prod_id,
            "buyer_id": "buy-001",
            "buyer_name": "FabIndia Sourcing & Merchandising Team",
            "buyer_contact": "sourcing.crafts@fabindia.com / +91-11-40001234",
            "quantity": 25,
            "notes": "Bulk order for winter premier handloom festival across 12 outlets.",
            "message": "Bulk order for winter premier handloom festival across 12 outlets.",
            "price_offered": 6000.0
        }
        res_order = self.client.post("/api/orders/request", json=order_payload)
        self.assertEqual(res_order.status_code, 201)
        order = res_order.json()
        order_id = order["id"]
        self.assertEqual(order["status"], "pending")
        self.assertEqual(order["quantity"], 25)
        print(f"  [OK] Bulk order requested! Order ID: {order_id} (Status: {order['status']})")

        # ----------------------------------------------------
        # STEP 8: Artisan Reviews and Accepts Order
        # ----------------------------------------------------
        print("\n[STEP 8] Artisan accepts order and marks in-production...")
        res_status = self.client.patch(f"/api/orders/{order_id}/status", json={"status": "accepted"})
        self.assertEqual(res_status.status_code, 200)
        updated_order = res_status.json()
        self.assertEqual(updated_order["status"], "accepted")
        print(f"  [OK] Order lifecycle updated to: '{updated_order['status']}'")

        # Clean up
        self.client.delete(f"/api/products/{prod_id}")
        print("\n" + "="*70)
        print(">>> TANTU END-TO-END SMOKE TEST PASSED WITH 100% SUCCESS!")
        print("="*70)


if __name__ == "__main__":
    unittest.main()
