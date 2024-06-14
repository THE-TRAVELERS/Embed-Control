import os


class Utils:
    """
    A class to represent a utility object.

    ...

    Methods
    -------
    unwrap_message(message: list) -> str:
        Unwraps a message from a list and returns it as a string.
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the utility object.
        """

        pass

    def unwrap_message(self, message):
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

    def clear_console(self):
        """
        Clears the console screen.
        """

        os.system("clear")
