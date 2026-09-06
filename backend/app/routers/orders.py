import uuid
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from backend.app.schemas import OrderRequestCreate, OrderRequestResponse, OrderStatus, OrderStatusUpdateRequest
from backend.app.database import OrderRepository, ProductRepository

router = APIRouter(prefix="/api/orders", tags=["Order Requests (B2B Linkage)"])


@router.post("/request", response_model=OrderRequestResponse, status_code=status.HTTP_201_CREATED)
def create_order_request(order: OrderRequestCreate):
    """
    POST /api/orders/request
    Submits a bulk B2B purchase or direct buyer order request to an artisan.
    """
    product = ProductRepository.get_by_id(order.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID '{order.product_id}' not found"
        )
    if product.get("status") != "published":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Bulk orders can only be requested for published products"
        )

    order_dict = order.model_dump()
    order_dict["id"] = f"ord-{uuid.uuid4().hex[:8]}"
    order_dict["product_title"] = product.get("title", "Artisan Product")
    order_dict["artisan_id"] = product.get("artisan_id", "art-001")
    order_dict["status"] = "pending"

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
def get_order(id: str):
    """
    GET /api/orders/{id}
    Retrieves single order request by ID.
    """
    order = OrderRepository.get_by_id(id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID '{id}' not found"
        )
    return order


@router.patch("/{id}/status", response_model=OrderRequestResponse)
def update_order_status(
    id: str,
    new_status: Optional[OrderStatus] = Query(None, description="New status: pending, accepted, fulfilled, rejected"),
    payload: Optional[OrderStatusUpdateRequest] = None,
):
    """
    PATCH /api/orders/{id}/status
    Updates order request status (e.g. accepted by artisan, fulfilled, rejected).
    """
    existing = OrderRepository.get_by_id(id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID '{id}' not found"
        )

    requested_status = payload.status if payload else new_status
    if requested_status is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Provide a valid status in JSON body or as the 'new_status' query parameter"
        )

    updated = OrderRepository.update_status(id, requested_status)
    return updated
