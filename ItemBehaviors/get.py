import ItemBehaviors.PlasmaRay, ItemBehaviors.Communicator
def behavior(name:str):
    match name:
        case "PlasmaRay":
            return ItemBehaviors.PlasmaRay
        case "Communicator":
            return ItemBehaviors.Communicator
