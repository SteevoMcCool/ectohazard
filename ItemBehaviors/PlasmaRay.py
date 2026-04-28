from pygame import * 
from gamepaths import *
from entity import Actor
from listOfLists import ListOfLists
BASE_DAMAGE = 10
DAMAGE_PER_LEVEL = 0.5
DAMAGE_PER_LEVEL_SQUARED = 0.5
TEMP = 0
global FIRE_ENT
FIRE_ENT = None

def update(self,gameApp): 
    """
        Function to be called every tick
        Parameters:
            self: the Entity described by the file 
                ...
    """
    global FIRE_ENT
    if FIRE_ENT:
        #from player import Player
        p = gameApp.player
        walls = ListOfLists(area.walls for area in gameApp.areas.loadedAreas.values())
        entities =  ListOfLists(area.entities for area in gameApp.areas.loadedAreas.values())
        (wall,cp) = p.camera.center.firstContact(walls)
        ents = p.camera.center.entityContacts(entities,  (cp-p.camera.center.pos).magnitude() if wall else math.inf )
        ent = False
        if len(ents) > 0:
            ent = ents[0]
        if wall:
            if ent:
                dwall = (cp-p.camera.center.pos).magnitude() 
                if dwall <= ent[2]:
                    p.camera.center.shift(dwall- 0.25)
                    FIRE_ENT.pos = p.camera.center.pos *1 #*1 here needed for copy
                    p.camera.center.shift(-dwall + 0.25)
                else:
                    p.camera.center.shift(ent[2]- 0.25)
                    FIRE_ENT.pos = p.camera.center.pos *1 #*1 here needed for copy
                    p.camera.center.shift(-ent[2] + 0.25)
            else:
                dwall = (cp-p.camera.center.pos).magnitude() 
                p.camera.center.shift(dwall- 0.25)
                FIRE_ENT.pos = p.camera.center.pos *1 #*1 here needed for copy
                p.camera.center.shift(-dwall + 0.25)        
        elif ent:
            p.camera.center.shift(ent[2] - 0.25)
            FIRE_ENT.pos = p.camera.center.pos *1 #*1 here needed for copy
            p.camera.center.shift(-ent[2] + 0.25) 
        print (FIRE_ENT.pos)
            

def button1down(self,gameApp):
    """
        Function to be called when the player presses button 1 (defaults to minus key)
        Parameters:
            self: the Entity described by the file 
            ...
    """
    global FIRE_ENT
    if not FIRE_ENT:
        print(FIRE_ENT)
        FIRE_ENT = Actor("FIRE",(0,0),getFile("_","plasmafire.png","texture"),radius=0.5)
        gameApp.tempenties += [FIRE_ENT]
    pass

def button1up(self,gameApp):
    """
        Function to be called when the player presses button 1 (defaults to minus key)
        Parameters:
            self: the Entity described by the file 
            ...
    """
    global FIRE_ENT
    if FIRE_ENT:
        gameApp.tempenties.remove(FIRE_ENT)
        FIRE_ENT = None

def button2down(self,gameApp):
    """
        Function to be called when the player presses button 2 (defaults to plus key)
        Parameters:
            self: the Entity described by the file 
            ...
    """
    print("2d")
    pass

def button2up(self,gameApp):
    """
        Function to be called when the player presses button 2 (defaults to plus key)
        Parameters:
            self: the Entity described by the file 
            ...
    """
    print("2u")
    pass





