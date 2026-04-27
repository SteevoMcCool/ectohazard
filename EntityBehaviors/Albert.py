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
    pass



def actionKeyPressed(self,gameApp):
    """
        Function to be called when the player is nearby and presses the action key (defaults to E/F)
        Parameters:
            self: the Entity described by the file 
            approacher: the Entity|Player that approached 
                ...
    """
    pass
 


