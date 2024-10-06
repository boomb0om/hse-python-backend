from dataclasses import dataclass
from itertools import islice

from lecture_2.hw.shop_api.app.storages import Item


@dataclass(slots=True)
class CartItem:
    id: int
    name: str
    quantity: int
    available: bool


@dataclass(slots=True)
class Cart:
    id: int
    items: dict[int, CartItem]
    price: float


class CartStorage:

    def __init__(self):
        self.carts: dict[int, Cart] = {}

    def create_cart(self) -> int:
        new_id = len(self.carts) + 1
        cart = Cart(id=new_id, items={}, price=0)
        self.carts[new_id] = cart
        return new_id
    
    def get_cart(self, cart_id: int) -> Cart | None:
        return self.carts.get(cart_id)
    
    def add_item_to_cart(self, cart_id: int, item: Item) -> CartItem:
        cart = self.carts[cart_id]
        if item.id in cart.items:
            cart.items[item.id].quantity += 1
        else:
            cart.items[item.id] = CartItem(
                id=item.id, name=item.name, quantity=1, available=not item.deleted
            )
        cart.price += item.price
        return cart.items[item.id]
    
    def paginate_filtered(
        self,
        offset: int = 0,
        limit: int = 10,
        min_price: float | None = None,
        max_price: float | None = None,
        min_quantity: int | None = None,
        max_quantity: int | None = None,
    ) -> list[Item]:
        
        def filter_cart(cart: Cart) -> bool:
            if min_price is not None and cart.price < min_price:
                return False
            if max_price is not None and cart.price > max_price:
                return False
            quantity = sum([item.quantity for item in cart.items.values()])
            if min_quantity is not None and quantity < min_quantity:
                return False
            if max_quantity is not None and quantity > max_quantity:
                return False
            return True

        carts = islice(filter(filter_cart, list(self.carts.values())), offset, limit)
        return list(carts)


carts_storage = CartStorage()