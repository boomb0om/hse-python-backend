from fastapi.testclient import TestClient
from lecture_2.hw.shop_api.main import app
from threading import Thread
from queue import Queue
import time


client = TestClient(app)


def test_websocket():
    chat_name = "test_chat"
    with client.websocket_connect(f"/chat/{chat_name}") as websocket:
        with client.websocket_connect(f"/chat/{chat_name}") as websocket2:
            data = websocket.receive_text()
            assert "subscribed" in data
            data = websocket.receive_text()
            assert "subscribed" in data

            data = websocket2.receive_text()
            assert "subscribed" in data

            test_message = "Hello, WebSocket!"
            websocket.send_text(test_message)
            data = websocket.receive_text()
            assert ":: "+test_message in data

            data = websocket2.receive_text()
            assert ":: "+test_message in data

            websocket.close()
            data = websocket.receive_text()
            assert "unsubscribed" in data