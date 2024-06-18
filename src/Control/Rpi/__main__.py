from threads import Threads

######################################
# Feature for pc_main.py
#
# def check_wifi():
#     if Utils.get_wifi_info() != 0:
#         exit(1)
######################################


def init_i2c(threads):
    if threads.i2c_utils.init_bus() != 0:
        exit(1)


if __name__ == "__main__":
    try:
        threads = Threads()
        init_i2c(threads)
    except KeyboardInterrupt:
        exit(0)
