import time
from threads import Threads
from utils import Utils

if __name__ == "__main__":
    threads = Threads()
    utils = Utils()

    while True:
        # TODO: Add Menu
        choice = input(
            "1. Activer/Désactiver le retour vidéo\n"
            + "2. Connecter/Déconnecter la manette PS4\n"
            + "3. Clear Console\n"
        )

        if choice == "1":
            # TODO: Add camera capturing
            is_camera_active = not threads.is_camera_active

        elif choice == "2":
            # TODO: Add PS4 controller connection
            is_controller_active = not threads.is_controller_active

        elif choice == "3":
            utils.clear_console()
        else:
            print("Error: Invalid choice!")
        time.sleep(1)
        utils.clear_console()
