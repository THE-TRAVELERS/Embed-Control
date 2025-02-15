import logging
from typing import Callable, Coroutine
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from functools import wraps

from app.i2c import I2CUtils
from app.routers.services import WebSocketsServices
from app.routers.status import services_status

enabled_services = {
    "debug": True,
    "controller": True,
    "camera": True,
    "humidity": False,
    "temperature": False,
    "pressure": False,
    "cpu_temperature": True,
    "cpu_usage": True,
    "ram_usage": True,
}

router: APIRouter = APIRouter()


class WebSocketManager:
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

        @router.websocket(f"/{ws_category}/{ws_name}")
        @wraps(func)
        async def wrapper(websocket: WebSocket):
            await websocket.accept()
            logging.info(
                f"[WEBSOCKET] {ws_category}/{ws_name} WebSocket connection established."
            )
            try:
                if services_status[ws_category][ws_name]:
                    logging.warning(
                        f"[WEBSOCKET] {ws_category}/{ws_name} WebSocket connection already active."
                    )
                else:
                    services_status[ws_category][ws_name] = True
                    await func(websocket)
            except WebSocketDisconnect:
                services_status[ws_category][ws_name] = False
                logging.info(
                    f"[WEBSOCKET] {ws_category}/{ws_name} WebSocket connection closed."
                )
            except Exception as e:
                services_status[ws_category][ws_name] = False
                logging.error(
                    f"[WEBSOCKET] {ws_category}/{ws_name} WebSocket error: {e}"
                )
                logging.info(
                    f"[WEBSOCKET] {ws_category}/{ws_name} WebSocket connection closed."
                )

        return wrapper

    @classmethod
    def init_services(cls) -> None:
        """
        Initializes all WebSocket services.
        """
        cls.init_ws_general()
        cls.init_ws_external_sensor()
        cls.init_ws_internal_sensor()
        logging.info("[WEBSOCKETS] Initialization complete.")

    @classmethod
    def init_ws_general(cls) -> None:
        """
        Initializes all general WebSocket services.
        """
        if (
            enabled_services["debug"]
            or enabled_services["controller"]
            or enabled_services["camera"]
        ):
            if enabled_services["debug"]:
                logging.debug("[WEBSOCKETS] Initializing debug service.")
                cls.setup_websocket_service(
                    "general",
                    "debug",
                    WebSocketsServices.ws_debug,
                )
                logging.debug("[WEBSOCKETS] Initialized.")
            if enabled_services["controller"]:
                logging.debug("[WEBSOCKETS] Initializing controller service.")
                cls.setup_websocket_service(
                    "general",
                    "controller",
                    WebSocketsServices.ws_controller,
                )
                logging.debug("[WEBSOCKETS] Initialized.")
            if enabled_services["camera"]:
                logging.debug("[WEBSOCKETS] Initializing camera service.")
                if I2CUtils.init_camera():
                    cls.setup_websocket_service(
                        "general",
                        "camera",
                        WebSocketsServices.ws_camera,
                    )
                    logging.debug("[WEBSOCKETS] Initialized.")
                else:
                    logging.error("[WEBSOCKETS] Initialization failed.")
        else:
            logging.warning("[WEBSOCKETS] Skipping initialization of general services.")

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
            if I2CUtils.init_bme680():
                if enabled_services["humidity"]:
                    logging.debug("[WEBSOCKETS] Initializing humidity service.")
                    cls.setup_websocket_service(
                        "external_sensor",
                        "humidity",
                        WebSocketsServices.ws_external_humidity,
                    )
                    logging.debug("[WEBSOCKETS] Initialized.")
                if enabled_services["temperature"]:
                    logging.debug("[WEBSOCKETS] Initializing temperature service.")
                    cls.setup_websocket_service(
                        "external_sensor",
                        "temperature",
                        WebSocketsServices.ws_external_temperature,
                    )
                    logging.debug("[WEBSOCKETS] Initialized.")
                if enabled_services["pressure"]:
                    logging.debug("[WEBSOCKETS] Initializing pressure service.")
                    cls.setup_websocket_service(
                        "external_sensor",
                        "pressure",
                        WebSocketsServices.ws_external_pressure,
                    )
                    logging.debug("[WEBSOCKETS] Initialized.")
            else:
                logging.error(
                    "[WEBSOCKETS] Failed to initialize external sensor services."
                )
        else:
            logging.warning(
                "[WEBSOCKETS] Skipping initialization of external sensor services."
            )

    @classmethod
    def init_ws_internal_sensor(cls) -> None:
        """
        Initializes all internal sensor WebSocket services.
        """
        if (
            enabled_services["cpu_temperature"]
            or enabled_services["cpu_usage"]
            or enabled_services["ram_usage"]
        ):
            if enabled_services["cpu_temperature"]:
                logging.debug("[WEBSOCKETS] Initializing CPU temperature service.")
                cls.setup_websocket_service(
                    "internal_sensor",
                    "cpu_temperature",
                    WebSocketsServices.ws_internal_cpu_temperature,
                )
                logging.debug("[WEBSOCKETS] Initialized.")
            if enabled_services["cpu_usage"]:
                logging.debug("[WEBSOCKETS] Initializing CPU usage service.")
                cls.setup_websocket_service(
                    "internal_sensor",
                    "cpu_usage",
                    WebSocketsServices.ws_internal_cpu_usage,
                )
                logging.debug("[WEBSOCKETS] Initialized.")
            if enabled_services["ram_usage"]:
                logging.debug("[WEBSOCKETS] Initializing RAM usage service.")
                cls.setup_websocket_service(
                    "internal_sensor",
                    "ram_usage",
                    WebSocketsServices.ws_internal_ram_usage,
                )
                logging.debug("[WEBSOCKETS] Initialized.")
        else:
            logging.warning(
                "[WEBSOCKETS] Skipping initialization of internal sensor services."
            )
