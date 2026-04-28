from pygame import * 
from gamepaths import *
from entity import Actor
from listOfLists import ListOfLists

global FIRE_ENT,TEMPERATURE,OVERHEATED
BASE_DAMAGE = 10
DAMAGE_PER_LEVEL = 0.5
DAMAGE_PER_LEVEL_SQUARED = 0.5
TEMPERATURE = 0
TEMPERATURE_INCREASE_RATE = 10
MAX_TEMPERATURE = 49.1
MAX_TEMPERATURE_BOOST_PER_LEVEL = 0.9
COOLDOWN_RATE = 22
OVERHEATED = False
FIRE_ENT = None

def update(self,gameApp): 
    """
        Function to be called every tick
        Parameters:
            self: the Entity described by the file 
                ...
    """
    LEVEL = self.data.get("level",1)
    global FIRE_ENT, TEMPERATURE,OVERHEATED
    if FIRE_ENT:
        #from player import Player
        TEMPERATURE += gameApp.dt*TEMPERATURE_INCREASE_RATE
        if TEMPERATURE > (MAX_TEMPERATURE + MAX_TEMPERATURE_BOOST_PER_LEVEL*LEVEL):
            gameApp.tempenties.remove(FIRE_ENT)
            FIRE_ENT = None     
            OVERHEATED = True       
            return; 
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
    elif TEMPERATURE > 0:
        TEMPERATURE = max(TEMPERATURE-gameApp.dt*COOLDOWN_RATE,0)
    else:   
        OVERHEATED = False

def button1down(self,gameApp):
    """
        Function to be called when the player presses button 1 (defaults to minus key)
        Parameters:
            self: the Entity described by the file 
            ...
    """
    global FIRE_ENT,OVERHEATED
    if (not FIRE_ENT) and (not OVERHEATED):
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
    global FIRE_ENT,OVERHEATED
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





