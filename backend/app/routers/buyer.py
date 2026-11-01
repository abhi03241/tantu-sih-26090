from typing import List, Optional
from fastapi import APIRouter, Query, status, HTTPException
from backend.app.schemas import ProductResponse, BuyerBase, BuyerResponse, PublicBuyerProfileResponse
from backend.app.database import ProductRepository, BuyerRepository, UserRepository

router = APIRouter(prefix="/api/buyer", tags=["Buyer Marketplace Feed"])


@router.get("/products", response_model=List[ProductResponse])
def get_buyer_products(
    category: Optional[str] = Query(None, description="Filter products by artisan category"),
    q: Optional[str] = Query(None, description="Search query across product titles and heritage stories"),
    include_all: bool = Query(False, description="Deprecated compatibility parameter; public feed remains published-only")
):
    """
    GET /api/buyer/products
    Retrieves published marketplace product feed tailored for urban B2B and retail buyers.
    Integrated with Team Member P's buyer UI and Team Member S's B2B marketplace feed.
    """
    # This is a public marketplace boundary. Keep the legacy query parameter
    # accepted for client compatibility, but never let it expose private drafts.
    products = ProductRepository.get_all(category=category, query=q, status="published")
    return products



@router.get("/profile/{buyer_id}", response_model=PublicBuyerProfileResponse)
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
        "buyer_type": "B2B Retailer"
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

