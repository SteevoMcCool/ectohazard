# Globals that hold save files
CORE_FILE_PATH = "./GameCoreFiles"
SAVES_FILE_PATH = "./GameSaves"

# Globals that hold gamefile paths
AREA_PATH = f"{CORE_FILE_PATH}/Areas"
TEXTURE_PATH = f"{CORE_FILE_PATH}/Textures"
DIALOGUE_PATH = f"{CORE_FILE_PATH}/Dialogues"
ENTITIES_PATH = f"{CORE_FILE_PATH}/Entities"




import os
FALLBACK_DIRECTORY = "GameCoreFiles"
def getFile(directory:str|os.PathLike,fname:str,fileType:str):
    fileType = fileType.lower()
    validFiletypes = ["area","dialogue","entity","texture","item"]
    if fileType not in validFiletypes:
        print(f"Error: {fileType} is invalid, expected one of {validFiletypes}")
        exit(1) 
    
    match fileType:
        case "area":
            midpart = "Areas"
        case "dialogue":
            midpart = "Dialogues"
        case "entity":
            midpart = "Entities"
        case "texture":
            midpart = "Textures"
        case "item":
            midpart = "InventoryItems"
    fullPath = os.path.join(directory,midpart,fname)
    if os.path.exists(fullPath) and os.path.isfile(fullPath):
        return fullPath
    
    fullPath = os.path.join(FALLBACK_DIRECTORY,midpart,fname)
    if os.path.exists(fullPath) and os.path.isfile(fullPath):
        return fullPath

    print(f"Error: cannot find {fileType} of name {fname} in {directory} or in fallback={FALLBACK_DIRECTORY}")
    exit(1)


def getFileToWrite(directory:str|os.PathLike,fname:str,fileType:str):
    fileType = fileType.lower()
    validFiletypes = ["area","dialogue","entity","texture","item"]
    if fileType not in validFiletypes:
        print(f"Error: {fileType} is invalid, expected one of {validFiletypes}")
        exit(1) 
    
    match fileType:
        case "area":
            raise ValueError("Area files not mutable")
        case "dialogue":
            raise ValueError("Dialogue files not mutable")
        case "entity":
            midpart = "Entities"
        case "texture":
            raise ValueError("Texture files not mutable")
        case "item":
            midpart = "InventoryItems"

    fullPath = os.path.join(directory,midpart,fname)
    return fullPath