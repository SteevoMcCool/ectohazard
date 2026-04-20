import pickle
import os

def load(directory: str):
    """
    load file from directory
    """
    file_path = os.path.join(directory, "savegame.dat")

    if not os.path.exists(file_path):
        print(f"File not exist: {file_path}")
        return None, None

    with open(file_path, "rb") as f:
        try:
            data = pickle.load(f)
            playerData = data.get("player")
            centerArea = data.get("area")
            return playerData, centerArea
        except Exception :
            print(f"Load file failed: {Exception}")
            return None, None


def unload(directory: str, playerData, centerArea):
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, "savegame.dat")

    data_to_save = {
        "player": playerData,
        "area": centerArea}

    with open(file_path, "wb") as f:
        pickle.dump(data_to_save, f)

    print(f"File saved to: {file_path}")
