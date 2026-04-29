import math
from pygame import Vector2
from random import random
from listOfLists import *
from wall_ray_camera import Ray
def update(self,gameApp): 
    """
        Function to be called every tick
        Parameters:
            self: the Entity described by the file 
                ...
    """
    if self.hp <= 0:
        self.radius = 0
        return
    dt = gameApp.dt 
    player = gameApp.player
    ppos = player.camera.center.pos
    epos = self.pos
    dpos:Vector2 = (ppos-epos)
    angle= math.atan2(dpos.y, dpos.x)

    walls = ListOfLists(area.walls for area in gameApp.areas.loadedAreas.values())
    entities =  ListOfLists(area.entities for area in gameApp.areas.loadedAreas.values())
    hit =  Ray(epos,angle).firstContact(walls)
    if hit:
        (wall,cp) = hit
        if (cp - epos).magnitude() < (ppos - epos).magnitude(): #wall is closer, cannot see player 
            return ;

    LV:Ray = player.camera.center
    LV = LV.lookVector().normalize()
    V2 = -dpos.normalize()
    cosSim = LV.x*V2.x + LV.y*V2.y
    if cosSim > 0.95:
        atk = self.atk
        defc = gameApp.player.defc
        bdmg =  dt* atk
        gameApp.player.hp -=  bdmg * (atk+5)/(atk+defc+5)
        self.pos += Vector2(random()-0.5,random()-0.5)/5
        self.radius+= 0.37*dt
    else: 
        self.radius-= 0.37*dt 
    self.radius = max(min(self.radius,1),0.5)
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
 


def chatted(self,response:int|str,gameApp):
    pass
    



