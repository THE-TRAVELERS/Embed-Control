import logging
from smbus2 import SMBus
from typing import Any, Optional

# import board
# from busio import I2C
# import adafruit_bme680

I2C_CHANNEL = 1
I2C_SLAVE_ADDRESS = 0x11
DEFAULT_CAMERA_WIDTH = 640
DEFAULT_CAMERA_HEIGHT = 480
DEFAULT_CAMERA_FORMAT = "RGB888"


class I2CUtils:
    """
    Provides utility methods for I2C communication between the Raspberry Pi and the ESP32.
    """

    slave_address: int = I2C_SLAVE_ADDRESS
    bus: Optional[SMBus] = SMBus(I2C_CHANNEL)

    # i2c: I2C = I2C(board.SCL, board.SDA)
    bme680: Any

    camera: Any

    @classmethod
    def init_bme680(cls, debug: bool = False) -> bool:
        """
        Initializes the BME680 sensor.

        Args:
            debug: Whether to enable debug mode.
        """
        logging.debug(f"[SENSORS] BME680 settings: debug={debug}")
        try:
            # cls.bme680 = adafruit_bme680.Adafruit_BME680_I2C(cls.i2c, debug=debug)
            logging.info("[SENSORS] BME680 Deprecated.")
            return False
            # return True
        except Exception as e:
            logging.error(f"[SENSORS] Error initializing BME680: {e}")
            return False

    @classmethod
    def init_camera(
        cls,
        width: int = DEFAULT_CAMERA_WIDTH,
        height: int = DEFAULT_CAMERA_HEIGHT,
        format: str = DEFAULT_CAMERA_FORMAT,
    ) -> bool:
        """
        Initializes the camera.

        Args:
            width: The width of the camera feed.
            height: The height of the camera feed.
            format: The format of the camera feed.
        """
        logging.debug(
            f"[SENSORS] Picamera settings: width={width}, height={height}, format={format}"
        )
        try:
            from picamera2 import Picamera2

            cls.camera = Picamera2()

            cls.camera.video_configuration.main.size = (width, height)
            cls.camera.video_configuration.main.format = format
            cls.camera.video_configuration.align()
            cls.camera.configure("video")
            logging.info("[SENSORS] Picamera initialized.")
            return True
        except Exception as e:
            logging.error(f"[SENSORS] Error initializing Picamera: {e}")
            return False

    @classmethod
    def convert_string_to_bytes(cls, val: str) -> list[int]:
        """Converts a string to a list of bytes.

        Args:
            val: The string to convert.

        Returns:
            A list of integers representing the ASCII values of the characters in the string.
        """
        return [ord(c) for c in val]

    @classmethod
    def write_data(cls, value: str):
        """Writes a string to the I2C bus as a block of data.

        Args:
            value: The string to write.

        Raises:
            Exception: Propagates any exceptions raised by write_i2c_block_data.
        """
        logging.debug(f"[I2C] Writing data: {value}")
        byte_value: list[int] = cls.convert_string_to_bytes(value)
        logging.debug(f"[I2C] Writing data: {byte_value}")
        try:
            cls.bus.write_i2c_block_data(cls.slave_address, 0x00, byte_value)
        except Exception as e:
            logging.error(f"[I2C] Error writing data: {e}")
            raise e
