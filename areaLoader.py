import os

from gamepaths import *
from pygame import * 
from wall_ray_camera import *
from controller import * 
from entity import *
from gamepaths import *

#the amount of areas in a row of the total map There can be gaps/jumps
MAPAREAWIDTH = 32 

#the size of a single area
AREAINNERSIZE = [64,64] 

DEFAULTSKYCOLOR = Color(60,120,240)

DEFAULTGROUNDCOLOR = Color(100,220,100)


class Area:
    def __init__(self,id):
        print("LOADING...",id)
        self.walls = []
        self.entities = []
        self.id = id
        self.name = ''
        self.walls = []
        self.sky = DEFAULTSKYCOLOR
        self.ground = DEFAULTGROUNDCOLOR
        self.entities = []
        filename = f"{AREA_PATH}/area{id}.atxt"
        self.saveable = False

        self.areaOffset = Vector2(AREAINNERSIZE[0] *  (id%32)  ,     AREAINNERSIZE[1]*  (id//32) )
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
                            self.areaOffset + Vector2(*(float(coord) for coord in tokens[2].strip().split(" "))),
                            self.areaOffset + Vector2(*(float(coord) for coord in tokens[3].strip().split(" "))),
                            Color(*(int(c) for c  in tokens[1].strip().split(" ")))
                        )]


                    #Parse Entity property
                    case "Entity":
                        for fname in tokens[1:]:
                            self.entities.append(Entity(getFile("_",fname,"entity"),self.areaOffset))
                    case "SAVEABLE":
                        self.saveable = True
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


class AreaLoader:

    def __init__(self):
        self.loadedAreas = {}
        self.currentCenter = -1

    def loadAround(self,center:int): 
        #loads all the areas in a 3x3 grid, with the specified area being in the center
        if (center:=int(center)) == self.currentCenter:
            return 0
        above = int(max(center - MAPAREAWIDTH,0))
        below = int(center + MAPAREAWIDTH )
        left = int(max((center - 1),0)% MAPAREAWIDTH) 
        cmod = center  % MAPAREAWIDTH
        right = int(min( (center + 1)  % MAPAREAWIDTH,MAPAREAWIDTH-1))
        numLoads = 0
        loadedIds = []
        print(above,below,left,right)
        for row in range(above,below+1,32):
            for col in range(left-cmod,right+1-cmod):
                id= row + col 
                loadedIds += [id]
                if  not self.loadedAreas.get(id):
                    area = Area(id)
                    if not area.uninitialized:
                        self.loadedAreas[id] = area
                        numLoads += 1
        if (numLoads > 0): #then we unload old areas
            deleted = True 
            while deleted:
                deleted  = False
                for id in self.loadedAreas:
                    if id not in loadedIds:
                        del self.loadedAreas[id] 
                        deleted = True
                        break
        self.currentCenter = center
        return numLoads # for debugging reasons, return number of newly loaded areas

