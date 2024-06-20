from api import API
from utils import Utils


@Utils.loading(
    "Starting API...",
    "API started successfully.",
    "Failed to start API.",
    1,
)
def start_api():
    return project_api.run()


if __name__ == "__main__":
    try:
        project_api = API()

        if start_api() != 0:
            exit(1)

        project_api.t_run.join()
    except KeyboardInterrupt:
        exit(0)
