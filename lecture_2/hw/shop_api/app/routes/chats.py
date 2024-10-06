from dataclasses import dataclass, field
from uuid import uuid4
from fastapi import APIRouter, Request, HTTPException, Response
from fastapi import WebSocket, WebSocketDisconnect


router = APIRouter(
    prefix="/chat"
)


@dataclass(slots=True)
class ChatBroadcaster:
    subscribers: list[WebSocket] = field(init=False, default_factory=list)

    async def subscribe(self, ws: WebSocket) -> None:
        await ws.accept()
        self.subscribers.append(ws)

    async def unsubscribe(self, ws: WebSocket) -> None:
        self.subscribers.remove(ws)

    async def publish(self, message: str) -> None:
        for ws in self.subscribers:
            await ws.send_text(message)


@dataclass(slots=True)
class ChatStorage:
    chat2broadcaster: dict[str, ChatBroadcaster] = field(init=False, default_factory=dict)

    def get_chat_broadcaster(self, chat_name: str) -> ChatBroadcaster:
        if chat_name in self.chat2broadcaster:
            return self.chat2broadcaster[chat_name]
        else:
            new_broadcaster = ChatBroadcaster()
            self.chat2broadcaster[chat_name] = new_broadcaster
            return new_broadcaster


chat_store = ChatStorage()


@router.websocket("/{chat_name}")
async def ws_subscribe(chat_name: str, ws: WebSocket):
    client_id = uuid4()

    broadcaster = chat_store.get_chat_broadcaster(chat_name)
    await broadcaster.subscribe(ws)
    await broadcaster.publish(f"client {client_id} subscribed")

    try:
        while True:
            text = await ws.receive_text()
            text = f"{client_id} :: {text}"
            await broadcaster.publish(text)
    except WebSocketDisconnect:
        broadcaster.unsubscribe(ws)
        await broadcaster.publish(f"client {client_id} unsubscribed")