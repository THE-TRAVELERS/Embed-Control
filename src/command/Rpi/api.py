import threading
from fastapi import FastAPI, HTTPException
from utils import Utils
from threads import Threads


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
        ###############
        # ! Test
        "test": False,
        ##############
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

    @app.get("/ping")
    async def ping():
        return {"Connection Status": "Active"}

    @app.get("/status/all")
    async def get_all_status():
        return API.services_status

    @app.get("/status/{service_name}")
    async def get_service_status(service_name: str):
        service_status = API.services_status.get(service_name)
        if service_status is not None:
            return {"service": service_name, "status": service_status}
        else:
            for key in API.services_status:
                if (
                    isinstance(API.services_status[key], dict)
                    and service_name in API.services_status[key]
                ):
                    return {
                        "service": service_name,
                        "status": API.services_status[key][service_name],
                    }
            raise HTTPException(status_code=404, detail="Service not found")

    ####################################################################################################
    # ! Test
    # @app.post("/start/{service_name}")
    @app.post("/start/test")
    async def start_test():
        if API.services_status["test"]:
            raise HTTPException(status_code=400, detail="Service already running.")
        API.threads.start_test()
        API.services_status["test"] = True
        return {"service": "test", "status": API.services_status["test"]}

    ####################################################################################################
