"""
Vision Service Layer for TANTU Backend
Abstracts Team Member R's AI Vision and Image Enhancement module.
"""
import logging
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
        try:
            result = enhance_artisan_image(
                image_url=image_url,
                prompt=prompt,
                mock=settings.MOCK_AI
            )
            return result
        except Exception as e:
            logger.error(f"[VisionService] Error enhancing image: {e}. Falling back to mock Vision enhancement.")
            return enhance_artisan_image(image_url=image_url, prompt=prompt, mock=True)
