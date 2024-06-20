import socket
import threading
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
    t_debug: threading.Thread
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
            self.t_controller = threading.Thread(target=Websockets.ws_controller_loop)
            self.t_camera = threading.Thread(target=Websockets.ws_video_loop)
            #########################################################
            # ! Test
            self.t_debug = threading.Thread(target=Websockets.ws_debug_loop)
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

    

    #####################################################################
    # ! Test
    def start_debug_ws(self):
        self.t_debug.start()

    #####################################################################
