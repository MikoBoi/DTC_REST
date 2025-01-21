from fastapi import APIRouter, Depends
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
def get_order():
    return

@router.get("/orders")
def get_orders():
    return

@router.put("/orders/{order_id}")
def edit_order():
    return

@router.delete("/orders/{order_id}")
def delete_order():
    return