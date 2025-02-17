import logging
from pyPS4Controller.controller import Controller
from position import Position


class MyController(Controller):
    """
    Custom controller class to handle PS4 controller inputs.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.position = Position(0, 0)
        logging.info("[MyController] Initialized.")

    def on_L3_up(self, value):
        self.position.y = max(min(value, 1.0), -1.0)
        self.send_position()

    def on_L3_down(self, value):
        self.position.y = max(min(-value, 1.0), -1.0)
        self.send_position()

    def on_L3_left(self, value):
        self.position.x = max(min(-value, 1.0), -1.0)
        self.send_position()

    def on_L3_right(self, value):
        self.position.x = max(min(value, 1.0), -1.0)
        self.send_position()

    def send_position(self):
        # Send the position to the server via WebSocket
        pass
