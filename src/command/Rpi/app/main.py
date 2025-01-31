from app.utils import Utils
from app.logs import Logs
from app.ws import WebSocketManager

Utils.clear_console()
Logs.start()
WebSocketManager.init_services()
