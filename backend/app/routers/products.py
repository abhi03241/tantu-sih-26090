import os
import uuid
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Request, status
from pydantic import ValidationError
from backend.app.schemas import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
    ProductStatusResponse,
    ImageUrlUploadRequest,
)
from backend.app.database import ProductRepository

router = APIRouter(prefix="/api/products", tags=["Products"])

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
UPLOADS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads"))


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    """
    Creates a new product record in 'draft' status using the Common Product Contract schema.
    """
    product_dict = product.model_dump()
    product_dict["id"] = f"prod-{uuid.uuid4().hex[:8]}"
    if not product_dict.get("status"):
        product_dict["status"] = "draft"
    
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
    status: Optional[str] = Query(None, description="Filter products by status (draft, processing, ready, published, failed)")
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


@router.get("/{id}/status", response_model=ProductStatusResponse)
def get_product_status(id: str):
    """
    GET /api/products/{id}/status
    Retrieves current processing status of a product (draft, processing, ready, published, failed).
    """
    product = ProductRepository.get_by_id(id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID '{id}' not found"
        )
    return {"id": product["id"], "status": product.get("status", "draft")}


@router.post("/{id}/upload-image", response_model=ProductResponse)
async def upload_product_image(id: str, request: Request):
    """
    POST /api/products/{id}/upload-image
    Uploads a product photograph locally (JPG, JPEG, PNG, WEBP), or accepts an
    already available image/data URL from web clients. Both forms update
    ``image_url`` on the product record.
    """
    product = ProductRepository.get_by_id(id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID '{id}' not found"
        )

    content_type = request.headers.get("content-type", "").lower()
    if not content_type.startswith("multipart/form-data"):
        try:
            payload = ImageUrlUploadRequest.model_validate(await request.json())
        except (ValidationError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Provide multipart field 'file' or a JSON body with a non-empty 'image_url'."
            )
        product["image_url"] = payload.image_url
        return ProductRepository.save(product)

    form = await request.form()
    file = form.get("file")
    if file is None or not getattr(file, "filename", None):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Multipart requests require a 'file' field."
        )

    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format '{ext}'. Allowed image types: JPG, JPEG, PNG, WEBP."
        )

    os.makedirs(UPLOADS_DIR, exist_ok=True)
    saved_filename = f"{id}_{uuid.uuid4().hex[:6]}{ext}"
    saved_path = os.path.join(UPLOADS_DIR, saved_filename)

    content = await file.read()
    with open(saved_path, "wb") as f:
        f.write(content)

    # Local URL reference
    image_url = f"/uploads/{saved_filename}"
    product["image_url"] = image_url
    updated = ProductRepository.save(product)
    return updated


@router.put("/{id}", response_model=ProductResponse)
def update_product(id: str, payload: ProductUpdate):
    """
    Updates existing product attributes (title, descriptions, category, material, tags, story, etc.).
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


@router.patch("/{id}/publish", response_model=ProductResponse)
def publish_product(id: str):
    """
    PATCH /api/products/{id}/publish
    Publishes a product (transitions status from draft/ready -> published).
    Makes the product visible on buyer marketplace feeds.
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


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_product(id: str):
    """
    Deletes a product listing by ID.
    """
    existing = ProductRepository.get_by_id(id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID '{id}' not found"
        )
    ProductRepository.delete(id)
    return {"status": "success", "message": f"Product '{id}' deleted successfully"}

