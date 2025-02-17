import logging
import requests

DEFAULT_MAX_ATTEMPTS = 5


class ServerPinger:
    """
    Pings the server at the specified address and checks for an active status.
    """

    def __init__(self, server_address: str, max_attempts: int = DEFAULT_MAX_ATTEMPTS):
        self.server_address = server_address
        if max_attempts < 1:
            logging.warning(
                f"[ServerPinger] Max attempts should be at least 1 but given: {max_attempts}. Setting to default: {DEFAULT_MAX_ATTEMPTS}"
            )
            max_attempts = DEFAULT_MAX_ATTEMPTS
        self.max_attempts = max_attempts
        logging.info("[ServerPinger] Initialized.")

    def ping(self) -> bool:
        for attempt in range(self.max_attempts):
            try:
                response = requests.get(self.server_address)
                data = response.json()
                status = data.get("Connection Status") == "Active"
                logging.info(f"[ServerPinger] Server status: {status}")
                return status
            except Exception as e:
                logging.error(
                    f"[ServerPinger] Error pinging server on attempt {attempt + 1}: {e}"
                )
        return False
