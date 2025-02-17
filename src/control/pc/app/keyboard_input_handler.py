import logging
from input_handler import InputHandler
from models.position import Position
from pynput import keyboard


class KeyboardInputHandler(InputHandler):
    """
    Handles input from the keyboard and sends positions to the server.
    """

    def __init__(self, websocket_url: str):
        super().__init__(websocket_url)
        logging.info("[KeyboardInputHandler] Initialized.")
        self.listener = keyboard.Listener(on_press=self.on_press)

    def on_press(self, key):
        try:
            if key == keyboard.Key.up:
                self.send_position(Position(0, 1))
            elif key == keyboard.Key.down:
                self.send_position(Position(0, -1))
            elif key == keyboard.Key.right:
                self.send_position(Position(-1, 0))
            elif key == keyboard.Key.left:
                self.send_position(Position(1, 0))
            elif key == keyboard.Key.esc:
                self.listener.stop()
        except AttributeError:
            pass

    def handle_input(self):
        self.listener.start()
        self.listener.join()

    def start(self):
        super().start()
        self.handle_input()
