from utils import Utils
from i2c import I2CUtils


def check_wifi():
    if Utils.get_wifi_info() != 0:
        exit(1)


def init_i2c():
    i2c = I2CUtils()
    if i2c.init_bus() != 0:
        exit(1)


if __name__ == "__main__":
    # check_wifi()

    # init_i2c()
    pass
