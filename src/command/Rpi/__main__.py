from api import API
from utils import Utils
from dotenv import load_dotenv


@Utils.loading(
    "Loading environment variables...",
    "Environment variables loaded successfully.",
    "Failed to load environment variables.",
)
def load_variables():
    return 0 if load_dotenv() else 1


@Utils.loading(
    "Starting API...",
    "API started successfully.",
    "Failed to start API.",
)
def start_api():
    return project_api.run()


if __name__ == "__main__":
    try:
        load_variables()

        project_api = API()

        if start_api() != 0:
            exit(1)

        project_api.t_run.join()
    except KeyboardInterrupt:
        exit(0)
