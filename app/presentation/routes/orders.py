from fastapi import APIRouter, Depends, HTTPException
from app.application.use_cases.orders import *
from app.infrastructure.db import get_db
from app.infrastructure.auth.auth_dependencies import get_current_user
from app.infrastructure.repositories.order_repository import *
from app.presentation.dto import *

router = APIRouter()

@router.post("/orders")
def create_order(order_dto: OrderCreateDTO, db=Depends(get_db), current_user: CurrentUserDTO = Depends(get_current_user)):
    order_repository = SQLAlchemyOrderRepository(db)
    product_repository = SQLAlchemyProductRepository(db)
    use_case = OrderUseCases(order_repository, product_repository)
    order = use_case.create(order_dto, int(current_user["user_id"]))

    return order

@router.get("/orders/{order_id}")
def get_order(order_id: int, db=Depends(get_db), current_user: CurrentUserDTO = Depends(get_current_user)):
    order_repository = SQLAlchemyOrderRepository(db)
    use_case = OrderUseCases(order_repository)
    order = use_case.get_order_by_id(order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if current_user["role"] != "ADMIN":
        if order.user_id != int(current_user["user_id"]):
            raise HTTPException(status_code=403, detail="Forbidden")

    return {
        "order_id": order.order_id,
        "customer_name": order.customer_name,
        "total_price": order.total_price,
        "status": order.status,
        "products": [{"name": p.name, "price": p.price, "quantity": p.quantity} for p in order.products]
    }

@router.get("/orders")
def get_orders(status: str = None,
               min_price: float = None,
               max_price: float = None,
               db=Depends(get_db), current_user: CurrentUserDTO = Depends(get_current_user)):
    repository = SQLAlchemyOrderRepository(db)
    orders = repository.get_orders(current_user, status, min_price, max_price)

    if not orders:
        raise HTTPException(status_code=404, detail="Orders not found")

    return [{
            "order_id": o.order_id,
            "customer_name": o.customer_name,
            "total_price": o.total_price,
            "status": o.status,
            "products": [{"name": p.name, "price": p.price, "quantity": p.quantity} for p in o.products]
        } for o in orders]

@router.put("/orders/{order_id}")
def edit_order(order_id: int, order_upd_dto: OrderUpdateDTO, db=Depends(get_db), current_user: CurrentUserDTO = Depends(get_current_user)):
    order_repository = SQLAlchemyOrderRepository(db)
    product_repository = SQLAlchemyProductRepository(db)
    order = order_repository.get_by_id(order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if current_user["role"] != "ADMIN":
        if order.user_id != int(current_user["user_id"]):
            raise HTTPException(status_code=403, detail="Forbidden")

    use_case = OrderUseCases(order_repository, product_repository)
    edit_order = use_case.put(order_upd_dto, order)

    return {
        "order_id": edit_order.order_id,
        "customer_name": edit_order.customer_name,
        "total_price": edit_order.total_price,
        "status": edit_order.status,
        "products": [{"name": p.name, "price": p.price, "quantity": p.quantity} for p in edit_order.products]
    }

@router.delete("/orders/{order_id}")
def delete_order():
    return