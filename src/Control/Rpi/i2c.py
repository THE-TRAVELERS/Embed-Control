import smbus2 as smbus
from utils import Utils


class I2CUtils:
    """
    A class to represent an I2C interface.

    ...

    Attributes
    ----------
    channel : int
        an integer representing the I2C channel (default 1)
    slave_address : int
        an integer representing the I2C address of the slave device (default 0x11)
    bus : smbus.SMBus
        an SMBus instance representing the I2C bus

    Methods
    -------
    convert_string_to_bytes(val: str) -> list:
        Converts a string to a list of ASCII values.
    write_data(value: str, i2c_address: int = None) -> int:
        Writes a string of data to an I2C device.
    """

    def __init__(self, channel=1, slave_address=0x11):
        """
        Constructs all the necessary attributes for the I2C object.

        Parameters
        ----------
            channel : int
                an integer representing the I2C channel (default 1)
            slave_address : int
                an integer representing the I2C address of the slave device (default 0x11)
        """
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
        """
        Converts a string to a list of ASCII values.

        Parameters
        ----------
            val : str
                a string to be converted

        Returns
        -------
            list
                a list of ASCII values
        """

        if not isinstance(val, str):
            raise ValueError("Input must be a string")

        return [ord(c) for c in val]

    def write_data(self, value, i2c_address=None):
        """
        Writes a string of data to an I2C device.

        Parameters
        ----------
            value : str
                a string of data to be written
            i2c_address : int, optional
                an integer representing the I2C address of the device (default is None, which means use self.slave_address)

        Returns
        -------
            int
                0 if the operation is successful
        """

        if i2c_address is None:
            i2c_address = self.slave_address

        byte_value = self.convert_string_to_bytes(value)

        try:
            self.bus.write_i2c_block_data(i2c_address, 0x00, byte_value)
        except Exception as e:
            print(f"Failed to write data: {e}")
            return

        return 0 # updated from -1 to 0
