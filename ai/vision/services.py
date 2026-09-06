"""
Service Interface and Implementations for AI Vision Studio in TANTU.
Maintained by Team Member R (AI Image Enhancement).
"""

import abc
import base64
import hashlib
import io
import os
import urllib.request
from typing import Dict, Any, Optional, Union
from PIL import Image

from ai.vision.pipeline import (
    ImagePipeline,
    ImageValidationError,
    DEFAULT_TARGET_SIZE,
)


ENHANCED_IMAGE_ROUTE = "/enhanced"


class BaseImageService(abc.ABC):
    """
    Abstract Service Interface for image enhancement in TANTU.
    """

    @abc.abstractmethod
    def enhance_image(
        self,
        image_input: Union[str, bytes],
        prompt: Optional[str] = None,
        output_dir: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Enhances the input image (URL, local file path, or bytes)
        and returns a standardized response contract.
        """
        pass


class MockImageService(BaseImageService):
    """
    Fallback Mock Service:
    Provides fast, deterministic, high-quality responses for SIH demonstrations
    and when external connectivity is disabled or unavailable.
    """

    # High quality artisan product backdrop demo photos
    MOCK_ENHANCED_CATALOG_MAP = {
        "bamboo": "https://images.unsplash.com/photo-1590736969955-71cc94801759?auto=format&fit=crop&w=1200&q=90",
        "pottery": "https://images.unsplash.com/photo-1605379399642-870262d3d051?auto=format&fit=crop&w=1200&q=90",
        "textile": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=1200&q=90",
        "wood": "https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=1200&q=90",
        "default": "https://images.unsplash.com/photo-1590736969955-71cc94801759?auto=format&fit=crop&w=1200&q=90"
    }

    def enhance_image(
        self,
        image_input: Union[str, bytes],
        prompt: Optional[str] = None,
        output_dir: Optional[str] = None,
    ) -> Dict[str, Any]:
        image_url = image_input if isinstance(image_input, str) else "local_upload"
        
        # Select appropriate mock studio image or format URL
        if isinstance(image_input, str) and (image_input.startswith("http://") or image_input.startswith("https://")):
            if "enhanced" in image_input:
                enhanced_url = image_input
            elif "?" in image_input:
                enhanced_url = image_input + "&auto=format&fit=crop&w=1200&q=90"
            else:
                enhanced_url = image_input + "?auto=format&fit=crop&w=1200&q=90"
        else:
            # Match keyword if provided in prompt or path
            chosen = self.MOCK_ENHANCED_CATALOG_MAP["default"]
            check_str = f"{image_input} {prompt or ''}".lower()
            for kw, url in self.MOCK_ENHANCED_CATALOG_MAP.items():
                if kw in check_str:
                    chosen = url
                    break
            enhanced_url = chosen

        return {
            "original_image_url": image_url,
            "enhanced_image_url": enhanced_url,
            "status": "success",
            "mock_mode": True,
            "processing_steps": [
                "validated",
                "format_converted",
                "cropped",
                "lighting_enhanced",
                "background_cleaned",
                "resized"
            ],
            "enhancements_applied": [
                "Background clutter removal & studio lighting",
                "Studio light normalization",
                "Color vibrancy auto-correction",
                "High-resolution upscaling (2x)"
            ],
            "confidence_score": 0.96,
            "metadata": {
                "target_dimensions": list(DEFAULT_TARGET_SIZE),
                "aspect_ratio": "1:1",
                "prompt": prompt
            }
        }


class RealImageService(BaseImageService):
    """
    Production/Prototype Local Computer Vision Service:
    Applies the full image enhancement pipeline locally via PIL / computer vision algorithms.
    Saves the studio-grade output to static assets or returns data URLs / file paths.
    """

    def __init__(self, target_size=DEFAULT_TARGET_SIZE):
        self.pipeline = ImagePipeline(target_size=target_size)

    def _fetch_image_bytes(self, image_input: Union[str, bytes]) -> bytes:
        if isinstance(image_input, bytes):
            return image_input

        if not isinstance(image_input, str) or not image_input.strip():
            raise ImageValidationError("No image URL, file path, or bytes provided.")

        image_input_str = image_input.strip()

        # Check for Base64 Data URL
        if image_input_str.startswith("data:image/"):
            try:
                base64_data = image_input_str.split(",", 1)[1]
                return base64.b64decode(base64_data)
            except Exception as exc:
                raise ImageValidationError(f"Invalid base64 image data: {exc}")

        # Check for HTTP/HTTPS URL
        if image_input_str.startswith("http://") or image_input_str.startswith("https://"):
            try:
                req = urllib.request.Request(
                    image_input_str,
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) TANTU-AI/1.0"}
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    if resp.status != 200:
                        raise ImageValidationError(f"HTTP error {resp.status} fetching image from {image_input_str}")
                    return resp.read()
            except Exception as exc:
                raise ImageValidationError(f"Failed to fetch image from URL: {exc}")

        # Check for local file path
        if os.path.isfile(image_input_str):
            try:
                with open(image_input_str, "rb") as f:
                    return f.read()
            except Exception as exc:
                raise ImageValidationError(f"Failed to read local image file '{image_input_str}': {exc}")

        raise ImageValidationError(f"Image source not found or unreachable: {image_input_str}")

    def enhance_image(
        self,
        image_input: Union[str, bytes],
        prompt: Optional[str] = None,
        output_dir: Optional[str] = None,
    ) -> Dict[str, Any]:
        try:
            image_bytes = self._fetch_image_bytes(image_input)
            enhanced_pil, steps, metadata = self.pipeline.process(image_bytes)

            # Determine output destination
            orig_ref = image_input if isinstance(image_input, str) else "upload"
            # Hash all source bytes: two different camera files can share their
            # first kilobyte (headers/metadata), so hashing only that prefix can
            # overwrite an existing enhanced catalogue asset.
            input_hash = hashlib.sha256(image_bytes).hexdigest()[:16]
            filename = f"enhanced_studio_{input_hash}.jpg"

            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, filename)
                enhanced_pil.save(output_path, format="JPEG", quality=92, optimize=True)
                enhanced_url = output_path
            else:
                # If no output directory specified, save to default static / cache folder
                default_static = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "enhanced"))
                os.makedirs(default_static, exist_ok=True)
                output_path = os.path.join(default_static, filename)
                enhanced_pil.save(output_path, format="JPEG", quality=92, optimize=True)
                
                # The backend mounts this directory at /enhanced so API clients
                # receive a renderable URL rather than a server-local path.
                enhanced_url = f"{ENHANCED_IMAGE_ROUTE}/{filename}"

            metadata["output_file"] = output_path
            metadata["prompt"] = prompt

            return {
                "original_image_url": orig_ref,
                "enhanced_image_url": enhanced_url,
                "status": "success",
                "mock_mode": False,
                "processing_steps": steps,
                "enhancements_applied": [
                    "Background clutter removal & studio lighting",
                    "Dynamic contrast & exposure correction",
                    "Authentic handicraft texture sharpening",
                    f"Catalogue framing & resize ({DEFAULT_TARGET_SIZE[0]}x{DEFAULT_TARGET_SIZE[1]})"
                ],
                "confidence_score": 0.95,
                "metadata": metadata
            }

        except ImageValidationError as err:
            return {
                "original_image_url": image_input if isinstance(image_input, str) else "upload",
                "enhanced_image_url": None,
                "status": "error",
                "error": str(err),
                "processing_steps": [],
                "enhancements_applied": [],
                "confidence_score": 0.0
            }
        except Exception as exc:
            return {
                "original_image_url": image_input if isinstance(image_input, str) else "upload",
                "enhanced_image_url": None,
                "status": "error",
                "error": f"Internal image processing error: {exc}",
                "processing_steps": [],
                "enhancements_applied": [],
                "confidence_score": 0.0
            }


def get_image_enhancement_service(mock: Optional[bool] = None) -> BaseImageService:
    """
    Factory function to retrieve either MockImageService or RealImageService.
    Defaults to environment configuration if mock is not explicitly passed.
    """
    if mock is None:
        mock_env = os.getenv("MOCK_AI", "true").lower() == "true"
        mock = mock_env

    if mock:
        return MockImageService()
    return RealImageService()
