import EntityBehaviors.Albert, EntityBehaviors.Blank, EntityBehaviors.BasicEnemy, EntityBehaviors.Portal, EntityBehaviors.Peeker,EntityBehaviors.HalfApparation,EntityBehaviors.Mouther
def behavior(name:str):
    match name:
        case "Albert":
            return EntityBehaviors.Albert
        case "Erdon":
            return EntityBehaviors.BasicEnemy
        case "HalfApparation":
            return EntityBehaviors.HalfApparation
        case "Portal":
            return EntityBehaviors.Portal
        case "Peeker":
            return EntityBehaviors.Peeker
        case "Mouther":
            return EntityBehaviors.Mouther
    return EntityBehaviors.Blank
