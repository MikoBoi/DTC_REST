from fastapi import APIRouter

router = APIRouter()

@router.post("/orders")
def create_order():
    return

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