from utils import Utils


if __name__ == "__main__":
    if Utils.get_wifi_info() != 0:
        exit(1)
