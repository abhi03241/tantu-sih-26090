from typing import List, Optional
from fastapi import APIRouter, Query
from backend.app.schemas import ProductResponse
from backend.app.database import ProductRepository

router = APIRouter(prefix="/api/buyer", tags=["Buyer Marketplace Feed"])


@router.get("/products", response_model=List[ProductResponse])
def get_buyer_products(
    category: Optional[str] = Query(None, description="Filter products by artisan category"),
    q: Optional[str] = Query(None, description="Search query across product titles and heritage stories"),
    include_all: bool = Query(False, description="Set to true to include draft/unpublished products for testing")
):
    """
    GET /api/buyer/products
    Retrieves marketplace product feed tailored for urban B2B and retail buyers.
    Integrated with Team Member P's buyer UI and Team Member S's B2B marketplace feed.
    """
    prod_status = None if include_all else "published"
    products = ProductRepository.get_all(category=category, query=q, status=prod_status)
    return products
