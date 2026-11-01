"""
End-to-End Integration Demo Test for TANTU Backend Artisan Processing Flow (Prompt #3)
Verifies: Create -> Upload Image -> Voice Input -> AI Processing -> Catalogue Edit -> Publish -> Buyer Retrieval.
"""
import sys
import os
import io
import unittest
from PIL import Image
from fastapi.testclient import TestClient

# Add project root to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.main import app
from backend.app.database import init_db
from backend.app.seed_data import seed_demo_data
from backend.app.services.orchestrator import ProductPipelineOrchestrator


class TestTantuIntegrationPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        seed_demo_data()
        cls.client = TestClient(app)

    def test_01_full_artisan_lifecycle(self):
        """
        Prompt #3 Step 12 End-to-End Test:
        Create Product -> Upload Image -> Submit Voice -> Process AI Pipeline -> Edit Catalogue -> Publish -> Retrieve as Buyer.
        """
        # Step 1: Create Product (draft)
        create_payload = {
            "title": "Bamboo Basket Draft",
            "category": "Bamboo & Cane Craft",
            "artisan_id": "art-001"
        }
        res_create = self.client.post("/api/products", json=create_payload)
        self.assertEqual(res_create.status_code, 201)
        prod = res_create.json()
        prod_id = prod["id"]
        self.assertEqual(prod["status"], "draft")

        # Step 2: Upload Product Image
        img_buffer = io.BytesIO()
        Image.new("RGB", (60, 60), (180, 120, 80)).save(img_buffer, format="PNG")
        img_bytes = img_buffer.getvalue()
        files = {"file": ("bamboo_basket.png", img_bytes, "image/png")}
        res_upload = self.client.post(f"/api/products/{prod_id}/upload-image", files=files)
        self.assertEqual(res_upload.status_code, 200)
        self.assertIn("/uploads/", res_upload.json()["image_url"])

        # Step 3: Submit Artisan Voice/Text
        voice_payload = {
            "audio_transcript": "Ye bamboo ki tokri hai. Isko banane mein mujhe do din lagte hain. Meri maa ne mujhe ye banana sikhaya tha.",
            "language": "hi"
        }
        res_voice = self.client.post(f"/api/products/{prod_id}/voice", json=voice_payload)
        self.assertEqual(res_voice.status_code, 200)

        # Step 4: Process AI Pipeline
        process_payload = {
            "audio_transcript": "Ye bamboo ki tokri hai. Isko banane mein mujhe do din lagte hain. Meri maa ne mujhe ye banana sikhaya tha.",
            "raw_material_cost": 250.0
        }
        res_process = self.client.post(f"/api/products/{prod_id}/process", json=process_payload)
        self.assertEqual(res_process.status_code, 200)
        process_resp = res_process.json()

        self.assertEqual(process_resp["status"], "ready")
        processed_prod = process_resp["product"]
        self.assertIsNotNone(processed_prod["description_english"])
        self.assertIsNotNone(processed_prod["description_hindi"])
        self.assertIsNotNone(processed_prod["enhanced_image_url"])
        self.assertGreater(processed_prod["suggested_price_min"], 0)

        # Check status endpoint
        res_status = self.client.get(f"/api/products/{prod_id}/status")
        self.assertEqual(res_status.status_code, 200)
        self.assertEqual(res_status.json()["status"], "ready")

        # Step 5: Edit Catalogue
        edit_payload = {
            "title": "Masterpiece Handcrafted Bamboo Utility Basket",
            "production_time": "2 days"
        }
        res_edit = self.client.put(f"/api/products/{prod_id}", json=edit_payload)
        self.assertEqual(res_edit.status_code, 200)
        self.assertEqual(res_edit.json()["title"], "Masterpiece Handcrafted Bamboo Utility Basket")

        # Draft product should NOT be in buyer feed yet
        res_buyer_before = self.client.get("/api/buyer/products")
        buyer_ids_before = [p["id"] for p in res_buyer_before.json()]
        self.assertNotIn(prod_id, buyer_ids_before)

        # Step 6: Publish Product
        res_pub = self.client.patch(f"/api/products/{prod_id}/publish")
        self.assertEqual(res_pub.status_code, 200)
        self.assertEqual(res_pub.json()["status"], "published")

        # Step 7: Retrieve as Buyer
        res_buyer_after = self.client.get("/api/buyer/products")
        buyer_ids_after = [p["id"] for p in res_buyer_after.json()]
        self.assertIn(prod_id, buyer_ids_after)

    def test_02_image_upload_validation(self):
        """
        Verifies image upload validates file formats and rejects unsupported file types.
        """
        # Create temp draft product
        res = self.client.post("/api/products", json={"title": "Temp Test Product"})
        prod_id = res.json()["id"]

        # Upload invalid file (text file)
        invalid_file = {"file": ("script.sh", b"#!/bin/bash\necho hello", "text/plain")}
        res_invalid = self.client.post(f"/api/products/{prod_id}/upload-image", files=invalid_file)
        self.assertEqual(res_invalid.status_code, 400)
        self.assertIn("Unsupported file format", res_invalid.json()["detail"])

    def test_03_json_image_upload_and_marketplace_order_guards(self):
        """Web clients may submit an already-captured image URL; only published items can receive orders."""
        created = self.client.post("/api/products", json={"title": "Browser upload compatibility test"})
        self.assertEqual(created.status_code, 201)
        product_id = created.json()["id"]

        uploaded = self.client.post(
            f"/api/products/{product_id}/upload-image",
            json={"image_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="},
        )
        self.assertEqual(uploaded.status_code, 200)
        self.assertEqual(
            uploaded.json()["image_url"],
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=",
        )

        order_payload = {
            "product_id": product_id,
            "buyer_name": "Compatibility Buyer",
            "buyer_contact": "buyer@example.test",
            "quantity": 25,
        }
        self.assertEqual(self.client.post("/api/orders/request", json=order_payload).status_code, 409)

        processed = self.client.post(
            f"/api/products/{product_id}/process",
            json={"audio_transcript": "Bamboo basket made in two days."},
        )
        self.assertEqual(processed.status_code, 200)
        self.assertEqual(processed.json()["status"], "ready")
        self.assertIn("breakdown", processed.json()["product"])
        self.assertIn("reason", processed.json()["product"])

        self.assertEqual(self.client.patch(f"/api/products/{product_id}/publish").status_code, 200)
        order = self.client.post("/api/orders/request", json=order_payload)
        self.assertEqual(order.status_code, 201)

        updated = self.client.patch(f"/api/orders/{order.json()['id']}/status", json={"status": "accepted"})
        self.assertEqual(updated.status_code, 200)
        self.assertEqual(updated.json()["status"], "accepted")

        invalid_status = self.client.patch(f"/api/orders/{order.json()['id']}/status?new_status=unknown")
        self.assertEqual(invalid_status.status_code, 422)

        invalid_quantity = self.client.post(
            "/api/orders/request",
            json={**order_payload, "quantity": 0},
        )
        self.assertEqual(invalid_quantity.status_code, 422)

    def test_04_upload_content_and_size_validation(self):
        created = self.client.post("/api/products", json={"title": "Upload validation test"})
        product_id = created.json()["id"]

        invalid_signature = {"file": ("photo.png", b"not-a-png", "image/png")}
        rejected = self.client.post(f"/api/products/{product_id}/upload-image", files=invalid_signature)
        self.assertEqual(rejected.status_code, 400)
        self.assertIn("valid image", rejected.json()["detail"])

        mismatched_type = {"file": ("photo.png", b"\xff\xd8\xff\x00", "image/jpeg")}
        rejected_type = self.client.post(f"/api/products/{product_id}/upload-image", files=mismatched_type)
        self.assertEqual(rejected_type.status_code, 400)
        self.assertIn("extension and MIME", rejected_type.json()["detail"])

    def test_05_invalid_state_transitions_and_public_filtering(self):
        created = self.client.post("/api/products", json={"title": "State validation test"})
        product_id = created.json()["id"]
        self.assertEqual(self.client.patch(f"/api/products/{product_id}/publish").status_code, 409)
        self.assertEqual(
            self.client.put(f"/api/products/{product_id}", json={"status": "published"}).status_code,
            409,
        )

        self.assertEqual(self.client.get("/api/buyer/products?include_all=true").status_code, 200)
        buyer_ids = [product["id"] for product in self.client.get("/api/buyer/products?include_all=true").json()]
        self.assertNotIn(product_id, buyer_ids)

    def test_06_mock_results_are_labelled(self):
        pricing = self.client.post("/api/pricing/estimate", json={"category": "Bamboo", "material": "Bamboo"})
        self.assertEqual(pricing.status_code, 200)
        self.assertEqual(pricing.json()["ai_mode"]["mode"], "mock")
        self.assertTrue(pricing.json()["ai_mode"]["is_simulated"])

    def test_07_partial_failure_resilience(self):
        """
        Verifies AI pipeline does not crash when partial steps experience warnings/errors.
        """
        voice_input = "Handmade clay lamp"
        result = ProductPipelineOrchestrator.process_product_pipeline(
            product_id="new",
            audio_transcript=voice_input,
            raw_material_cost=150.0
        )
        self.assertIn("status", result)
        self.assertIn("product", result)
        self.assertEqual(result["status"], "ready")

    def test_08_nlp_notes_and_pricing_inputs_persist(self):
        """Verify M and S inputs are carried through A's product lifecycle endpoints."""
        created = self.client.post("/api/products", json={"title": "Integration inputs test"})
        self.assertEqual(created.status_code, 201)
        product_id = created.json()["id"]

        voice = self.client.post(
            f"/api/products/{product_id}/voice",
            json={"audio_transcript": "Bamboo basket takes 3 days and measures 30cm x 20cm.", "language": "en"},
        )
        self.assertEqual(voice.status_code, 200)
        self.assertEqual(voice.json()["production_time"], "3 days")
        self.assertEqual(voice.json()["dimensions"], "30cm x 20cm")

        catalogue = self.client.post(
            f"/api/products/{product_id}/generate-catalogue",
            json={"raw_notes": "Learned this weaving from my grandmother."},
        )
        self.assertEqual(catalogue.status_code, 200)
        self.assertIn("grandmother", catalogue.json()["description_english"].lower())

        pricing = self.client.post(
            f"/api/products/{product_id}/price",
            json={"raw_material_cost": 200, "labor_hours": 20},
        )
        self.assertEqual(pricing.status_code, 200)
        self.assertGreater(pricing.json()["suggested_price_min"], 0)
        self.assertGreaterEqual(pricing.json()["suggested_price_max"], pricing.json()["suggested_price_min"])

        invalid_pricing = self.client.post(
            f"/api/products/{product_id}/price",
            json={"raw_material_cost": -1, "labor_hours": -1},
        )
        self.assertEqual(invalid_pricing.status_code, 422)


if __name__ == "__main__":
    unittest.main()

