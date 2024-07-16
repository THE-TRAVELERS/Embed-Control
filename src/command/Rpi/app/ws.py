from typing import Callable, Coroutine
from fastapi import WebSocket, WebSocketDisconnect
from dotenv import load_dotenv
from functools import wraps
import asyncio
import psutil
import socket
import os

from . import main
from .i2c import I2CUtils
from .utils import Utils

# TODO: try using Rpi
import base64
import cv2

# import board
from busio import I2C
import adafruit_bme680
from picamera2 import Picamera2
# TODO: try using Rpi


@Utils.loading(
    "Loading environment variables...",
    "Environment variables loaded successfully.",
    "Failed to load environment variables.",
)
def load_variables(docker_path: str = "../config/.env") -> int:
    """
    Loads environment variables from a specified path.

    Args:
        docker_path (str): The path to the .env file. Defaults to "../config/.env".

    Returns:
        int: 0 if environment variables were loaded successfully, 1 otherwise.
    """
    return 0 if load_dotenv() or load_dotenv(docker_path) else 1


class Websockets:
    Utils.clear_console()
    if load_variables() != 0:
        exit(1)

    i2c_utils: I2CUtils
    controller_socket: socket.socket
    piCam = None

    # TODO: try using Rpi
    i2c: I2C
    bme680: adafruit_bme680.Adafruit_BME680_I2C
    # TODO: try using Rpi

    @Utils.loading(
        "Initializing board I2C...",
        "Board I2C initialized successfully.",
        "Failed to initialize board I2C. Please ensure that the program is run from a Raspberry Pi.",
    )
    def init_board_i2c() -> int:
        """
        Initializes the board I2C interface. Placeholder for Raspberry Pi I2C initialization.

        Returns:
            int: 0 if initialization was successful, 1 otherwise.
        """
        try:
            # TODO: try using Rpi
            Websockets.i2c_utils = I2CUtils()
            if Websockets.i2c_utils.init_bus() != 0:
                return 1

            Websockets.controller_socket = socket.socket(
                family=socket.AF_INET, type=socket.SOCK_DGRAM
            )
            Websockets.controller_socket.bind(
                (
                    Utils.read_variable("LISTEN_ADDRESS"),
                    int(Utils.read_variable("CONTROLLER_PORT")),
                )
            )

            # Websockets.i2c = I2C(board.SCL, board.SDA)
            # Websockets.bme680 = adafruit_bme680.Adafruit_BME680_I2C(
            #     Websockets.i2c, debug=False
            # )
            # TODO: try using Rpi
            return 0
        except Exception:
            return 1

    @Utils.loading(
        "Initializing camera...",
        "Camera initialized successfully.",
        "Failed to initialize camera. Please ensure that the program is run from a Raspberry Pi.",
    )
    def init_camera() -> int:
        """
        Initializes the camera. Placeholder for Raspberry Pi camera initialization.

        Returns:
            int: 0 if initialization was successful, 1 otherwise.
        """
        try:
            Websockets.piCam = Picamera2()

            Websockets.piCam.video_configuration.main.size = (640, 480)
            Websockets.piCam.video_configuration.main.format = "RGB888"
            Websockets.piCam.video_configuration.align()

            Websockets.piCam.configure("video")

            return 0
        except Exception:
            return 1

    @Utils.loading(
        "(General) Initializing Websockets...",
        "(General) Websockets initialized successfully.",
        "(General) Failed to initialize Websockets.",
    )
    def init_ws_general() -> int:
        """
        Initializes general WebSocket services.

        Returns:
            int: 0 if initialization was successful, 1 otherwise.
        """
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
    def init_ws_external_sensor() -> int:
        """
        Initializes external sensor WebSocket services.

        Returns:
            int: 0 if initialization was successful, 1 otherwise.
        """
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
    def init_ws_internal_sensor() -> int:
        """
        Initializes internal sensor WebSocket services.

        Returns:
            int: 0 if initialization was successful, 1 otherwise.
        """
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

    def setup_websocket_service(
        ws_category: str,
        ws_name: str,
        func: Callable[[WebSocket], Coroutine[None, None, None]],
    ):
        """
        Sets up a WebSocket service by decorating the given function with the WebSocket route.

        Args:
            ws_category (str): The category of the WebSocket service.
            ws_name (str): The name of the WebSocket service.
            func (Callable[[WebSocket], Coroutine[None, None, None]]): The async function to be called when the WebSocket is accessed.
        """

        @main.app.websocket(f"/{ws_category}/{ws_name}")
        @wraps(func)
        async def wrapper(websocket: WebSocket):
            await websocket.accept()
            try:
                if main.services_status[ws_category][ws_name]:
                    raise Exception("Service already running.")
                else:
                    main.services_status[ws_category][ws_name] = True
                await func(websocket)
            except Exception:
                main.services_status[ws_category][ws_name] = False

        return wrapper

    async def ws_debug(websocket: WebSocket):
        """
        A WebSocket endpoint for debugging purposes. Sends an incrementing count every second.

        Args:
            websocket (WebSocket): The WebSocket connection instance.
        """
        count = 0
        while True:
            await websocket.send_text(str(count))
            count += 1
            await asyncio.sleep(1)

    async def ws_controller(websocket: WebSocket, default_speed: float = 0.0002):
        """
        A WebSocket endpoint for controlling the device. Placeholder for actual control logic.

        Args:
            websocket (WebSocket): The WebSocket connection instance.
            default_speed (float): The default speed for the control loop. Defaults to 0.0002.
        """
        while True:
            # TODO: try on Rpi
            recept = Utils.unwrap_message(Websockets.controller_socket.recvfrom(1024))
            Websockets.i2c_utils.write_data(recept)
            await asyncio.sleep(default_speed)
            # TODO: try using Rpi

    async def ws_video(websocket: WebSocket):
        """
        A WebSocket endpoint for video streaming. Placeholder for actual video streaming logic.

        Args:
            websocket (WebSocket): The WebSocket connection instance.
        """
        # TODO: try on Rpi
        print("passed")

        try:
            Websockets.piCam.start()
            print("sent")
            while True:
                frame = Websockets.piCam.capture_array()
                _, encoded = cv2.imencode(".jpg", frame)
                data = str(base64.b64encode(encoded))
                data = data[2 : len(data) - 1]  # remove the quotes from the encoding
                await websocket.send_text(data)
        except WebSocketDisconnect:
            print("exited")
            Websockets.piCam.stop()
            print("INFO X:  connection closed")

        except Exception as e:
            print(f"ERROR X: Failed to capture frame: {e}")
            Websockets.piCam.stop()

    async def ws_external_humidity(websocket: WebSocket, delay: int = 1):
        """
        A WebSocket endpoint for external humidity sensor data. Placeholder for actual sensor data retrieval.

        Args:
            websocket (WebSocket): The WebSocket connection instance.
            delay (int): The delay between data sends. Defaults to 1 second.
        """
        while True:
            # TODO: try on Rpi
            await websocket.send_text(str(Websockets.bme680.humidity))
            await asyncio.sleep(delay)

    async def ws_external_temperature(websocket: WebSocket, delay: int = 1):
        """
        A WebSocket endpoint for external temperature sensor data. Placeholder for actual sensor data retrieval.

        Args:
            websocket (WebSocket): The WebSocket connection instance.
            delay (int): The delay between data sends. Defaults to 1 second.
        """
        while True:
            # TODO: try on Rpi
            await websocket.send_text(str(Websockets.bme680.temperature))
            await asyncio.sleep(delay)

    async def ws_external_pressure(websocket: WebSocket, delay: int = 1):
        """
        A WebSocket endpoint for external pressure sensor data. Placeholder for actual sensor data retrieval.

        Args:
            websocket (WebSocket): The WebSocket connection instance.
            delay (int): The delay between data sends. Defaults to 1 second.
        """
        while True:
            # TODO: try on Rpi
            await websocket.send_text(str(Websockets.bme680.pressure))
            await asyncio.sleep(delay)

    async def ws_internal_cpu_temperature(websocket: WebSocket, delay: int = 1):
        """
        A WebSocket endpoint for internal CPU temperature data. Placeholder for actual data retrieval.

        Args:
            websocket (WebSocket): The WebSocket connection instance.
            delay (int): The delay between data sends. Defaults to 1 second.
        """
        while True:
            # TODO: try on Rpi
            cpu_temp = os.popen("vcgencmd measure_temp").readline()
            cpu_temp_float = float(cpu_temp.replace("temp=", "").replace("'C\n", ""))
            await websocket.send_text(str(round(cpu_temp_float, 2)))
            await asyncio.sleep(delay)

    async def ws_internal_cpu_usage(websocket: WebSocket, delay: int = 1):
        """
        A WebSocket endpoint for internal CPU usage data. Placeholder for actual data retrieval.

        Args:
            websocket (WebSocket): The WebSocket connection instance.
            delay (int): The delay between data sends. Defaults to 1 second.
        """
        while True:
            # TODO: try on Rpi
            await websocket.send_text(str(round(psutil.cpu_percent(interval=1), 2)))
            await asyncio.sleep(delay)

    async def ws_internal_ram_usage(websocket: WebSocket, delay: int = 1):
        """
        A WebSocket endpoint for internal RAM usage data. Placeholder for actual data retrieval.

        Args:
            websocket (WebSocket): The WebSocket connection instance.
            delay (int): The delay between data sends. Defaults to 1 second.
        """
        while True:
            # TODO: try on Rpi
            await websocket.send_text(str(round(psutil.virtual_memory().percent, 2)))
            await asyncio.sleep(delay)
