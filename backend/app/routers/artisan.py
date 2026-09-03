from typing import List, Optional
from fastapi import APIRouter, Query
from backend.app.schemas import ProductResponse, ArtisanProfileResponse
from backend.app.database import ProductRepository

router = APIRouter(prefix="/api/artisan", tags=["Artisan Dashboard"])


@router.get("/products", response_model=List[ProductResponse])
def get_artisan_products(
    artisan_id: Optional[str] = Query("art-001", description="Artisan ID (defaults to demo artisan art-001)")
):
    """
    GET /api/artisan/products
    Retrieves list of products cataloged by a specific artisan.
    Used by Team Member P's mobile app for the Artisan Dashboard catalog view.
    """
    products = ProductRepository.get_all(artisan_id=artisan_id)
    return products


@router.get("/profile/{artisan_id}", response_model=ArtisanProfileResponse)
def get_artisan_profile(artisan_id: str):
    """
    GET /api/artisan/profile/{artisan_id}
    Retrieves artisan profile details and regional heritage credentials.
    """
    return {
        "id": f"prof-{artisan_id}",
        "user_id": artisan_id,
        "artisan_name": "Lakshmi Devi",
        "craft_type": "Bamboo & Natural Fiber Crafting",
        "location": "Silchar, Cachar District, Assam",
        "bio": "Master artisan with 20+ years of experience crafting eco-friendly bamboo items.",
        "phone": "+91-9876543210",
        "story_style": "Cultural Heritage"
    }
