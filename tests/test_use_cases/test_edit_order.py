from app.application.use_cases.orders import OrderUseCases
from app.infrastructure.repositories.order_repository import SQLAlchemyOrderRepository, SQLAlchemyProductRepository
from app.presentation.dto import *

def test_edit_order(db_session):
    order_repo = SQLAlchemyOrderRepository(db_session)
    product_repo = SQLAlchemyProductRepository(db_session)
    use_case = OrderUseCases(order_repo, product_repo)

    order_data = {
        "customer_name": "PYTEST_CUSTOMER",
        "products": [{"name": "Test Product", "price": 100, "quantity": 2}],
    }
    order_dto = OrderCreateDTO.parse_obj(order_data)

    order = use_case.create(order_dto, cur_user_id=1)

    assert order[0].customer_name == "PYTEST_CUSTOMER"

    cur_order = order_repo.get_by_id(order[1]['order_id'])

    edit_order_data = {
        "status": "cancelled"
    }
    order_update_dto = OrderUpdateDTO.parse_obj(edit_order_data)
    edited_order = use_case.put(order_update_dto, cur_order)

    assert edited_order.customer_name == "PYTEST_CUSTOMER"
    assert edited_order.total_price == 200
    assert edited_order.status.value == "cancelled"