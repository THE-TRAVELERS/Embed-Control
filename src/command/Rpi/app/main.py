import logging
from app.utils import Utils
from app.logs import Logs
from fastapi import FastAPI
from app.ws import WebSocketManager, router as ws_router
from app.routers.status import router as status_router

Utils.clear_console()
Logs.start()

app: FastAPI = FastAPI()

WebSocketManager.init_services()
app.include_router(ws_router)
app.include_router(status_router)

logging.debug("Registered routes:")
for route in app.routes:
    logging.debug(f" + {route.name}: {route.path}")