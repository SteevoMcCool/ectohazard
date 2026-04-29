import EntityBehaviors.Albert, EntityBehaviors.Blank, EntityBehaviors.BasicEnemy, EntityBehaviors.Portal, EntityBehaviors.Peeker
def behavior(name:str):
    match name:
        case "Albert":
            return EntityBehaviors.Albert
        case "Erdon":
            return EntityBehaviors.BasicEnemy
        case "Portal":
            return EntityBehaviors.Portal
        case "Peeker":
            return EntityBehaviors.Peeker
    return EntityBehaviors.Blank
