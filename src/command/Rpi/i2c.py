import smbus2 as smbus  # smbus2 not tested yet initially used smbus
from utils import Utils


class I2CUtils:
    def __init__(self, channel=1, slave_address=0x11):
        self.channel = channel
        self.slave_address = slave_address
        self.bus = None

    @Utils.loading(
        "Initializing I2C bus...",
        "I2C bus initialized successfully.",
        "Failed to initialize I2C bus. Please ensure that the program is run from a Raspberry Pi.",
    )
    def init_bus(self):
        try:
            self.bus = smbus.SMBus(self.channel)
            return 0
        except Exception:
            return 1

    def convert_string_to_bytes(self, val):
        if not isinstance(val, str):
            raise ValueError("Input must be a string")

        return [ord(c) for c in val]

    def write_data(self, value, i2c_address=None):
        if i2c_address is None:
            i2c_address = self.slave_address

        byte_value = self.convert_string_to_bytes(value)

        try:
            self.bus.write_i2c_block_data(i2c_address, 0x00, byte_value)
        except Exception as e:
            raise e

        return 0  # updated from -1 to 0
