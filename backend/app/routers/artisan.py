import uuid
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from backend.app.schemas import ProductResponse, ArtisanProfileBase, ArtisanProfileResponse
from backend.app.database import ProductRepository, ArtisanProfileRepository, UserRepository

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
    profile = ArtisanProfileRepository.get_by_id(artisan_id)
    if profile:
        return profile

    # Default fallback for demo resilience
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


@router.post("/profile", response_model=ArtisanProfileResponse, status_code=status.HTTP_201_CREATED)
def create_or_update_artisan_profile(profile: ArtisanProfileBase):
    """
    POST /api/artisan/profile
    Creates or updates an artisan profile in the database.
    """
    profile_dict = profile.model_dump()
    if not profile_dict.get("id"):
        profile_dict["id"] = f"prof-{profile.user_id}"

    # Auto sync user record
    UserRepository.save({
        "id": profile.user_id,
        "name": profile.artisan_name,
        "phone": profile.phone or "",
        "role": "artisan",
        "region": profile.location
    })

    saved = ArtisanProfileRepository.save(profile_dict)
    return saved

