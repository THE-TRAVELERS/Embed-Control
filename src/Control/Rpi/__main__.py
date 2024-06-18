import time
from utils import Utils


@Utils.loading()
def dummy():
    time.sleep(5)
    raise Exception("An error occurred")
    return 1


if __name__ == "__main__":
    dummy()
