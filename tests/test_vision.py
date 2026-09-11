"""
Unit and Integration Tests for TANTU AI Vision Module.
Maintained by Team Member R (AI Image Enhancement).
"""

import base64
import io
import os
import sys
import tempfile
import unittest
from PIL import Image

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai.vision.pipeline import (
    ImagePipeline,
    ImageValidationError,
    validate_image_bytes,
    fix_exif_orientation,
    DEFAULT_TARGET_SIZE,
)
from ai.vision.services import (
    RealImageService,
    MockImageService,
    get_image_enhancement_service,
)
from ai.vision.image_enhancer import enhance_artisan_image
from backend.app.main import app
from backend.app.database import init_db, ProductRepository
from backend.app.seed_data import seed_demo_data
from fastapi.testclient import TestClient


class TestAIVisionModule(unittest.TestCase):

    def setUp(self):
        self.pipeline = ImagePipeline()
        self.real_service = RealImageService()
        self.mock_service = MockImageService()

    def _create_dummy_image_bytes(self, size=(300, 300), format="JPEG", color=(200, 150, 100)) -> bytes:
        img = Image.new("RGB", size, color)
        buf = io.BytesIO()
        img.save(buf, format=format)
        return buf.getvalue()

    def test_01_valid_jpeg(self):
        """Tests processing a valid JPEG artisan image."""
        jpg_bytes = self._create_dummy_image_bytes(size=(400, 300), format="JPEG")
        enhanced, steps, meta = self.pipeline.process(jpg_bytes)

        self.assertEqual(enhanced.size, DEFAULT_TARGET_SIZE)
        self.assertIn("validated", steps)
        self.assertIn("cropped", steps)
        self.assertIn("lighting_enhanced", steps)
        self.assertIn("background_cleaned", steps)
        self.assertIn("resized", steps)

    def test_02_valid_png(self):
        """Tests processing a valid PNG artisan image (with transparency/alpha)."""
        img = Image.new("RGBA", (500, 500), (180, 100, 60, 255))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        png_bytes = buf.getvalue()

        enhanced, steps, meta = self.pipeline.process(png_bytes)
        self.assertEqual(enhanced.size, DEFAULT_TARGET_SIZE)
        self.assertEqual(enhanced.mode, "RGB")
        self.assertIn("format_converted", steps)

    def test_03_invalid_corrupted_image(self):
        """Tests that corrupted/garbage bytes raise ImageValidationError."""
        corrupted_bytes = b"NOT_AN_IMAGE_RANDOM_TEXT_DATA_CORRUPTED"
        with self.assertRaises(ImageValidationError):
            validate_image_bytes(corrupted_bytes)

        # Service level should return status error, never crash
        res = self.real_service.enhance_image(corrupted_bytes)
        self.assertEqual(res["status"], "error")
        self.assertIn("error", res)

    def test_04_extremely_small_image(self):
        """Tests image below minimum allowed dimensions (<50x50)."""
        tiny_bytes = self._create_dummy_image_bytes(size=(20, 20), format="JPEG")
        with self.assertRaises(ImageValidationError):
            validate_image_bytes(tiny_bytes)

    def test_05_large_high_resolution_image(self):
        """Tests handling high resolution images (e.g. 3000x2000) properly."""
        large_bytes = self._create_dummy_image_bytes(size=(3000, 2000), format="JPEG")
        enhanced, steps, meta = self.pipeline.process(large_bytes)
        self.assertEqual(enhanced.size, DEFAULT_TARGET_SIZE)
        self.assertEqual(meta["original_size"], [3000, 2000])

    def test_06_unsupported_format(self):
        """Tests unsupported dummy format/data."""
        dummy_data = b"%PDF-1.4 dummy pdf data content here"
        with self.assertRaises(ImageValidationError):
            validate_image_bytes(dummy_data)

    def test_07_mock_image_service(self):
        """Tests mock service response contract and resilience."""
        res = self.mock_service.enhance_image(
            image_input="https://images.unsplash.com/photo-1590736969955-71cc94801759",
            prompt="Studio spotlight"
        )
        self.assertEqual(res["status"], "success")
        self.assertTrue(res["mock_mode"])
        self.assertIsNotNone(res["enhanced_image_url"])
        self.assertGreaterEqual(res["confidence_score"], 0.9)
        self.assertIn("validated", res["processing_steps"])

    def test_08_service_factory(self):
        """Tests dynamic service instantiation via factory."""
        mock_svc = get_image_enhancement_service(mock=True)
        self.assertIsInstance(mock_svc, MockImageService)

        real_svc = get_image_enhancement_service(mock=False)
        self.assertIsInstance(real_svc, RealImageService)

    def test_09_high_level_enhance_function(self):
        """Tests high-level enhance_artisan_image facade function."""
        # Using a sample image from samples dir
        samples_dir = os.path.join(os.path.dirname(__file__), "..", "ai", "vision", "samples")
        sample_path = os.path.join(samples_dir, "bamboo_basket.jpg")
        
        if os.path.exists(sample_path):
            res = enhance_artisan_image(image_url=sample_path, mock=False)
            self.assertEqual(res["status"], "success")
            self.assertIsNotNone(res["enhanced_image_url"])
            self.assertTrue(res["enhanced_image_url"].startswith("/enhanced/"))
            self.assertTrue(os.path.exists(res["metadata"]["output_file"]))

    def test_10_api_integration_endpoint(self):
        """Tests integration with FastAPI /api/products/{id}/enhance-image endpoint."""
        init_db()
        seed_demo_data()
        client = TestClient(app)

        # Get first seeded product
        res = client.get("/api/products")
        prod_id = res.json()[0]["id"]

        # Call enhance endpoint
        enhance_res = client.post(f"/api/products/{prod_id}/enhance-image", json={
            "image_url": "https://images.unsplash.com/photo-1590736969955-71cc94801759",
            "prompt": "Soft studio background"
        })

        self.assertEqual(enhance_res.status_code, 200)
        data = enhance_res.json()
        self.assertEqual(data["id"], prod_id)
        self.assertIsNotNone(data["enhanced_image_url"])

    def test_11_missing_or_empty_input(self):
        """Tests that empty or missing file inputs are handled safely without crashing."""
        res = self.real_service.enhance_image("")
        self.assertEqual(res["status"], "error")
        self.assertIn("error", res)

        res_none = self.real_service.enhance_image(None)
        self.assertEqual(res_none["status"], "error")

    def test_12_original_preservation(self):
        """Tests that the original input file is never modified or overwritten."""
        samples_dir = os.path.join(os.path.dirname(__file__), "..", "ai", "vision", "samples")
        sample_path = os.path.join(samples_dir, "bamboo_basket.jpg")
        
        if os.path.exists(sample_path):
            with open(sample_path, "rb") as f:
                orig_bytes_before = f.read()

            res = enhance_artisan_image(image_url=sample_path, mock=False)
            
            with open(sample_path, "rb") as f:
                orig_bytes_after = f.read()

            self.assertEqual(orig_bytes_before, orig_bytes_after, "Original image file was modified!")
            self.assertNotEqual(res["original_image_url"], res["enhanced_image_url"])

    def test_13_failure_handling_and_fallback(self):
        """Tests that invalid inputs trigger graceful fallback without crashing."""
        res = enhance_artisan_image(image_url="invalid_non_existent_file.xyz", mock=False)
        self.assertEqual(res["status"], "success")
        self.assertIn("warning", res)
        self.assertIsNotNone(res["enhanced_image_url"])

    def test_14_exif_orientation_is_normalized(self):
        """Phone-camera EXIF orientation is applied before catalogue cropping."""
        image = Image.new("RGB", (80, 160), (180, 120, 80))
        exif = Image.Exif()
        exif[274] = 6  # Rotate 90 degrees clockwise.
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", exif=exif)

        oriented = fix_exif_orientation(validate_image_bytes(buffer.getvalue()))
        self.assertEqual(oriented.size, (160, 80))

    def test_15_full_content_hash_prevents_output_collisions(self):
        """Files with matching headers still produce distinct enhanced assets."""
        first = Image.new("RGB", (100, 100), (100, 100, 100))
        second = first.copy()
        second.putpixel((0, 0), (101, 100, 100))
        first_buffer, second_buffer = io.BytesIO(), io.BytesIO()
        first.save(first_buffer, format="BMP")
        second.save(second_buffer, format="BMP")
        self.assertEqual(first_buffer.getvalue()[:1024], second_buffer.getvalue()[:1024])

        with tempfile.TemporaryDirectory() as output_dir:
            first_result = self.real_service.enhance_image(first_buffer.getvalue(), output_dir=output_dir)
            second_result = self.real_service.enhance_image(second_buffer.getvalue(), output_dir=output_dir)

        self.assertEqual(first_result["status"], "success")
        self.assertEqual(second_result["status"], "success")
        self.assertNotEqual(first_result["enhanced_image_url"], second_result["enhanced_image_url"])

    def test_16_mobile_camera_sized_jpeg(self):
        """A common 12 MP phone resolution remains within the supported limits."""
        camera_bytes = self._create_dummy_image_bytes(
            size=(4032, 3024), format="JPEG", color=(125, 95, 70)
        )
        enhanced, _, metadata = self.pipeline.process(camera_bytes)

        self.assertEqual(metadata["original_size"], [4032, 3024])
        self.assertEqual(enhanced.size, DEFAULT_TARGET_SIZE)

    def test_17_enhanced_asset_is_retrievable_from_static_route(self):
        """The relative enhanced URL returned to a mobile client resolves to JPEG bytes."""
        image_bytes = self._create_dummy_image_bytes(size=(400, 300), format="JPEG")
        result = self.real_service.enhance_image(image_bytes)

        self.assertEqual(result["status"], "success")
        self.assertTrue(result["enhanced_image_url"].startswith("/enhanced/"))

        response = TestClient(app).get(result["enhanced_image_url"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "image/jpeg")

    def test_18_mobile_base64_data_url_upload(self):
        """Frontend camera/gallery uploads encoded as base64 data URLs are correctly processed."""
        # Test JPEG base64 data URL
        jpeg_bytes = self._create_dummy_image_bytes(size=(600, 800), format="JPEG", color=(150, 100, 50))
        b64_jpeg_str = f"data:image/jpeg;base64,{base64.b64encode(jpeg_bytes).decode('utf-8')}"
        res_jpeg = self.real_service.enhance_image(b64_jpeg_str)
        self.assertEqual(res_jpeg["status"], "success")
        self.assertTrue(res_jpeg["enhanced_image_url"].startswith("/enhanced/"))
        self.assertEqual(res_jpeg["metadata"]["original_size"], [600, 800])
        self.assertEqual(res_jpeg["metadata"]["enhanced_size"], list(DEFAULT_TARGET_SIZE))

        # Test PNG base64 data URL
        img_png = Image.new("RGBA", (500, 500), (200, 120, 80, 255))
        buf_png = io.BytesIO()
        img_png.save(buf_png, format="PNG")
        b64_png_str = f"data:image/png;base64,{base64.b64encode(buf_png.getvalue()).decode('utf-8')}"
        res_png = self.real_service.enhance_image(b64_png_str)
        self.assertEqual(res_png["status"], "success")
        self.assertTrue(res_png["enhanced_image_url"].startswith("/enhanced/"))


if __name__ == "__main__":
    unittest.main()
