import ItemBehaviors.PlasmaRay, ItemBehaviors.Detector,ItemBehaviors.SkectoLog
def behavior(name:str):
    match name:
        case "PlasmaRay":
            return ItemBehaviors.PlasmaRay
        case "Detector":
            return ItemBehaviors.Detector
        case "SkectoLog":
            return ItemBehaviors.SkectoLog
