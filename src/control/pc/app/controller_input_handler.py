import platform
from input_handler import InputHandler


class ControllerInputHandler(InputHandler):
    """
    Handles input from the PS4 controller and sends positions to the server.
    """

    def __init__(self, websocket_url: str, controller_interface: str):
        super().__init__(websocket_url)
        if platform.system() == "Linux":
            from app.models.controller import MyController            
            self.controller = MyController(
                interface=controller_interface, connecting_using_ds4drv=False
            )
        else:
            raise EnvironmentError("Controller is only supported on Linux.")

    def handle_input(self):
        self.controller.listen(on_connect=self.on_connect)

    def on_connect(self):
        print("Controller connected")
