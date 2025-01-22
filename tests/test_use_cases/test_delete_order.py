from app.application.use_cases.orders import OrderUseCases
from app.infrastructure.repositories.order_repository import SQLAlchemyOrderRepository, SQLAlchemyProductRepository
from app.presentation.dto import *

def test_delete_order(db_session):
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

    deleted_order = use_case.delete(cur_order)
    assert deleted_order.is_deleted is True