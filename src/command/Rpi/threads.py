import time
import socket
import asyncio
import threading
import websockets
from utils import Utils
from i2c import I2CUtils
from ws import Websockets
from dotenv import load_dotenv


@Utils.loading(
    "Loading environment variables...",
    "Environment variables loaded successfully.",
    "Failed to load environment variables.",
)
def load_variables():
    return 0 if load_dotenv() else 1


class Threads:
    Utils.clear_console()
    load_variables()
    t_controller: threading.Thread
    t_camera: threading.Thread
    ###################################
    # ! Test
    t_test: threading.Thread
    ###################################

    def __init__(self):
        self.i2c_utils = I2CUtils()

        self.controller_socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM
        )
        self.controller_socket.bind(
            (
                Utils.read_variable("LISTEN_ADDRESS"),
                int(Utils.read_variable("CONTROLLER_PORT")),
            )
        )

    @Utils.loading(
        "Initializing threads...",
        "Threads initialized successfully.",
        "Failed to initialize threads.",
    )
    def init_threads(self):
        try:
            self.t_controller = threading.Thread(target=self.controller_stream)
            self.t_camera = threading.Thread(target=self.video_stream)
            #########################################################
            # ! Test
            self.t_test = threading.Thread(target=Threads.test)
            #########################################################

            return 0
        except Exception:
            return 1

    @Utils.loading(
        "Starting controller stream...",
        "Controller stream started.",
        "Failed to start controller stream.",
    )
    def start_controller_stream(self):
        try:
            self.t_controller = threading.Thread(target=self.controller_stream)
            self.t_controller.start()
            return 0
        except Exception:
            return 1

    def controller_stream(self, default_speed=200 * (10 ** (-6))):
        while True:
            recept = Utils.unwrap_message(self.sckt.recvfrom(1024))
            self.i2c_utils.write_data(recept)
            time.sleep(default_speed)

    def video_stream(self):
        start_server = websockets.serve(
            Websockets.ws_video,
            host=Utils.read_variable("RPI_ADDRESS"),
            port=int(Utils.read_variable("CAMERA_PORT")),
        )

        asyncio.get_event_loop().run_until_complete(start_server)

    def external_sensors_stream(self, port):
        start_server = websockets.serve(
            Websockets.ws_external_sensor,
            host=Utils.read_variable("RPI_ADDRESS"),
            port=port,
        )

        asyncio.get_event_loop().run_until_complete(start_server)

    def internal_sensors(self, port):
        start_server = websockets.serve(
            Websockets.ws_internal_sensors,
            host=Utils.read_variable("RPI_ADDRESS"),
            port=port,
        )

        asyncio.get_event_loop().run_until_complete(start_server)

    #####################################################################
    # ! Test
    def start_test(self):
        self.t_test.start()

    def test():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        start_server = websockets.serve(
            Websockets.ws_test,
            host=Utils.read_variable("LOCAL_ADDRESS"),
            port=8500,
        )

        loop.run_until_complete(start_server)
        loop.run_forever()

    #####################################################################
