from fastapi import FastAPI, HTTPException
import threading
from typing import Any, Dict

from . import ws

app: FastAPI = FastAPI()
t_run: threading.Thread
services_status: Dict[str, Dict[str, bool]] = {
    "general": {
        "video": False,
        "controller": False,
        "debug": False,
    },
    "external_sensor": {
        "humidity": False,
        "temperature": False,
        "pressure": False,
    },
    "internal_sensor": {
        "CPU_temperature": False,
        "CPU_usage": False,
        "RAM_usage": False,
    },
}


@app.get("/")
async def ping() -> Dict[str, str]:
    """
    Endpoint to check the connection status of the server.

    Returns:
        Dict[str, str]: A dictionary with the connection status.
    """
    return {"Connection Status": "Active"}


@app.get("/status/all")
async def get_all_status() -> Dict[str, Dict[str, bool]]:
    """
    Endpoint to get the status of all services.

    Returns:
        Dict[str, Dict[str, bool]]: A dictionary containing the status of all services.
    """
    return services_status


@app.get("/status/{service_name}")
async def get_service_status(service_name: str) -> Dict[str, Any]:
    """
    Endpoint to get the status of a specific service.

    Args:
        service_name (str): The name of the service.

    Returns:
        Dict[str, Any]: A dictionary containing the service name and its status.

    Raises:
        HTTPException: If the service is not found.
    """
    for key, sub_services in services_status.items():
        if isinstance(sub_services, dict) and service_name in sub_services:
            return {"service": service_name, "status": sub_services[service_name]}
    raise HTTPException(status_code=404, detail="Service not found")


def init_websockets() -> None:
    """
    Initializes the websocket connections for various services.

    Exits the application if any initialization fails.
    """
    if ws.Websockets.init_board_i2c() != 0:
        exit(1)

    if ws.Websockets.init_ws_general() != 0:
        exit(1)

    if ws.Websockets.init_ws_external_sensor() != 0:
        exit(1)

    if ws.Websockets.init_ws_internal_sensor() != 0:
        exit(1)


init_websockets()
