from typing import List, Optional
from fastapi import APIRouter, Query, status, HTTPException
from backend.app.schemas import ProductResponse, BuyerBase, BuyerResponse
from backend.app.database import ProductRepository, BuyerRepository, UserRepository

router = APIRouter(prefix="/api/buyer", tags=["Buyer Marketplace Feed"])


@router.get("/products", response_model=List[ProductResponse])
def get_buyer_products(
    category: Optional[str] = Query(None, description="Filter products by artisan category"),
    q: Optional[str] = Query(None, description="Search query across product titles and heritage stories"),
    include_all: bool = Query(False, description="Set to true to include draft/unpublished products for testing")
):
    """
    GET /api/buyer/products
    Retrieves published marketplace product feed tailored for urban B2B and retail buyers.
    Integrated with Team Member P's buyer UI and Team Member S's B2B marketplace feed.
    """
    prod_status = None if include_all else "published"
    products = ProductRepository.get_all(category=category, query=q, status=prod_status)
    return products



@router.get("/profile/{buyer_id}", response_model=BuyerResponse)
def get_buyer_profile(buyer_id: str):
    """
    GET /api/buyer/profile/{buyer_id}
    Retrieves buyer organization profile details.
    """
    buyer = BuyerRepository.get_by_id(buyer_id)
    if buyer:
        return buyer
    return {
        "id": f"buyer-{buyer_id}",
        "user_id": buyer_id,
        "buyer_name": "FabIndia Procurement Team",
        "organization": "FabIndia Overseas Pvt Ltd",
        "buyer_type": "B2B Retailer",
        "contact_email": "procurement@fabindia.com"
    }


@router.post("/profile", response_model=BuyerResponse, status_code=status.HTTP_201_CREATED)
def create_or_update_buyer_profile(buyer: BuyerBase):
    """
    POST /api/buyer/profile
    Registers or updates a buyer entity profile in the database.
    """
    buyer_dict = buyer.model_dump()
    if not buyer_dict.get("id"):
        buyer_dict["id"] = f"buyer-{buyer.user_id}"

    # Auto sync user record
    UserRepository.save({
        "id": buyer.user_id,
        "name": buyer.buyer_name,
        "phone": "",
        "role": "buyer",
        "region": buyer.organization or "India"
    })

    saved = BuyerRepository.save(buyer_dict)
    return saved

