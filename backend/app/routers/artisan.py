from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from backend.app.schemas import ProductResponse, ArtisanProfileBase, ArtisanProfileResponse
from backend.app.database import ProductRepository, ArtisanRepository

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


@router.get("/profiles", response_model=List[ArtisanProfileResponse])
def list_artisan_profiles():
    """
    GET /api/artisan/profiles
    Retrieves all registered artisan profiles.
    """
    profiles = ArtisanRepository.get_all()
    return profiles


@router.get("/profile/{artisan_id}", response_model=ArtisanProfileResponse)
def get_artisan_profile(artisan_id: str):
    """
    GET /api/artisan/profile/{artisan_id}
    Retrieves artisan profile details and regional heritage credentials.
    """
    profile = ArtisanRepository.get_by_id(artisan_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Artisan profile with ID '{artisan_id}' not found"
        )
    return profile


@router.post("/profile", response_model=ArtisanProfileResponse, status_code=status.HTTP_201_CREATED)
def create_or_update_artisan_profile(profile: ArtisanProfileBase):
    """
    POST /api/artisan/profile
    Registers or updates an artisan's profile.
    """
    saved = ArtisanRepository.save(profile.model_dump())
    return saved
