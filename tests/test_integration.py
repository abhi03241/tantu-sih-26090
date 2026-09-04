"""
End-to-End Integration Demo Test for TANTU Backend Artisan Processing Flow (Prompt #3)
Verifies: Create -> Upload Image -> Voice Input -> AI Processing -> Catalogue Edit -> Publish -> Buyer Retrieval.
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
        img_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4"
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

    def test_03_partial_failure_resilience(self):
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


if __name__ == "__main__":
    unittest.main()
