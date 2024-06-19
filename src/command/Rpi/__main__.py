import api
from utils import Utils
from threads import Threads
from dotenv import load_dotenv


######################################
# Feature for pc_main.py
#
# def check_wifi():
#     if Utils.get_wifi_info() != 0:
#         exit(1)
######################################


@Utils.loading(
    "Loading environment variables...",
    "Environment variables loaded successfully.",
    "Failed to load environment variables.",
)
def load_variables():
    return 0 if load_dotenv() else 1


@Utils.loading(
    "Starting API...",
    "API started successfully.",
    "Failed to start API.",
)
def start_api():
    return api.api().run()


def init_i2c(threads):
    if threads.i2c_utils.init_bus() != 0:
        exit(1)


if __name__ == "__main__":
    try:
        load_variables()

        start_api()

        # threads = Threads()
        # init_i2c(threads)
    except KeyboardInterrupt:
        exit(0)
