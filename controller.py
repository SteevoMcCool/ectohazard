from pygame import *

class Controller:
    def __init__(self):
        self.binds = {} 
        self.activePresses = {}
   
    def addBind(self,key:int,down=None,up=None,whileDown=None):
        self.binds[key] = {
            "down": down, #accepts parameter 'z', which does nothing. It just makes it so all functions have 1 parameter
            "up": up, #accepts parameter 't', which is the amount of time the user was holding the key down
            "whileDown": whileDown #accepts parameter 'dt', which is the amount of time since the last call
        }

    def process(self, press: int, time:float, action="down"):
        bind = self.binds.get(press)
        if bind:
            if (action == 'down'):
                if bind.get("down"):
                    bind.down(0)
                self.activePresses[press] = [
                    time,  
                    bind.get("whileDown")
                ]
            elif (action == 'up'):
                if bind.get("up"):
                    bind.up(time - self.activePresses[press][0])
                del self.activePresses[press]
        else:
            return False 

    def step(self,dt):
        for key,value in self.activePresses.items():
            if (len(value) > 1 and value[1]):
                value[1](dt)
        
