from typing import Annotated
from http import HTTPStatus
from fastapi import APIRouter, Query, HTTPException, Response
from fastapi.responses import JSONResponse
from pydantic import NonNegativeInt, PositiveInt

from lecture_2.hw.shop_api.app.storages import Item, Cart, CartItem, carts_storage, items_storage
from lecture_2.hw.shop_api.app.models import CartResponse

router = APIRouter(
    prefix="/cart"
)


@router.post(
    "/",
    responses={
        HTTPStatus.CREATED: {
            "description": "Successfully created cart",
        },
    },
)
async def post_cart(response: Response) -> JSONResponse:
    cart_id = carts_storage.create_cart()
    response.headers["location"] = f"/cart/{cart_id}"
    return JSONResponse({"id": cart_id}, status_code=HTTPStatus.CREATED, headers=response.headers)


@router.get(
    "/{cart_id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully returned requested cart",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to return requested cart as one was not found",
        },
    },
)
async def get_cart(cart_id: int) -> CartResponse:
    cart = carts_storage.get_cart(cart_id)
    if cart is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Cart with id {cart_id} not found",
        )
    return CartResponse.from_cart(cart)


@router.get("/")
async def paginate_carts(
    offset: Annotated[NonNegativeInt, Query()] = 0,
    limit: Annotated[PositiveInt, Query()] = 10,
    min_price: Annotated[NonNegativeInt | None, Query()] = None,
    max_price: Annotated[NonNegativeInt | None, Query()] = None,
    min_quantity: Annotated[NonNegativeInt | None, Query()] = None,
    max_quantity: Annotated[NonNegativeInt | None, Query()] = None,
) -> list[CartResponse]:
    return [
        CartResponse.from_cart(cart) 
        for cart in carts_storage.paginate_filtered(
            offset, limit, min_price, max_price, min_quantity, max_quantity
        )
    ]


@router.post(
    "/{cart_id}/add/{item_id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully added item to cart",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to get cart or item",
        },
    },
)
async def add_item(cart_id: int, item_id: int):
    item = items_storage.get_item(item_id)
    if item is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )
    cart = carts_storage.get_cart(cart_id)
    if cart is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Cart with id {cart_id} not found",
        )
    carts_storage.add_item_to_cart(cart_id, item)
    return Response(status_code=HTTPStatus.OK)