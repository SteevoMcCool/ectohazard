from pygame import * 
from gamepaths import *
from entity import Actor
from listOfLists import ListOfLists
import math

global GUIS,FIRE_ENT,TEMPERATURE,OVERHEATED
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
GUIS = {}
def update(self,gameApp,isEquipped=True): 
    """
        Function to be called every tick
        Parameters:
            self: the Entity described by the file
                ...
    """
    LEVEL = self.data.get("level",1)
    global FIRE_ENT, TEMPERATURE,OVERHEATED,GUIS
    maxTemp  = MAX_TEMPERATURE + MAX_TEMPERATURE_BOOST_PER_LEVEL*LEVEL

    if FIRE_ENT:
        #from player import Player
        TEMPERATURE += gameApp.dt*TEMPERATURE_INCREASE_RATE
        if TEMPERATURE > (maxTemp):
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

    if isEquipped:
        temperatureGui = GUIS.get("temperatureGui")
        winSize = gameApp.screen.get_size()
        displayTemperature = math.ceil(TEMPERATURE*10)/10
        r = 255
        g = int(max(0,255-255*(TEMPERATURE/maxTemp)))
        b = int(max(0,255-510*(TEMPERATURE/maxTemp)))
        if not temperatureGui:
            GUIS["temperatureGui"] = [
                gameApp.terminalFont.render(f"Temperature: {displayTemperature}",True,Color(r,g,b)),
                (winSize[0]*0.1,winSize[1]*0.1)
            ]
            gameApp.tempGUIS.append(GUIS["temperatureGui"])
        else:
            temperatureGui[0] = gameApp.terminalFont.render(f"Temperature: {displayTemperature}",True,Color(r,g,b))

        overHeatedGUI = GUIS.get("overHeatedGui")
        if (OVERHEATED and not overHeatedGUI):
            GUIS["overHeatedGui"] = [
                gameApp.terminalFont.render(f"OVERHEATED",True,Color(255,0,0)),
                Rect(winSize[0]*0.1,winSize[1]*0.1+30,winSize[0]*0.25,winSize[1]*0.15)
            ]
            gameApp.tempGUIS.append(GUIS["overHeatedGui"])       
        elif (overHeatedGUI and not OVERHEATED):
            gameApp.tempGUIS.remove(overHeatedGUI)
            GUIS["overHeatedGui"] = None
    else:
        for k,v in GUIS.items():
            gameApp.tempGUIS.remove(v)
            GUIS[k] = None  


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





