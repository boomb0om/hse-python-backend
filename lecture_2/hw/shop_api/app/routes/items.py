from typing import Annotated
from http import HTTPStatus
from fastapi import APIRouter, Query, HTTPException, Response
from fastapi.responses import JSONResponse
from pydantic import NonNegativeInt, PositiveInt

from lecture_2.hw.shop_api.app.models import ItemResponse, ItemRequest, ItemUpdateRequest
from lecture_2.hw.shop_api.app.storages import items_storage, Item

router = APIRouter(
    prefix="/item"
)


@router.post(
    "/",
    status_code=HTTPStatus.CREATED
)
async def add_new(item: ItemRequest) -> ItemResponse:
    item = items_storage.add_new_item(item.name, item.price)
    return ItemResponse.from_item(item)


@router.get(
    "/{item_id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully returned requested item",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to return requested item as one was not found",
        },
    },
)
async def get_item(item_id: int) -> ItemResponse:
    item = items_storage.get_item(item_id)
    if item is None or item.deleted:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )
    return ItemResponse.from_item(item)


@router.get("/")
async def paginate_items(
    offset: Annotated[NonNegativeInt, Query()] = 0,
    limit: Annotated[PositiveInt, Query()] = 10,
    min_price: Annotated[NonNegativeInt | None, Query()] = None,
    max_price: Annotated[NonNegativeInt | None, Query()] = None,
    show_deleted: Annotated[bool, Query()] = False,
) -> list[ItemResponse]:
    return items_storage.paginate_items_filtered(offset, limit, min_price, max_price, show_deleted)
    

@router.put("/{item_id}")
async def put_item(item_id: int, item: ItemRequest) -> ItemResponse:
    try:
        item = items_storage.replace_item(item_id, item.name, item.price)
    except ValueError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Item id {item_id} not found",
        )
    
    return ItemResponse.from_item(item)


@router.patch("/{item_id}")
async def update_item(item_id: int, item_update_info: ItemUpdateRequest) -> ItemResponse:
    item = items_storage.get_item(item_id)
    if item.deleted:
        raise HTTPException(
            status_code=HTTPStatus.NOT_MODIFIED,
            detail="Item is deleted",
        )
    try:
        item = items_storage.update_item(item_id, item_update_info.name, item_update_info.price)
    except ValueError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Item id {item_id} not found",
        )
    return ItemResponse.from_item(item)


@router.delete("/{item_id}")
async def delete_item(item_id: int) -> Response:
    try:
        items_storage.delete_item(item_id)
    except ValueError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Item id {item_id} not found",
        )
    return Response(status_code=HTTPStatus.OK)