"""
Vision Service Layer for TANTU Backend
Abstracts Team Member R's AI Vision and Image Enhancement module.
"""
import logging
import os
from typing import Dict, Any, Optional
from backend.app.config import settings
from ai.vision.image_enhancer import enhance_artisan_image

logger = logging.getLogger("tantu.vision_service")


class VisionService:
    """
    Orchestrates Computer Vision operations: background noise removal, studio lighting,
    and high-resolution upscaling for catalog images.
    """

    @classmethod
    def enhance_image(cls, image_url: Optional[str], prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Enhances raw product photo into professional studio-grade catalog display image.
        """
        source_image = image_url
        # The API stores uploaded files as browser-renderable `/uploads/...` URLs,
        # whereas R's real pipeline needs an actual local file path.
        if image_url and image_url.startswith("/uploads/"):
            filename = os.path.basename(image_url)
            candidate = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads", filename))
            if os.path.isfile(candidate):
                source_image = candidate

        try:
            result = enhance_artisan_image(
                image_url=source_image,
                prompt=prompt,
                mock=settings.MOCK_AI
            )
            return result
        except Exception as e:
            logger.error(f"[VisionService] Error enhancing image: {e}. Falling back to mock Vision enhancement.")
            return enhance_artisan_image(image_url=source_image, prompt=prompt, mock=True)
