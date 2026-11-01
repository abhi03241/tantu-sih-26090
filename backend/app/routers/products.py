import base64
import binascii
import io
import os
import uuid
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Request, status
from pydantic import ValidationError
from PIL import Image, UnidentifiedImageError
from backend.app.schemas import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
    ProductStatusResponse,
    ImageUrlUploadRequest,
)
from backend.app.database import ProductRepository
from backend.app.config import settings

router = APIRouter(prefix="/api/products", tags=["Products"])

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_IMAGE_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_UPLOAD_BYTES = 10 * 1024 * 1024
UPLOADS_DIR = os.path.abspath(settings.UPLOADS_DIR)


def _validate_image_content(content: bytes, content_type: str, extension: str) -> None:
    """Validate size, declared type, and file signature before persistence."""
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded image is empty.")
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="Uploaded image exceeds the 10 MiB limit.")

    normalized_type = content_type.split(";", 1)[0].strip().lower()
    expected_types = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}
    if normalized_type not in ALLOWED_IMAGE_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported image MIME type.")
    if normalized_type != expected_types[extension]:
        raise HTTPException(status_code=400, detail="Image extension and MIME type do not match.")

    signatures = {
        ".jpg": lambda value: value.startswith(b"\xff\xd8\xff"),
        ".jpeg": lambda value: value.startswith(b"\xff\xd8\xff"),
        ".png": lambda value: value.startswith(b"\x89PNG\r\n\x1a\n"),
        ".webp": lambda value: len(value) >= 12 and value[:4] == b"RIFF" and value[8:12] == b"WEBP",
    }
    if not signatures[extension](content):
        raise HTTPException(status_code=400, detail="Uploaded content is not a valid image of the declared type.")

    try:
        with Image.open(io.BytesIO(content)) as image:
            image.verify()
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=f"Uploaded image cannot be decoded: {exc}")


def _validate_image_url(image_url: str) -> str:
    """Keep compatibility URLs bounded and limited to safe image schemes."""
    if len(image_url) > MAX_UPLOAD_BYTES * 2:
        raise HTTPException(status_code=413, detail="Image URL or data URL is too large.")
    if image_url.startswith(("https://", "http://")):
        return image_url
    if image_url.startswith("data:image/") and "," in image_url:
        header, encoded = image_url.split(",", 1)
        if not encoded:
            raise HTTPException(status_code=400, detail="Image data URL is empty.")
        try:
            decoded = base64.b64decode(encoded, validate=True)
        except (ValueError, binascii.Error):
            raise HTTPException(status_code=400, detail="Image data URL is not valid base64.")
        mime = header.split(";", 1)[0].lower()
        extension = {"data:image/jpeg": ".jpg", "data:image/png": ".png", "data:image/webp": ".webp"}.get(mime)
        if not extension:
            raise HTTPException(status_code=400, detail="Only JPEG, PNG, and WEBP images are supported.")
        _validate_image_content(decoded, mime.removeprefix("data:"), extension)
        return image_url
    raise HTTPException(status_code=400, detail="Image URL must use HTTP(S) or a validated image data URL.")


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    """
    Creates a new product record in 'draft' status using the Common Product Contract schema.
    """
    product_dict = product.model_dump()
    product_dict["id"] = f"prod-{uuid.uuid4().hex[:8]}"
    # New records always begin private; publishing is an explicit lifecycle action.
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
        product["image_url"] = _validate_image_url(payload.image_url)
        return ProductRepository.save(product)

    form = await request.form()
    file = form.get("file")
    if file is None or not getattr(file, "filename", None):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Multipart requests require a 'file' field."
        )

    filename = os.path.basename(file.filename)
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format '{ext}'. Allowed image types: JPG, JPEG, PNG, WEBP."
        )

    content_type = getattr(file, "content_type", "") or ""
    content = await file.read(MAX_UPLOAD_BYTES + 1)
    _validate_image_content(content, content_type, ext)

    os.makedirs(UPLOADS_DIR, exist_ok=True)
    saved_filename = f"{id}_{uuid.uuid4().hex[:6]}{ext}"
    saved_path = os.path.abspath(os.path.join(UPLOADS_DIR, saved_filename))
    if os.path.commonpath((UPLOADS_DIR, saved_path)) != UPLOADS_DIR:
        raise HTTPException(status_code=400, detail="Unsafe upload path.")

    try:
        with open(saved_path, "wb") as f:
            f.write(content)

        # Local URL reference
        image_url = f"/uploads/{saved_filename}"
        product["image_url"] = image_url
        return ProductRepository.save(product)
    except OSError:
        if os.path.exists(saved_path):
            os.remove(saved_path)
        raise HTTPException(status_code=500, detail="Unable to safely store the uploaded image.")


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

    try:
        updated = ProductRepository.save(existing)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
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
    try:
        published = ProductRepository.save(existing)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
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
