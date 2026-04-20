import pickle
import os


FALLBACK_DIRECTORY = "GameCoreFiles"
def getFile(directory:str|os.PathLike,fname:str,fileType:str):
    fileType = fileType.lower()
    validFiletypes = ["area","dialogue","entity","texture"]
    if fileType not in validFiletypes:
        print(f"Error: {fileType} is invalid, expected one of {validFiletypes}")
        exit(1) 
    
    match fileType:
        case "area":
            midpart = "Areas"
        case "dialogues":
            midpart = "Dialogues"
        case "entity":
            midpart = "Entities"
        case "texture":
            midpart = "Texture"
    fullPath = os.path.join(directory,midpart,fname)
    if os.path.exists(fullPath) and os.path.isfile(fullPath):
        return fullPath
    
    fullPath = os.path.join(FALLBACK_DIRECTORY,midpart,fname)
    if os.path.exists(fullPath) and os.path.isfile(fullPath):
        return fullPath

    print(f"Error: cannot find {fileType} of name {fname} in {directory} or in fallback={FALLBACK_DIRECTORY}")
    exit(1)
    

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
