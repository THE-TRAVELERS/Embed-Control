import os
import subprocess
from halo import Halo
from functools import wraps
import time


class Utils:
    spinner_type = "line"

    def unwrap_message(message):
        if not isinstance(message, list) or not all(
            isinstance(m, str) for m in message
        ):
            raise ValueError("Input must be a list of strings")

        unwrapped_message = str(message[0])
        unwrapped_message = unwrapped_message[1:].strip("'")
        return unwrapped_message

    def clear_console():
        os.system("clear")

    def loadings_demo(delay=3) -> None:
        def dummy_job():
            time.sleep(delay)

        list = [
            "dots",
            "dots2",
            "dots3",
            "dots4",
            "dots5",
            "line",
            "line2",
            "pipe",
            "star",
            "star2",
            "flip",
            "hamburger",
            "growVertical",
            "growHorizontal",
            "squareCorners",
            "circleHalves",
            "balloon",
            "balloon2",
            "noise",
            "bounce",
            "boxBounce",
            "boxBounce2",
            "triangle",
            "arc",
            "circle",
            "circleCorners",
            "bouncingBar",
            "bouncingBall",
            "earth",
            "moon",
            "pong",
            "shark",
            "dqpb",
        ]
        for i in list:
            spinner = Halo(text=f"Loading using: {i}", spinner=i)
            spinner.start()
            dummy_job()
            spinner.stop()

    def loading(
        loading_message="Loading...",
        success_message="Loading complete.",
        failure_message="Loading failed.",
    ):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                spinner = Halo(text=loading_message, spinner=Utils.spinner_type)
                spinner.start()
                time.sleep(1)

                try:
                    result = func(*args, **kwargs)
                    spinner.succeed(success_message) if result == 0 else spinner.fail(
                        failure_message
                    )
                    return result
                except Exception as e:
                    spinner.fail(str(e))

            return wrapper

        return decorator

    @loading(
        "Checking Wi-Fi host...",
        "Wi-Fi hostname correct",
        "Wi-Fi hostname incorrect, please connect to the 'ntw_TRAVELERS' to access further features.",
    )
    def get_wifi_info():
        if os.name == "posix" and os.uname().sysname == "Darwin":
            process = subprocess.Popen(
                ["networksetup", "-getairportnetwork", "en0"],
                stdout=subprocess.PIPE,
            )
            out, _ = process.communicate()
            process.wait()
            wifi_info = {}
            if out:
                info = out.decode("utf-8").strip()
                if ": " in info:
                    key, val = info.split(": ", 1)
                    wifi_info[key.strip()] = val.strip()
            return 0 if wifi_info["Current Wi-Fi Network"] == "ntw_TRAVELERS" else 1
        else:
            raise OSError("Unsupported OS")

    def read_variable(var_name):
        try:            
            return os.environ[var_name]

        except KeyError:
            return None
