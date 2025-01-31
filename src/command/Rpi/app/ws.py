from typing import Callable, Coroutine
from fastapi import WebSocket
from functools import wraps

from app import main

from app.i2c import I2CUtils
from app.routers.services import WebSocketsServices
from app.routers.status import services_status

enabled_services = {
    "debug": True,
    "controller": True,
    "camera": True,
    "humidity": True,
    "temperature": True,
    "pressure": True,
    "CPU_temperature": True,
    "CPU_usage": True,
    "RAM_usage": True,
}


class WebSocketManager:
    @classmethod
    def init_services(cls) -> None:
        """
        Initializes all WebSocket services.
        """
        cls.init_ws_general()
        cls.init_ws_external_sensor()
        cls.init_ws_internal_sensor()

    @classmethod
    def init_ws_general(cls) -> None:
        """
        Initializes all general WebSocket services.
        """
        if enabled_services["debug"]:
            cls.setup_websocket_service(
                "general",
                "debug",
                WebSocketsServices.ws_debug,
            )
        if enabled_services["controller"]:
            cls.setup_websocket_service(
                "general",
                "controller",
                WebSocketsServices.ws_controller,
            )
        if enabled_services["camera"]:
            I2CUtils.init_camera()
            cls.setup_websocket_service(
                "general",
                "camera",
                WebSocketsServices.ws_camera,
            )

    @classmethod
    def init_ws_external_sensor(cls) -> None:
        """
        Initializes all external sensor WebSocket services.
        """
        if (
            enabled_services["humidity"]
            or enabled_services["temperature"]
            or enabled_services["pressure"]
        ):
            I2CUtils.init_bme680()
        if enabled_services["humidity"]:
            cls.setup_websocket_service(
                "external_sensor",
                "humidity",
                WebSocketsServices.ws_external_humidity,
            )
        if enabled_services["temperature"]:
            cls.setup_websocket_service(
                "external_sensor",
                "temperature",
                WebSocketsServices.ws_external_temperature,
            )
        if enabled_services["pressure"]:
            cls.setup_websocket_service(
                "external_sensor",
                "pressure",
                WebSocketsServices.ws_external_pressure,
            )

    @classmethod
    def init_ws_internal_sensor(cls) -> None:
        """
        Initializes all internal sensor WebSocket services.
        """
        if enabled_services["CPU_temperature"]:
            cls.setup_websocket_service(
                "internal_sensor",
                "CPU_temperature",
                WebSocketsServices.ws_internal_cpu_temperature,
            )
        if enabled_services["CPU_usage"]:
            cls.setup_websocket_service(
                "internal_sensor",
                "CPU_usage",
                WebSocketsServices.ws_internal_cpu_usage,
            )
        if enabled_services["RAM_usage"]:
            cls.setup_websocket_service(
                "internal_sensor",
                "RAM_usage",
                WebSocketsServices.ws_internal_ram_usage,
            )

    @classmethod
    def setup_websocket_service(
        cls,
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
                if services_status[ws_category][ws_name]:
                    raise Exception("Service already running.")
                else:
                    services_status[ws_category][ws_name] = True
                await func(websocket)
            except Exception:
                services_status[ws_category][ws_name] = False

        return wrapper
