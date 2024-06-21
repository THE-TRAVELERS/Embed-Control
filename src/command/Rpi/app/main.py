from fastapi import FastAPI, HTTPException
import threading

from . import ws


app: FastAPI = FastAPI()
t_run: threading.Thread
services_status = {
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
async def ping():
    return {"Connection Status": "Active"}


@app.get("/status/all")
async def get_all_status():
    return services_status


@app.get("/status/{service_name}")
async def get_service_status(service_name: str):
    for key, sub_services in services_status.items():
        if isinstance(sub_services, dict) and service_name in sub_services:
            return {"service": service_name, "status": sub_services[service_name]}
    raise HTTPException(status_code=404, detail="Service not found")


def init_websockets():
    if ws.Websockets.init_board_i2c() != 0:
        exit(1)

    if ws.Websockets.init_ws_general() != 0:
        exit(1)

    if ws.Websockets.init_ws_external_sensor() != 0:
        exit(1)

    if ws.Websockets.init_ws_internal_sensor() != 0:
        exit(1)


init_websockets()
