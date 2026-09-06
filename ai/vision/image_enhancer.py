"""
AI Vision & Image Enhancement Module
Maintained by Team Member R (AI Image Enhancement)
Integrated into TANTU Backend core workflow.

Transforms raw artisan phone photos into professional studio-grade catalog photos.
Removes clutter, adjusts lighting, centers product, and enhances color contrast for high buyer conversion.
"""

import os
from typing import Dict, Any, Optional, Union
from ai.vision.services import (
    BaseImageService,
    RealImageService,
    MockImageService,
    get_image_enhancement_service,
)
from ai.vision.pipeline import (
    ImagePipeline,
    ImageValidationError,
    validate_image_bytes,
    DEFAULT_TARGET_SIZE,
    SUPPORTED_FORMATS
)

# Export alias for convenience
ImageEnhancementService = get_image_enhancement_service


def enhance_artisan_image(
    image_url: str,
    prompt: Optional[str] = None,
    mock: Optional[bool] = None,
    output_dir: Optional[str] = None
) -> Dict[str, Any]:
    """
    Main entry point for TANTU artisan photo enhancement.

    Parameters:
    - image_url: URL or local filepath to artisan's photograph.
    - prompt: Optional studio lighting/backdrop description (e.g., 'Warm studio lighting').
    - mock: If True, uses instant high-res mock response. If False, runs real local CV pipeline.
            If None, defaults to MOCK_AI environment variable.
    - output_dir: Optional directory to store enhanced images.

    Returns:
    Standardized dictionary conforming to TANTU API contract.
    """
    if mock is None:
        mock = os.getenv("MOCK_AI", "true").lower() == "true"

    service = get_image_enhancement_service(mock=mock)
    result = service.enhance_image(image_input=image_url, prompt=prompt, output_dir=output_dir)

    # Fallback safety: If real mode failed (e.g. invalid URL during demo), fallback gracefully to mock
    if result.get("status") == "error" and not mock:
        fallback_service = MockImageService()
        fallback_result = fallback_service.enhance_image(image_input=image_url, prompt=prompt, output_dir=output_dir)
        fallback_result["warning"] = f"Real pipeline encountered an issue ({result.get('error')}); recovered via mock studio."
        return fallback_result

    return result
