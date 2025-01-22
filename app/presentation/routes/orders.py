from fastapi import APIRouter, Depends, HTTPException, Request
from app.application.use_cases.orders import *
from app.infrastructure.db import get_db
from app.infrastructure.metrics.metrics_service import Metrics
from app.infrastructure.auth.auth_dependencies import get_current_user
from app.infrastructure.repositories.order_repository import *
from app.presentation.dto import *

router = APIRouter()

metrics = Metrics()
# Декоратор для сбора метрик, результаты записываются в metrics.json
def collect_metrics(endpoint: str, success: bool = True):
    if success:
        metrics.increment_success(endpoint)
    else:
        metrics.increment_failure(endpoint)

# Создание заказа
@router.post("/orders")
def create_order(request: Request, order_dto: OrderCreateDTO, db=Depends(get_db), current_user: CurrentUserDTO = Depends(get_current_user)):
    order_repository = SQLAlchemyOrderRepository(db)
    product_repository = SQLAlchemyProductRepository(db)
    use_case = OrderUseCases(order_repository, product_repository)
    order = use_case.create(order_dto, int(current_user["user_id"]))

    collect_metrics(request.method + " " + request.scope["route"].path, success=True)
    return order

# Получение заказа по ID.
# Необходимо использовать генерированный по /auth/login токен
@router.get("/orders/{order_id}")
def get_order(request: Request, order_id: int, db=Depends(get_db), current_user: CurrentUserDTO = Depends(get_current_user)):
    order_repository = SQLAlchemyOrderRepository(db)
    use_case = OrderUseCases(order_repository)
    order = use_case.get_order_by_id(order_id)

    if not order:       # Если заказа не существует или удален
        collect_metrics(request.method + " " + request.scope["route"].path, success=False)
        raise HTTPException(status_code=404, detail="Order not found")

    if current_user["role"] != "ADMIN":     # Если у залогиненного пользователя роль не ADMIN и user_id не соответствует
        if order.user_id != int(current_user["user_id"]):
            collect_metrics(request.method + " " + request.scope["route"].path, success=False)
            raise HTTPException(status_code=403, detail="Forbidden")

    collect_metrics(request.method + " " + request.scope["route"].path, success=True)
    return {
        "order_id": order.order_id,
        "customer_name": order.customer_name,
        "total_price": order.total_price,
        "status": order.status,
        "products": [{"name": p.name, "price": p.price, "quantity": p.quantity} for p in order.products]
    }

# Получение заказа по фильтрам. Можно оставить фильтр пустым, тогда будут выводиться все соответствующие правам заказы.
# Если роль ADMIN, то отобразятся все заказы
# Необходимо использовать генерированный по /auth/login токен.
@router.get("/orders")
def get_orders(request: Request,
               status: str = None,
               min_price: float = None,
               max_price: float = None,
               db=Depends(get_db), current_user: CurrentUserDTO = Depends(get_current_user)):
    repository = SQLAlchemyOrderRepository(db)
    orders = repository.get_orders(current_user, status, min_price, max_price)

    if not orders:
        collect_metrics(request.method + " " + request.scope["route"].path, success=False)
        raise HTTPException(status_code=404, detail="Orders not found")

    collect_metrics(request.method + " " + request.scope["route"].path, success=True)
    return [{
            "order_id": o.order_id,
            "customer_name": o.customer_name,
            "total_price": o.total_price,
            "status": o.status,
            "products": [{"name": p.name, "price": p.price, "quantity": p.quantity} for p in o.products]
        } for o in orders]

# Изменение заказа по ID.
# Необходимо использовать генерированный по /auth/login токен.
@router.put("/orders/{order_id}")
def edit_order(request: Request, order_id: int, order_upd_dto: OrderUpdateDTO, db=Depends(get_db), current_user: CurrentUserDTO = Depends(get_current_user)):
    order_repository = SQLAlchemyOrderRepository(db)
    product_repository = SQLAlchemyProductRepository(db)
    order = order_repository.get_by_id(order_id)

    if not order:       # Если заказа не существует или удален
        collect_metrics(request.method + " " + request.scope["route"].path, success=False)
        raise HTTPException(status_code=404, detail="Order not found")

    if current_user["role"] != "ADMIN":     # Если у залогиненного пользователя роль не ADMIN и user_id не соответствует
        if order.user_id != int(current_user["user_id"]):
            collect_metrics(request.method + " " + request.scope["route"].path, success=False)
            raise HTTPException(status_code=403, detail="Forbidden")

    use_case = OrderUseCases(order_repository, product_repository)
    edit_order = use_case.put(order_upd_dto, order)

    collect_metrics(request.method + " " + request.scope["route"].path, success=True)
    return {
        "order_id": edit_order.order_id,
        "customer_name": edit_order.customer_name,
        "total_price": edit_order.total_price,
        "status": edit_order.status,
        "products": [{"name": p.name, "price": p.price, "quantity": p.quantity} for p in edit_order.products]
    }

# Удаление заказа по ID.
# Необходимо использовать генерированный по /auth/login токен.
@router.delete("/orders/{order_id}")
def delete_order(request: Request, order_id: int, db=Depends(get_db), current_user: CurrentUserDTO = Depends(get_current_user)):
    repository = SQLAlchemyOrderRepository(db)
    order = repository.get_by_id(order_id)

    if not order:       # Если заказа не существует или удален
        collect_metrics(request.method + " " + request.scope["route"].path, success=False)
        raise HTTPException(status_code=404, detail="Order not found")

    if current_user["role"] != "ADMIN":     # Если у залогиненного пользователя роль не ADMIN и user_id не соответствует
        if order.user_id != int(current_user["user_id"]):
            collect_metrics(request.method + " " + request.scope["route"].path, success=False)
            raise HTTPException(status_code=403, detail="Forbidden")

    use_case = OrderUseCases(repository)
    delete_order = use_case.delete(order)

    collect_metrics(request.method + " " + request.scope["route"].path, success=True)
    return {
        "order_id": delete_order.order_id,
        "is_deleted": delete_order.is_deleted
    }