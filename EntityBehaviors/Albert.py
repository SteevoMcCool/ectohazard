SPEED = 5
import math
from pygame import Vector2
def update(self,gameApp): 
    """
        Function to be called every tick
        Parameters:
            self: the Entity described by the file 
                ...
    """
    player = gameApp.player
    ppos = player.camera.center.pos
    epos = self.pos
    dpos = (ppos - epos)
    if dpos.magnitude() > 5:
       dt = gameApp.dt 
       angle= math.atan2(dpos.y, dpos.x)
       self.pos += SPEED*dt*Vector2(math.cos(angle),math.sin(angle))



def approached(self,approacher,gameApp):
    """
        Function to be called when another entity|player gets close
        Parameters:
            self: the Entity described by the file 
                ...
    """
    gameApp.displayDialogueYield(self, "Want to talk? Just press your [Action Key] (E / F)")



def actionKeyPressed(self,gameApp):
    """
        Function to be called when the player is nearby and presses the action key (defaults to E/F)
        Parameters:
            self: the Entity described by the file 
            approacher: the Entity|Player that approached 
                ...
    """
    if (self.dialogueLine == 3 and gameApp.player.invSlotEquipped == 0):
        self.dialogueLine= 4
    elif (self.dialogueLine == 9 and gameApp.player.invSlotEquipped == 1):
        self.dialogueLine=10

    gameApp.displayDialogueYield(self,self.dialogue.text(self.dialogueLine),self.dialogue.options(self.dialogueLine))
 


def chatted(self,response:int|str,gameApp):
    if (response <= 0):
        print("Got: 0")
    else:
        if (nextLine:= self.dialogue.next(self.dialogueLine,int(response)-1)) == 0:
            pass           
        else:
            self.dialogueLine = nextLine
            if nextLine == 3:
                gameApp.player.inventory.load(["PlasmaRay"])
                gameApp.displayDialogueYield(self,self.dialogue.text(self.dialogueLine),self.dialogue.options(self.dialogueLine))

            elif nextLine == 9:
                gameApp.player.inventory.load(["Detector"])
            elif nextLine == 15:
                gameApp.player.inventory.load(["SkectoLog"])
                gameApp.displayDialogueYield(self,self.dialogue.text(self.dialogueLine),self.dialogue.options(self.dialogueLine))
            else:
                gameApp.displayDialogueYield(self,self.dialogue.text(self.dialogueLine),self.dialogue.options(self.dialogueLine))

    



