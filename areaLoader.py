from pygame import * 
from wall_ray_camera import *
from controller import * 
import os
MAPAREAWIDTH = 32 #the amount of areas in a row of the total map There can be gaps/jumps

AREAINNERSIZE = [64,64] #the size of a single area

class Area:
    def __init__(self,id):
        self.walls = "INITIALIZE"
        self.entities = "INITIALIZE"
        self.id = id
        self.name = ''
        self.wall = []
        self.entities = []
        filename = f"area{id}.atxt"
        if not os.path.exists(filename):
            print(f"File {filename} is not found")

        with open(filename, 'r') as f:
            lines = f.readlines()
            self.name = lines[0]

            for line in lines[1:]:
                tokens = line.strip().split()
                match(tokens[0]):

                    case "Sky":
                        self.sky = tokens[1]

                    case "Ground":
                        self.ground =  tokens[1]

                    case "Wall":
                        self.wall_color = tokens[1]
                        self.wall.append(tokens[2:])

                    #Parse Entity property
                    case "Entity":
                        for name in tokens[1:]:
                            self.entities.append(name)
                    case _:
                        raise Exception(f"Error while parsing the file unknown property : {tokens[0]}")
        


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

        loadedIds = []
        for row in range(above,below+1,32):
            for col in range(left,right+1):
                id= row + col 
                loadedIds += [id]
                if  not self.loadedAreas.get(id):
                    self.loadedAreas[id] = Area(id)
                    numLoads += 1
        if (numLoads > 0): #then we unload old areas
            for id in self.loadedAreas:
                if id not in loadedIds:
                    del self.loadedAreas[id] 
        self.currentCenter = center
        return numLoads # for debugging reasons, return number of newly loaded areas

