import logging
from smbus2 import SMBus
from typing import Optional
from picamera2 import Picamera2

import board
from busio import I2C
import adafruit_bme680

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

    i2c: I2C = I2C(board.SCL, board.SDA)
    bme680: adafruit_bme680.Adafruit_BME680_I2C

    camera: Picamera2

    @classmethod
    def init_bme680(cls, debug: bool = False) -> None:
        """
        Initializes the BME680 sensor.

        Args:
            debug: Whether to enable debug mode.
        """
        logging.debug(f"[SENSORS] BME680 settings: debug={debug}")
        cls.bme680 = adafruit_bme680.Adafruit_BME680_I2C(cls.i2c, debug=debug)
        logging.info("[SENSORS] BME680 initialized.")

    @classmethod
    def init_camera(
        cls,
        width: int = DEFAULT_CAMERA_WIDTH,
        height: int = DEFAULT_CAMERA_HEIGHT,
        format: str = DEFAULT_CAMERA_FORMAT,
    ) -> None:
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
        cls.camera = Picamera2()

        cls.camera.video_configuration.main.size = (width, height)
        cls.camera.video_configuration.main.format = format
        cls.camera.video_configuration.align()
        cls.camera.configure("video")
        logging.info("[SENSORS] Picamera initialized.")

    def convert_string_to_bytes(self, val: str) -> list[int]:
        """Converts a string to a list of bytes.

        Args:
            val: The string to convert.

        Returns:
            A list of integers representing the ASCII values of the characters in the string.

        Raises:
            TypeError: If the input is not a string.
        """
        if not isinstance(val, str):
            raise TypeError("Input must be a string")
        return [ord(c) for c in val]

    def write_data(self, value: str):
        """Writes a string to the I2C bus as a block of data.

        Args:
            value: The string to write.

        Raises:
            Exception: Propagates any exceptions raised by write_i2c_block_data.
        """
        byte_value: list[int] = self.convert_string_to_bytes(value)

        try:
            self.bus.write_i2c_block_data(self.slave_address, 0x00, byte_value)
        except Exception as e:
            raise e
