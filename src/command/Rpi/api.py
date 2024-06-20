from fastapi import FastAPI, HTTPException
import ws
from utils import Utils
import threading


def init_websockets():
    if ws.Websockets.init_board_i2c() != 0:
        exit(1)

    if ws.Websockets.init_ws_general() != 0:
        exit(1)

    if ws.Websockets.init_ws_external_sensor() != 0:
        exit(1)

    if ws.Websockets.init_ws_internal_sensor() != 0:
        exit(1)


class API:
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

    def __init__(self):
        init_websockets()

    def run(self):
        try:
            import uvicorn

            self.t_run = threading.Thread(
                target=uvicorn.run,
                args=(self.app,),
                kwargs={
                    "host": Utils.read_variable("LOCAL_ADDRESS"),
                    "port": int(Utils.read_variable("API_PORT")),
                    "log_level": "error",
                },
            )
            self.t_run.start()

            return 0
        except Exception:
            return 1

    @app.get("/")
    async def ping():
        return {"Connection Status": "Active"}

    @app.get("/status/all")
    async def get_all_status():
        return API.services_status

    @app.get("/status/{service_name}")
    async def get_service_status(service_name: str):
        for key, sub_services in API.services_status.items():
            if isinstance(sub_services, dict) and service_name in sub_services:
                return {"service": service_name, "status": sub_services[service_name]}

        raise HTTPException(status_code=404, detail="Service not found")
