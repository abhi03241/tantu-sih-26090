import uuid
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from backend.app.schemas import ProductCreate, ProductResponse, ProductUpdate, ProductStatusResponse
from backend.app.database import ProductRepository

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    """
    Creates a new product record using the Common Product Contract schema.
    """
    product_dict = product.model_dump()
    product_dict["id"] = f"prod-{uuid.uuid4().hex[:8]}"
    
    # Auto-fill fallback pricing if not provided
    if not product_dict.get("suggested_price_min"):
        product_dict["suggested_price_min"] = 500.0
        product_dict["suggested_price_max"] = 1000.0

    saved = ProductRepository.save(product_dict)
    return saved


@router.get("", response_model=List[ProductResponse])
def list_products(
    category: Optional[str] = Query(None, description="Filter products by category"),
    artisan_id: Optional[str] = Query(None, description="Filter products by artisan ID"),
    q: Optional[str] = Query(None, description="Search query across title, description, material"),
    status: Optional[str] = Query(None, description="Filter products by status (draft, processing, ready, published)")
):
    """
    Retrieves all product listings with optional category, artisan, status, and search filtering.
    """
    products = ProductRepository.get_all(category=category, artisan_id=artisan_id, query=q, status=status)
    return products


@router.get("/{id}", response_model=ProductResponse)
def get_product(id: str):
    """
    Retrieves a single product by its unique product ID.
    """
    product = ProductRepository.get_by_id(id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID '{id}' not found"
        )
    return product


@router.put("/{id}", response_model=ProductResponse)
def update_product(id: str, payload: ProductUpdate):
    """
    Updates existing product attributes.
    """
    existing = ProductRepository.get_by_id(id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID '{id}' not found"
        )
    
    update_data = payload.model_dump(exclude_unset=True)
    for key, val in update_data.items():
        if val is not None:
            existing[key] = val

    updated = ProductRepository.save(existing)
    return updated


@router.get("/{id}/status", response_model=ProductStatusResponse)
def get_product_status(id: str):
    """
    GET /api/products/{id}/status
    Retrieves current processing/publication status of a product (draft, processing, ready, published).
    """
    product = ProductRepository.get_by_id(id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID '{id}' not found"
        )
    return {"id": product["id"], "status": product.get("status") or "published"}


@router.patch("/{id}/publish", response_model=ProductResponse)
def publish_product(id: str):
    """
    PATCH /api/products/{id}/publish
    Publishes a product (transitions status from draft/ready -> published).
    Makes the product visible on buyer marketplace feeds and open for bulk orders.
    """
    existing = ProductRepository.get_by_id(id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID '{id}' not found"
        )

    existing["status"] = "published"
    published = ProductRepository.save(existing)
    return published
