import time
import socket
import asyncio
import threading
import websockets
from utils import Utils
from i2c import I2CUtils
from ws import Websockets


class Threads:
    def __init__(self):
        self.is_camera_active = False
        self.is_controller_active = False

        self.i2c_utils = I2CUtils()

        self.controller_socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM
        )
        self.controller_socket.bind(
            (
                Utils.read_variable("LISTEN_ADDRESS"),
                Utils.read_variable("CONTROLLER_PORT"),
            )
        )

        # self.t_camera = threading.Thread(target=self.video_stream)

        # self.t_camera.start()

    @Utils.loading(
        "Starting controller stream...",
        "Controller stream started.",
        "Failed to start controller stream.",
    )
    def start_controller_stream(self):
        try:
            self.is_controller_active = True
            self.t_controller = threading.Thread(target=self.controller_stream)
            self.t_controller.start()
            return 0
        except Exception:
            return 1

    def controller_stream(
        self, default_speed=200 * (10 ** (-6)), default_standby_time=3
    ):
        while True:
            if self.is_controller_active:
                recept = Utils.unwrap_message(self.sckt.recvfrom(1024))
                self.i2c_utils.write_data(recept)
                time.sleep(default_speed)
            else:
                time.sleep(default_standby_time)

    def stop_controller_stream(self):
        self.is_controller_active = False

    def video_stream(self):
        start_server = websockets.serve(
            Websockets.ws_video,
            host=Utils.read_variable("RPI_ADDRESS"),
            port=Utils.read_variable("CAMERA_PORT"),
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
