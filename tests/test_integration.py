"""
End-to-End Integration Demo Test for TANTU Backend Pipeline (Prompt #2 Requirement #10)
Verifies: Photo + Voice -> NLP Service -> Vision Service -> Pricing Engine -> Complete Product.
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

    def test_01_full_orchestrator_pipeline_via_service(self):
        """
        Direct Orchestrator Python Service Test with SIH Prompt #2 Demo Input.
        """
        voice_input = "Ye bamboo ki tokri hai. Isko banane mein do din lagte hain. Meri maa ne mujhe ye banana sikhaya tha."
        image_input = "https://images.unsplash.com/photo-1590736969955-71cc94801759"
        raw_cost = 250.0

        product = ProductPipelineOrchestrator.process_product_pipeline(
            product_id="new",
            audio_transcript=voice_input,
            image_url=image_input,
            raw_material_cost=raw_cost,
            language="hi"
        )

        # Assertions proving complete integration
        self.assertIsNotNone(product.get("id"))
        self.assertIsNotNone(product.get("material"))
        self.assertIsNotNone(product.get("description_english"))

        self.assertIsNotNone(product.get("description_hindi"))
        self.assertIsNotNone(product.get("story"))
        self.assertIsNotNone(product.get("enhanced_image_url"))
        self.assertGreater(product.get("suggested_price_min", 0), 0)
        self.assertGreater(product.get("suggested_price_max", 0), product.get("suggested_price_min", 0))

    def test_02_full_orchestrator_pipeline_via_rest_api(self):
        """
        REST API Orchestrator Endpoint Test: POST /api/products/new/process
        """
        payload = {
            "audio_transcript": "Ye bamboo ki tokri hai. Isko banane mein do din lagte hain. Meri maa ne mujhe ye banana sikhaya tha.",
            "image_url": "https://images.unsplash.com/photo-1590736969955-71cc94801759",
            "raw_material_cost": 250.0,
            "language": "hi",
            "artisan_id": "art-001"
        }

        res = self.client.post("/api/products/new/process", json=payload)
        self.assertEqual(res.status_code, 200)

        data = res.json()
        self.assertIn("id", data)
        self.assertIsNotNone(data["description_english"])
        self.assertIsNotNone(data["description_hindi"])
        self.assertIsNotNone(data["enhanced_image_url"])
        self.assertIsNotNone(data["suggested_price_min"])
        self.assertIsNotNone(data["suggested_price_max"])


if __name__ == "__main__":
    unittest.main()
