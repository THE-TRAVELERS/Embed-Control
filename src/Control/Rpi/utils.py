import os
from halo import Halo
from functools import wraps
import time


class Utils:
    """
    A class to represent a utility object.

    ...

    Methods
    -------
    unwrap_message(message: list) -> str:
        Unwraps a message from a list and returns it as a string.
    """

    spinner_type = "boxBounce2"

    def unwrap_message(message):
        """
        Unwraps a message from a list and returns it as a string.

        Parameters
        ----------
            message : list
                a list containing a single string

        Returns
        -------
            str
                a string representing the unwrapped message
        """
        if not isinstance(message, list) or not all(
            isinstance(m, str) for m in message
        ):
            raise ValueError("Input must be a list of strings")

        unwrapped_message = str(message[0])
        unwrapped_message = unwrapped_message[1:].strip("'")
        return unwrapped_message

    def clear_console():
        """
        Clears the console screen.
        """
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
                try:
                    result = func(*args, **kwargs)
                    spinner.succeed(success_message) if result == 0 else spinner.fail(
                        failure_message
                    )
                except Exception as e:
                    spinner.fail(str(e))

            return wrapper

        return decorator
