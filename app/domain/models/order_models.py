class Product:
    def __init__(self, name: str, price: float, quantity: int, order_id):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.order_id = order_id

class Order:
    def __init__(self, customer_name: str, products: list[Product], total_price: float, user_id: int, status: str = "pending"):
        self.customer_name = customer_name
        self.products = products
        self.total_price = total_price
        self.user_id = user_id
        self.status = status