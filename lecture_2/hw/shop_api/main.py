from fastapi import FastAPI

from lecture_2.hw.shop_api.app.routes.carts import router as cart_router
from lecture_2.hw.shop_api.app.routes.items import router as item_router
from lecture_2.hw.shop_api.app.routes.chats import router as chat_router

app = FastAPI(title="Shop API")
app.include_router(item_router)
app.include_router(cart_router)
app.include_router(chat_router)