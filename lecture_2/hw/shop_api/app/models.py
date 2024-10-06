from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from lecture_2.hw.shop_api.app.storages import Item, Cart, CartItem


class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    deleted: bool

    @classmethod
    def from_item(cls, item: Item) -> ItemResponse:
        return cls(
            id=item.id,
            name=item.name,
            price=item.price,
            deleted=item.deleted,
        )
    

class ItemRequest(BaseModel):
    name: str
    price: float


class ItemUpdateRequest(BaseModel):
    name: str | None = None
    price: float | None = None

    model_config = ConfigDict(extra="forbid")


class CartItemResponse(BaseModel):
    id: int
    name: str
    quantity: int
    available: bool

    @classmethod
    def from_cart_item(cls, cart_item: CartItem) -> CartItem:
        return cls(
            id=cart_item.id,
            name=cart_item.name,
            quantity=cart_item.quantity,
            available=cart_item.available,
        )


class CartResponse(BaseModel):
    id: int
    items: list[CartItemResponse]
    price: float

    @classmethod
    def from_cart(cls, cart: Cart) -> CartResponse:
        return cls(
            id=cart.id,
            items=[CartItemResponse.from_cart_item(item) for item in cart.items.values()],
            price=cart.price,
        )