import threading
from typing import Any, Dict
from fastapi import APIRouter, HTTPException

router: APIRouter = APIRouter()

t_run: threading.Thread
lock: threading.Lock = threading.Lock()
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
        "cpu_temperature": False,
        "cpu_usage": False,
        "ram_usage": False,
    },
}


@router.get("/")
async def ping() -> Dict[str, str]:
    """
    Endpoint to check the connection status of the server.

    Returns:
        Dict[str, str]: A dictionary with the connection status.
    """
    return {"Connection Status": "Active"}


@router.get("/status/all")
async def get_all_status() -> Dict[str, Dict[str, bool]]:
    """
    Endpoint to get the status of all services.

    Returns:
        Dict[str, Dict[str, bool]]: A dictionary containing the status of all services.
    """
    global services_status
    with lock:
        return services_status.copy()


@router.get("/status/{service_name}")
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
    global services_status
    with lock:
        for category, services in services_status.items():
            if service_name in services:
                return {"service": service_name, "status": services[service_name]}
        raise HTTPException(
            status_code=404,
            detail=f"Service '{service_name}' not found.",
        )
