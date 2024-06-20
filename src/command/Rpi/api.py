import asyncio
import threading
from fastapi import FastAPI, HTTPException, WebSocket
from utils import Utils
from threads import Threads
from functools import wraps


def init_i2c(threads: Threads):
    if threads.i2c_utils.init_bus() != 0:
        exit(1)


def init_threads(threads: Threads):
    if threads.init_threads() != 0:
        exit(1)


class API:
    threads: Threads = Threads()
    app: FastAPI = FastAPI()
    t_run: threading.Thread

    services_status = {
        "general": {
            "camera": False,
            "controller": False,
            ###############
            # ! Test
            "debug_ws": False,
            ##############
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
        # init_i2c(self.threads)
        init_threads(self.threads)

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

    ####################################################################################################
    # ! Test
    # @app.post("/start/debug")
    # async def start_test():
    #     if API.services_status["debug"]:
    #         raise HTTPException(status_code=400, detail="Service already running.")
    #     API.threads.start_debug_ws()
    #     API.services_status["debug"] = True
    #     return {"service": "debug", "status": API.services_status["debug"]}

    ####################################################################################################

    # @app.websocket("/general/debug")
    # async def websocket_endpoint(websocket: WebSocket):
    #     await websocket.accept()
    #     try:
    #         if API.services_status["debug_ws"]:
    #             raise Exception("Service already running.")
    #         else:
    #             API.services_status["debug_ws"] = True

    #         count = 0
    #         while True:
    #             await websocket.send_text(str(count))
    #             count += 1
    #             await asyncio.sleep(1)
    #     except Exception:
    #         API.services_status["debug_ws"] = False

    # @app.websocket("/{ws_category}/{ws_name}")
    # async def websocket_endpoint(websocket: WebSocket, ws_category: str, ws_name: str):
    #     await websocket.accept()
    #     try:
    #         if API.services_status[ws_category][ws_name]:
    #             raise Exception("Service already running.")
    #         else:
    #             API.services_status[ws_category][ws_name] = True

    #         ###############################################
    #         # TODO: Replace
    #         count = 0
    #         while True:
    #             await websocket.send_text(str(count))
    #             count += 1
    #             await asyncio.sleep(1)
    #         ###############################################

    #     except Exception:
    #         API.services_status[ws_category][ws_name] = False


def setup_websocket_service(ws_category: str, ws_name: str, func):
    @API.app.websocket(f"/{ws_category}/{ws_name}")
    @wraps(func)
    async def wrapper(websocket: WebSocket):
        await websocket.accept()
        try:
            if API.services_status[ws_category][ws_name]:
                raise Exception("Service already running.")
            else:
                API.services_status[ws_category][ws_name] = True
            await func(websocket)
        except Exception:
            API.services_status[ws_category][ws_name] = False

    return wrapper


async def my_websocket_service(websocket: WebSocket):
    count = 0
    while True:
        await websocket.send_text(str(count))
        count += 1
        await asyncio.sleep(1)


setup_websocket_service("general", "debug_ws", my_websocket_service)
