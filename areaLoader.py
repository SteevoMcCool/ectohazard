from pygame import * 
from wall_ray_camera import *
from controller import * 
import os
MAPAREAWIDTH = 32 #the amount of areas in a row of the total map There can be gaps/jumps


AREAINNERSIZE = [64,64] #the size of a single area

DEFAULTSKYCOLOR = Color(60,120,240)

DEFAULTGROUNDCOLOR = Color(100,220,100)

PATH_TO_AREAS = "./GameCoreFiles/Areas"

class Area:
    def __init__(self,id):
        self.walls = []
        self.entities = []
        self.id = id
        self.name = ''
        self.walls = []
        self.sky = DEFAULTSKYCOLOR
        self.ground = DEFAULTGROUNDCOLOR
        self.entities = []
        filename = f"{PATH_TO_AREAS}/area{id}.atxt"


        self.uninitialized = False
        if not os.path.exists(filename):
            self.uninitialized = True
            return None

        with open(filename, 'r') as f:
            lines = f.readlines()
            self.name = lines[0]

            for line in lines[1:]:
                tokens = line.strip().split(",")
                match(tokens[0]):

                    case "Sky":
                        self.sky =  Color(*(int(c) for c in tokens[1].strip().split(" ")))

                    case "Ground":
                        self.ground =  Color(*(int(c) for c in tokens[1].strip().split(" ")))

                    case "Wall":
                        self.walls += [Wall(
                            Vector2(*(float(coord) for coord in tokens[2].strip().split(" "))),
                            Vector2(*(float(coord) for coord in tokens[3].strip().split(" "))),
                            Color(*(int(c) for c  in tokens[1].strip().split(" ")))
                        )]
                        print(  Vector2(*(float(coord) for coord in tokens[2].strip().split(" "))),
                            Vector2(*(float(coord) for coord in tokens[3].strip().split(" "))),
                            tokens[1].strip().split(" "))
                        print("ADDED WALL")

                    #Parse Entity property
                    case "Entity":
                        for name in tokens[1:]:
                            self.entities.append(name)
 
                    case _:
                        if len(tokens) > 0:
                            if (tokens[0][0] == "#"):
                                continue
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
                    area = Area(id)
                    if not area.uninitialized:
                        self.loadedAreas[id] = area
                        numLoads += 1
        if (numLoads > 0): #then we unload old areas
            for id in self.loadedAreas:
                if id not in loadedIds:
                    del self.loadedAreas[id] 
        self.currentCenter = center
        return numLoads # for debugging reasons, return number of newly loaded areas

