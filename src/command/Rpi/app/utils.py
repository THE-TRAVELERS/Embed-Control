from typing import List, Callable, Any
from functools import wraps
from halo import Halo
import subprocess
import time
import os


class Utils:
    """
    A utility class providing methods for unwrapping messages, demonstrating loading spinners,
    applying loading decorators, getting Wi-Fi information, reading environment variables,
    and listing spinner types.
    """

    @staticmethod
    def clear_console() -> None:
        """
        Clears the console screen.

        This function uses the 'clear' command on Unix/Linux/Mac systems to clear the console screen.
        """
        os.system("clear")

    @staticmethod
    def unwrap_message(message: List[str]) -> str:
        """
        Unwraps the first string from a list of strings, removing the leading character and stripping quotes.

        Args:
            message (List[str]): A list of strings.

        Returns:
            str: The unwrapped message.

        Raises:
            ValueError: If the input is not a list of strings.
        """
        if not isinstance(message, list) or not all(
            isinstance(m, str) for m in message
        ):
            raise ValueError("Input must be a list of strings")
        return message[0][1:].strip("'")

    @staticmethod
    def loadings_demo(delay: int = 3) -> None:
        """
        Demonstrates various loading spinners with a dummy job.

        Args:
            delay (int): The delay in seconds for the dummy job. Defaults to 3.
        """

        def dummy_job() -> None:
            time.sleep(delay)

        for spinner_type in Utils.spinner_types:
            spinner = Halo(text=f"Loading using: {spinner_type}", spinner=spinner_type)
            spinner.start()
            dummy_job()
            spinner.stop()

    def loading(
        loading_message: str = "Loading...",
        success_message: str = "Loading complete.",
        failure_message: str = "Loading failed.",
        startup_time: float = 0.75,
        spinner_type: str = "line",
    ) -> Callable:
        """
        A decorator for adding a loading spinner to functions.

        Args:
            loading_message (str): The message displayed while loading.
            success_message (str): The message displayed on success.
            failure_message (str): The message displayed on failure.
            startup_time (float): The startup time before the function execution.
            spinner_type (str): The type of spinner to use.

        Returns:
            Callable: The decorated function.
        """

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                spinner = Halo(text=loading_message, spinner=spinner_type)
                spinner.start()
                time.sleep(startup_time)
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
    def get_wifi_info() -> int:
        """
        Checks the current Wi-Fi network name and validates it against a predefined value.

        Returns:
            int: 0 if the current Wi-Fi network is 'ntw_TRAVELERS', 1 otherwise.

        Raises:
            ValueError: If the current Wi-Fi network cannot be found.
            OSError: If the operating system is not supported.
        """
        if os.name == "posix" and os.uname().sysname == "Darwin":
            process = subprocess.Popen(
                ["networksetup", "-getairportnetwork", "en0"], stdout=subprocess.PIPE
            )
            out, _ = process.communicate()
            process.wait()
            if out:
                info = out.decode("utf-8").strip()
                if ": " in info:
                    _, val = info.split(": ", 1)
                    return 0 if val.strip() == "ntw_TRAVELERS" else 1
            raise ValueError("Current Wi-Fi Network not found")
        else:
            raise OSError("Unsupported OS")

    @staticmethod
    def read_variable(var_name: str) -> str:
        """
        Reads an environment variable.

        Args:
            var_name (str): The name of the environment variable.

        Returns:
            str: The value of the environment variable or None if not found.
        """
        return os.environ.get(var_name)

    spinner_types: List[str] = [
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
    """
    A list of spinner types supported by the Halo library.
    """
