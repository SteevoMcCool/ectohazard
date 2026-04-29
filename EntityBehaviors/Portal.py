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
    pass


def approached(self,approacher,gameApp):
    """
        Function to be called when another entity|player gets close
        Parameters:
            self: the Entity described by the file 
                ...
    """
    gameApp.player.camera.center.pos = Vector2(260,200)
    gameApp.player.inventory.items = []
    gameApp.player.inventory.load(["PlasmaRay","Detector","SkectoLog"])

def actionKeyPressed(self,gameApp):
    """
        Function to be called when the player is nearby and presses the action key (defaults to E/F)
        Parameters:
            self: the Entity described by the file 
            approacher: the Entity|Player that approached 
                ...
    """
    pass
 


def chatted(self,response:int|str,gameApp):
    pass
    



