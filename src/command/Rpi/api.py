import threading
from fastapi import FastAPI
from utils import Utils
from threads import Threads


def init_i2c(threads):
    if threads.i2c_utils.init_bus() != 0:
        exit(1)


class API:
    app: FastAPI = FastAPI()
    services_status = {
        "camera": False,
        "controller": False,
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
        self.t_run: threading.Thread
        self.threads = Threads()

        # init_i2c(self.threads)

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

    @app.get("/ping")
    async def ping():
        return {"Connection Status": "Active"}

    @app.get("/status/all")
    async def get_all_status():
        return API.services_status
