import os


class Utils:
    """
    Provides minor utility methods for the application.
    """

    def clear_console() -> None:
        """
        Clears the console screen.

        This function uses the 'clear' command on Unix/Linux/Mac systems to clear the console screen.
        """
        os.system("clear")
