from pygame import * 
from wall_ray_camera import *
from controller import * 


class Area:
    #TODO- must read from an .atxt file that has walls and other info
    def __init__(self,id):
        pass


MAPAREAWIDTH = 32 #the amount of areas in a row of the total map There can be gaps/jumps
""" 
so, the map looks like: 

    [00][01][02]...[31]
    [32][33][34]...[63]
    [64][65][66].......
    ...................

where those are the area numbers. only 9 areas will be loaded in at a time.
There can be blank areas, or entire columns of blank areas if they dont connect. that's fine.
"""

AREA_SIZE = 1000 #the size (height and width) of each individual area 

class AreaLoader:

    def __init__(self):
        self.loadedAreas = {}
        self.currentCenter = 0

    def loadAround(self,center:int): 
        #loads all the areas in a 3x3 grid, with the specified area being in the center
        if center == self.currentCenter:
            return 0
        above = max(center - MAPAREAWIDTH,0)
        below = center + MAPAREAWIDTH 
        left = max(center - 1,0) % MAPAREAWIDTH 
        right = min(center + 1,MAPAREAWIDTH-1) % MAPAREAWIDTH
        numLoads = 0
        for row in range(above,below+1,32):
            for col in range(left,right+1):
                id= row + col 
                if  not self.loadedAreas.get(id):
                    self.loadedAreas[id] = Area(id)
                    numLoads += 1
        self.currentCenter = center
        return numLoads # for debugging reasons, return number of newly loaded areas

