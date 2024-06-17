import time
import socket
import asyncio
import threading
import websockets
from utils import Utils
from i2c import I2CUtils


class Threads:
    def __init__(self):
        self.is_camera_active = False
        self.is_controller_active = False
        self.ADDRESS = "10.3.141.1"

        self.utils = Utils()

        self.i2c_utils = I2CUtils()

        self.sckt = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.sckt.bind(("0.0.0.0", 5005))  # 0.0.0.0 = accept de tout le monde

        self.t_move = threading.Thread(target=self.move)
        self.t_camera = threading.Thread(target=self.video_stream)

        self.t_move.start()
        self.t_camera.start()

    def move(self, default_speed=200 * (10 ** (-6)), default_standby_time=3):
        while True:
            if self.is_controller_active:
                recept = Utils.unwrap_message(self.sckt.recvfrom(1024))
                self.i2c_utils.write_data(recept)
                time.sleep(default_speed)
            else:
                time.sleep(default_standby_time)

    def video_stream(self):
        PORT = 9000

        start_server = websockets.serve(
            self.utils.ws_video, host=self.ADDRESS, port=PORT
        )

        asyncio.get_event_loop().run_until_complete(start_server)

    def sensors_stream(self):
        PORT = 9001

        start_server = websockets.serve(
            self.utils.ws_sensors, host=self.ADDRESS, port=PORT
        )

        asyncio.get_event_loop().run_until_complete(start_server)
        
    def internal_sensors(self):
        PORT = 9002
        
        start_server = websockets.serve(
            self.utils.ws_internal_sensors, host=self.ADDRESS, port=PORT
        )
        
        asyncio.get_event_loop().run_until_complete(start_server)
