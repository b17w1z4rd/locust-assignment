from typing import List, Dict
from products import dao


class Product:
    def __init__(self, id: int, name: str, description: str, cost: float, qty: int = 0):
        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.qty = qty

    @classmethod
    def load(cls, data: Dict) -> 'Product':
        """Create a Product instance from a dictionary."""
        return cls(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            cost=data['cost'],
            qty=data.get('qty', 0)  # Default to 0 if 'qty' is not provided
        )


def list_products() -> List[Product]:
    """Retrieve a list of all products."""
    products_data = dao.list_products()
    return [Product.load(product) for product in products_data]


def get_product(product_id: int) -> Product:
    """Retrieve a single product by its ID."""
    product_data = dao.get_product(product_id)
    if not product_data:
        raise ValueError(f"Product with ID {product_id} not found")
    return Product.load(product_data)


def add_product(product: Dict):
    """Add a new product to the database."""
    if not all(key in product for key in ['name', 'description', 'cost']):
        raise ValueError("Product dictionary must contain 'name', 'description', and 'cost'")
    dao.add_product(product)


def update_qty(product_id: int, qty: int):
    """Update the quantity of a product."""
    if qty < 0:
        raise ValueError('Quantity cannot be negative')
    if not dao.get_product(product_id):
        raise ValueError(f"Product with ID {product_id} not found")
    dao.update_qty(product_id, qty)