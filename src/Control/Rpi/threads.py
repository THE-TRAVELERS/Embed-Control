import threading
import socket
import time
from i2c import I2CInterface
from utils import Utils
import websockets
import asyncio


class Threads:
    def __init__(self):
        self.is_camera_active = False
        self.is_controller_active = False

        self.utils = Utils()

        self.i2c = I2CInterface()
        self.sckt = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.sckt.bind(("0.0.0.0", 5005))  # 0.0.0.0 = recevoir de tout le monde

        self.t_move = threading.Thread(target=self.move)
        self.t_camera = threading.Thread(target=self.capture_stream)
        self.t_move.start()
        self.t_camera.start()

    def move(self, default_speed=200 * (10 ** (-6)), default_standby_time=3):
        while True:
            if self.is_controller_active:
                recept = Utils.unwrap_message(self.sckt.recvfrom(1024))
                self.i2c.write_data(recept)
                time.sleep(default_speed)
            else:
                time.sleep(default_standby_time)

    def capture_stream(self):
        PORT = 9000
        ADDRESS = "10.3.141.1"

        start_server = websockets.serve(self.utils.transmit, host=ADDRESS, port=PORT)

        asyncio.get_event_loop().run_until_complete(start_server)
