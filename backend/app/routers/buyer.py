from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from backend.app.schemas import ProductResponse, BuyerBase, BuyerResponse
from backend.app.database import ProductRepository, BuyerRepository

router = APIRouter(prefix="/api/buyer", tags=["Buyer Marketplace Feed"])


@router.get("/products", response_model=List[ProductResponse])
def get_buyer_products(
    category: Optional[str] = Query(None, description="Filter products by artisan category"),
    q: Optional[str] = Query(None, description="Search query across product titles and heritage stories")
):
    """
    GET /api/buyer/products
    Retrieves marketplace product feed tailored for urban B2B and retail buyers.
    Integrated with Team Member P's buyer UI and Team Member S's B2B marketplace feed.
    """
    products = ProductRepository.get_all(category=category, query=q)
    return products


@router.get("/profiles", response_model=List[BuyerResponse])
def list_buyer_profiles():
    """
    GET /api/buyer/profiles
    Retrieves all registered institutional and B2B buyers.
    """
    buyers = BuyerRepository.get_all()
    return buyers


@router.get("/profile/{buyer_id}", response_model=BuyerResponse)
def get_buyer_profile(buyer_id: str):
    """
    GET /api/buyer/profile/{buyer_id}
    Retrieves specific buyer organization details.
    """
    buyer = BuyerRepository.get_by_id(buyer_id)
    if not buyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Buyer with ID '{buyer_id}' not found"
        )
    return buyer


@router.post("/profile", response_model=BuyerResponse, status_code=status.HTTP_201_CREATED)
def create_or_update_buyer_profile(buyer: BuyerBase):
    """
    POST /api/buyer/profile
    Registers or updates a buyer organization profile.
    """
    saved = BuyerRepository.save(buyer.model_dump())
    return saved
