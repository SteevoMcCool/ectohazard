from pygame import * 
from skele import *
from controller import * 


class Area:
    #TODO- must read from an .atxt file that has walls and other info
    pass 


MAPAREAWIDTH = 32
class AreaLoader:

    def __init__(self):
        self.loadedAreas = {}
        self.currentCenter = 0

    def loadAround(self,center:int): 
        #loads all the areas in a 3x3 grid, with the specified area being in the center
        if center == self.currentCenter:
            return 0
        above = max(center - 32,0)
        below = center + 32 
        left = max(center - 1,0) % 32 
        right = min(center + 1,31) % 32
        numLoads = 0
        for row in range(above,below+1,32):
            for col in range(left,right+1):
                id= row + col 
                if  not self.loadedAreas.get(id):
                    self.loadedAreas[id] = Area(id)
                    numLoads += 1
        self.currentCenter = center
        return numLoads # for debugging reasons, return number of newly loaded areas

