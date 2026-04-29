SPEED = 5
SIGHTRANGE = 20
ATKRANGE = 2
MAXDISTANCEFROMBASE = 2
global TARGETPOINT,WANDERBASEPOSITION 
TARGETPOINT = None
WANDERBASEPOSITION = None
import math
import random
from pygame import Vector2
from listOfLists import * 
from wall_ray_camera import Ray
def sign(num):
    return 1 if num >= 0 else -1
def update(self,gameApp): 
    global TARGETPOINT,WANDERBASEPOSITION
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
    dpos = (ppos-epos)
    angle= math.atan2(dpos.y, dpos.x)
    if dpos.magnitude() > SIGHTRANGE:
        mode = "wander"
    elif dpos.magnitude() < ATKRANGE:
        atk = self.atk
        defc = gameApp.player.defc
        bdmg =  dt* atk
        gameApp.player.hp -=  bdmg * (atk+5)/(atk+defc+5)
        mode ="target"
        TARGETPOINT = ppos*1
    else:
        walls = ListOfLists(area.walls for area in gameApp.areas.loadedAreas.values())
        entities =  ListOfLists(area.entities for area in gameApp.areas.loadedAreas.values())
        hit =  Ray(epos,angle).firstContact(walls)
        mode = "wander"
        if hit:
            (wall,cp) = hit
            if (cp - epos).magnitude() >= (ppos - epos).magnitude(): #wall is further, can see player 
                mode = "target"
                TARGETPOINT = ppos * 1 #needed for copying
                WANDERBASEPOSITION = None

    if  mode == "target":
        if (TARGETPOINT.distance_to(self.pos) < ATKRANGE/2):
            TARGETPOINT = None 
        else:
            self.pos += SPEED*dt*Vector2(math.cos(angle),math.sin(angle))
      
    elif mode == "wander":
        if not WANDERBASEPOSITION:
            WANDERBASEPOSITION = self.pos * 1 #needed for copying   
        dx = self.pos.x - WANDERBASEPOSITION.x 
        dy = self.pos.y - WANDERBASEPOSITION.y
        r = random.random()
        mx = sign(2*MAXDISTANCEFROMBASE*r - MAXDISTANCEFROMBASE - dx)
        r = random.random()
        my = sign(2*MAXDISTANCEFROMBASE*r - MAXDISTANCEFROMBASE - dy)
        self.pos += SPEED*dt*Vector2(mx,my)


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
    



