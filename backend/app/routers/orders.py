import uuid
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from backend.app.schemas import OrderRequestCreate, OrderRequestResponse, OrderStatusUpdate
from backend.app.database import OrderRepository, ProductRepository

router = APIRouter(prefix="/api/orders", tags=["Order Requests (B2B Linkage)"])


@router.post("/request", response_model=OrderRequestResponse, status_code=status.HTTP_201_CREATED)
def create_order_request(order: OrderRequestCreate):
    """
    POST /api/orders/request
    Submits a bulk B2B purchase or direct buyer order request to an artisan.
    """
    if order.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Order quantity must be greater than zero."
        )

    product = ProductRepository.get_by_id(order.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID '{order.product_id}' not found"
        )

    order_dict = order.model_dump()
    order_dict["id"] = f"ord-{uuid.uuid4().hex[:8]}"
    order_dict["product_title"] = product.get("title", "Artisan Product")
    order_dict["artisan_id"] = product.get("artisan_id", "art-001")
    order_dict["status"] = "pending"

    # Synchronize message and notes
    msg = order_dict.get("message") or order_dict.get("notes") or ""
    order_dict["message"] = msg
    order_dict["notes"] = msg

    saved = OrderRepository.save(order_dict)
    return saved


@router.get("", response_model=List[OrderRequestResponse])
def list_orders(
    product_id: Optional[str] = Query(None, description="Filter orders by product ID"),
    artisan_id: Optional[str] = Query(None, description="Filter orders by artisan ID")
):
    """
    GET /api/orders
    Lists order requests submitted by buyers to artisans.
    """
    orders = OrderRepository.get_all(product_id=product_id, artisan_id=artisan_id)
    return orders


@router.get("/{id}", response_model=OrderRequestResponse)
def get_order_by_id(id: str):
    """
    GET /api/orders/{id}
    Retrieves a single order request by its unique ID.
    """
    order = OrderRepository.get_by_id(id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID '{id}' not found"
        )
    return order


@router.patch("/{id}/status", response_model=OrderRequestResponse)
def update_order_status(id: str, status_update: OrderStatusUpdate):
    """
    PATCH /api/orders/{id}/status
    Updates the status of a B2B order request (pending, accepted, rejected).
    """
    allowed_statuses = ["pending", "accepted", "rejected"]
    new_status = status_update.status.lower().strip()
    if new_status not in allowed_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status '{status_update.status}'. Must be one of: {allowed_statuses}"
        )

    existing = OrderRepository.get_by_id(id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID '{id}' not found"
        )

    updated = OrderRepository.update_status(id, new_status)
    return updated

