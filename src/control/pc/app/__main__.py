import logging
import platform
from logs import Logs
from models.server_pinger import ServerPinger
from keyboard_input_handler import KeyboardInputHandler
from controller_input_handler import ControllerInputHandler
import threading

# Server address:
# For development
# SERVER = "localhost"
# For production
SERVER = "travelers5.local"

SERVER_HTTP_ADDRESS = f"http://{SERVER}:8765/"
SERVER_WS_ADDRESS = f"ws://{SERVER}:8765/"
CONTROLLER_URL = SERVER_WS_ADDRESS + "general/controller"
LINUX_CONTROLLER_INTERFACE = "/dev/input/js0"

Logs.start()

pinger = ServerPinger(SERVER_HTTP_ADDRESS)
if not pinger.ping():
    logging.critical("[Main] Server is not active. Exiting.")
    exit()
if platform.system() == "Linux":
    logging.info("[Main] Using controller input.")
    input_handler = ControllerInputHandler(CONTROLLER_URL, LINUX_CONTROLLER_INTERFACE)
else:
    logging.info("[Main] Using keyboard input.")
    input_handler = KeyboardInputHandler(CONTROLLER_URL)

logging.info("[Main] Starting input handler.")
input_thread = threading.Thread(target=input_handler.handle_input)
input_thread.start()
input_handler.start()
