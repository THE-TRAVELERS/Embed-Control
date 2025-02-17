import logging
import websocket
from models.position import Position


class InputHandler:
    """
    Handles input from the keyboard or controller and sends positions to the server.
    """

    def __init__(self, websocket_url: str):
        self.websocket_url = websocket_url
        self.ws = websocket.WebSocketApp(
            self.websocket_url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        self.position = Position(0, 0)
        logging.info("[InputHandler] Initialized.")

    def on_open(self, ws):
        logging.info("[InputHandler] WebSocket connection opened.")

    def on_message(self, ws, message):
        logging.info(f"[InputHandler] Received message: {message}")

    def on_error(self, ws, error):
        logging.error(f"[InputHandler] Error: {error}")

    def on_close(self, ws):
        logging.info("[InputHandler] WebSocket connection closed.")

    def send_position(self, position: Position):
        logging.debug(f"[InputHandler] Sending position: {position}")
        self.ws.send(str(position))

    def start(self):
        self.ws.run_forever()
