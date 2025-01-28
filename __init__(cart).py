from typing import List, Optional
import json
import products
from cart import dao
from products import Product


class Cart:
    def __init__(self, id: int, username: str, contents: List[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data: dict) -> 'Cart':
        """
        Deserialize cart data into a Cart object.
        """
        return Cart(
            id=data['id'],
            username=data['username'],
            contents=[Product(**item) for item in json.loads(data['contents'])],  # Safely deserialize
            cost=data['cost']
        )


def get_cart(username: str) -> List[Product]:
    """
    Retrieve the cart for a given username.
    Returns a list of Product objects in the cart.
    """
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    items = []
    for cart_detail in cart_details:
        try:
            # Safely deserialize the contents field
            contents = json.loads(cart_detail['contents'])
            for content in contents:
                product = products.get_product(content['id'])  # Assuming content has an 'id' field
                if product:
                    items.append(product)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error processing cart contents: {e}")
            continue

    return items


def add_to_cart(username: str, product_id: int):
    """
    Add a product to the user's cart.
    """
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    """
    Remove a product from the user's cart.
    """
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str):
    """
    Delete the entire cart for a user.
    """
    dao.delete_cart(username)