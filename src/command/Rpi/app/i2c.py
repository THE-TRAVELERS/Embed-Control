import smbus2 as smbus  # ! smbus2 not tested yet initially used smbus
from typing import Optional


class I2CUtils:
    def __init__(self, channel=1, slave_address=0x11):
        self.channel: int = channel
        self.slave_address: int = slave_address
        self.bus: Optional[smbus.SMBus] = None

    def init_bus(self) -> int:
        """Initializes the I2C bus.

        Returns:
            0 if the bus was successfully initialized, 1 otherwise.
        """
        try:
            self.bus = smbus.SMBus(self.channel)
            return 0
        except Exception:
            return 1

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

    def write_data(self, value: str, i2c_address: int = None):
        """Writes a string to the I2C bus as a block of data.

        Args:
            value: The string to write.
            i2c_address: The I2C address to write to. Defaults to the object's slave_address.

        Raises:
            Exception: Propagates any exceptions raised by write_i2c_block_data.
        """
        if i2c_address is None:
            i2c_address = self.slave_address

        byte_value: list[int] = self.convert_string_to_bytes(value)

        try:
            self.bus.write_i2c_block_data(i2c_address, 0x00, byte_value)
        except Exception as e:
            raise e
