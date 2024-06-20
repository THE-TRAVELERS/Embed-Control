from i2c import I2CUtils
from utils import Utils
import api
from dotenv import load_dotenv
from fastapi import WebSocket
from functools import wraps
import asyncio
import socket

# TODO: try using Rpi
# import base64
# import cv2
# import board
# from busio import I2C
# import adafruit_bme680


@Utils.loading(
    "Loading environment variables...",
    "Environment variables loaded successfully.",
    "Failed to load environment variables.",
)
def load_variables():
    return 0 if load_dotenv() else 1


class Websockets:
    Utils.clear_console()
    load_variables()

    i2c_utils: I2CUtils
    controller_socket: socket.socket

    # TODO: try using Rpi
    # i2c: I2C
    # bme680: adafruit_bme680.Adafruit_BME680_I2C

    @Utils.loading(
        "Initializing board I2C...",
        "Board I2C initialized successfully.",
        "Failed to initialize board I2C. Please ensure that the program is run from a Raspberry Pi.",
    )
    def init_board_i2c():
        try:
            # TODO: try using Rpi
            # Websockets.i2c_utils = I2CUtils()
            # if Websockets.i2c_utils.init_bus() != 0:
            #     return 1

            # Websockets.controller_socket = socket.socket(
            #     family=socket.AF_INET, type=socket.SOCK_DGRAM
            # )
            # Websockets.controller_socket.bind(
            #     (
            #         Utils.read_variable("LISTEN_ADDRESS"),
            #         int(Utils.read_variable("CONTROLLER_PORT")),
            #     )
            # )

            # Websockets.i2c = I2C(board.SCL, board.SDA)
            # Websockets.bme680 = adafruit_bme680.Adafruit_BME680_I2C(
            #     Websockets.i2c, debug=False
            # )
            return 0
        except Exception:
            return 1

    @Utils.loading(
        "(General) Initializing Websockets...",
        "(General) Websockets initialized successfully.",
        "(General) Failed to initialize Websockets.",
    )
    def init_ws_general():
        try:
            Websockets.setup_websocket_service(
                "general",
                "debug",
                Websockets.ws_debug,
            )
            Websockets.setup_websocket_service(
                "general",
                "controller",
                Websockets.ws_controller,
            )
            Websockets.setup_websocket_service(
                "general",
                "video",
                Websockets.ws_video,
            )

            return 0
        except Exception:
            return 1

    @Utils.loading(
        "(External Sensor) Initializing Websockets...",
        "(External Sensor) Websockets initialized successfully.",
        "(External Sensor) Failed to initialize Websockets.",
    )
    def init_ws_external_sensor():
        try:
            Websockets.setup_websocket_service(
                "external_sensor",
                "humidity",
                Websockets.ws_external_humidity,
            )
            Websockets.setup_websocket_service(
                "external_sensor",
                "temperature",
                Websockets.ws_external_temperature,
            )
            Websockets.setup_websocket_service(
                "external_sensor",
                "pressure",
                Websockets.ws_external_pressure,
            )

            return 0
        except Exception:
            return 1

    @Utils.loading(
        "(Internal Sensor) Initializing Websockets...",
        "(Internal Sensor) Websockets initialized successfully.",
        "(Internal Sensor) Failed to initialize Websockets.",
    )
    def init_ws_internal_sensor():
        try:
            Websockets.setup_websocket_service(
                "internal_sensor",
                "CPU_temperature",
                Websockets.ws_internal_cpu_temperature,
            )
            Websockets.setup_websocket_service(
                "internal_sensor",
                "CPU_usage",
                Websockets.ws_internal_cpu_usage,
            )
            Websockets.setup_websocket_service(
                "internal_sensor",
                "RAM_usage",
                Websockets.ws_internal_ram_usage,
            )

            return 0
        except Exception:
            return 1

    def setup_websocket_service(ws_category: str, ws_name: str, func):
        @api.API.app.websocket(f"/{ws_category}/{ws_name}")
        @wraps(func)
        async def wrapper(websocket: WebSocket):
            await websocket.accept()
            try:
                if api.API.services_status[ws_category][ws_name]:
                    raise Exception("Service already running.")
                else:
                    api.API.services_status[ws_category][ws_name] = True
                await func(websocket)
            except Exception:
                api.API.services_status[ws_category][ws_name] = False

        return wrapper

    async def ws_debug(websocket: WebSocket):
        count = 0
        while True:
            await websocket.send_text(str(count))
            count += 1
            await asyncio.sleep(1)

    async def ws_controller(self, default_speed=0.0002):
        while True:
            # TODO: try on Rpi
            # recept = Utils.unwrap_message(Websockets.controller_socket.recvfrom(1024))
            # Websockets.i2c_utils.write_data(recept)
            await asyncio.sleep(default_speed)

    async def ws_video(websocket):
        # TODO: update websocket send function (send -> send_text...)
        # TODO: try on Rpi
        # capture = cv2.VideoCapture(0)
        # while capture.isOpened():
        #     _, frame = capture.read()
        #     encoded = cv2.imencode(".jpg", frame)[1]
        #     data = str(base64.b64encode(encoded))
        #     data = data[2 : len(data) - 1]
        #     await websocket.send(data)
        # capture.release()
        pass

    async def ws_external_humidity(websocket, delay=1):
        while True:
            # TODO: try on Rpi
            await websocket.send_text(str(Websockets.bme680.humidity))
            await asyncio.sleep(delay)

    async def ws_external_temperature(websocket, delay=1):
        while True:
            # TODO: try on Rpi
            await websocket.send_text(str(Websockets.bme680.temperature))
            await asyncio.sleep(delay)

    async def ws_external_pressure(websocket, delay=1):
        while True:
            # TODO: try on Rpi
            await websocket.send_text(str(Websockets.bme680.pressure))
            await asyncio.sleep(delay)

    async def ws_internal_cpu_temperature(websocket, delay=1):
        while True:
            # TODO: Implement
            await asyncio.sleep(delay)

    async def ws_internal_cpu_usage(websocket, delay=1):
        while True:
            # TODO: Implement
            await asyncio.sleep(delay)

    async def ws_internal_ram_usage(websocket, delay=1):
        while True:
            # TODO: Implement
            await asyncio.sleep(delay)
