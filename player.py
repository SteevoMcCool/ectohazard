from controller import * 
from areaLoader import *
from inventory import *
from listOfLists import ListOfLists

class Player:
    def __init__(self,gameApp):
        # spawn at 260, 200 for Tomsfhire   and 32, 32 for regular zone . 520, 400 for Yellowgrave
        self.camera = Camera(Ray(Vector2(520,400),0),1)
        self.controller = Controller()
        self.inventory = Inventory()
        self.inventory.load(["PlasmaRay","Detector","SkectoLog"])
        self.invSlotEquipped = self.inventory.capacity + 1 #out of bounds to start, you are holding nothing
        self.speed = 10
        self.maxhp = 100
        self.hp = 100
        self.atk = 10 
        self.defc = 10
        self.gameApp = gameApp
        self.controller.addBind(K_w,whileDown= lambda dt: self.move(dt*self.speed* self.camera.center.lookVector()))
        self.controller.addBind(K_s,whileDown= lambda dt: self.move(-dt*self.speed* self.camera.center.lookVector()))
        self.controller.addBind(K_LSHIFT)
        self.controller.addBind(K_d,whileDown= lambda dt: self.turn(0.95*  dt) if self.controller.activePresses.get(K_LSHIFT) else self.turn(2.75*dt) )
        self.controller.addBind(K_a,whileDown= lambda dt: self.turn(0.95* -dt) if self.controller.activePresses.get(K_LSHIFT) else self.turn(2.75*-dt))

        #binds "action" to both "e" and "f"
        self.controller.addBind(K_e,up=lambda t: self.actionKeyPressed() if t < 0.120 else 0)
        self.controller.addBind(K_f,up=lambda t: self.actionKeyPressed() if t < 0.120 else 0)


        self.controller.addBind(K_i,up= lambda t: self.inventory.toggle() if t < 0.120 else 0)
        
        self.controller.addBind(K_MINUS, 
            down = lambda _: self.inventory.items[self.invSlotEquipped].button1down(self,gameApp) if self.invSlotEquipped < len(self.inventory.items) else 0,
            up = lambda _ :self.inventory.items[self.invSlotEquipped].button1up(self,gameApp) if self.invSlotEquipped < len(self.inventory.items) else 0,
        )
        self.controller.addBind(K_EQUALS,
            down = lambda _: self.inventory.items[self.invSlotEquipped].button2down(self,gameApp) if self.invSlotEquipped < len(self.inventory.items) else 0,
            up = lambda _ :self.inventory.items[self.invSlotEquipped].button2up(self,gameApp) if self.invSlotEquipped < len(self.inventory.items) else 0,
        )

        #navigating your hotbar
        self.controller.addBind(K_1,up = lambda _: self.equipItem(0))
        self.controller.addBind(K_2,up = lambda _: self.equipItem(1))
        self.controller.addBind(K_3,up = lambda _: self.equipItem(2))
        self.controller.addBind(K_4,up = lambda _: self.equipItem(3))


    def equipItem(self,slot):
        if self.invSlotEquipped < len(self.inventory.items):
            self.inventory.items[self.invSlotEquipped].update(self.inventory.items[self.invSlotEquipped],self.gameApp,False)
        if slot >= len(self.inventory.items):
            return;
        if slot == self.invSlotEquipped:
            self.invSlotEquipped = self.inventory.capacity + 1 #out of bounds, you are holding nothing
            return;
        self.invSlotEquipped = slot


    def actionKeyPressed(self):
        entities = ListOfLists(area.entities for area in self.gameApp.areas.loadedAreas.values())
        closestEnt = None 
        closestDist = 99999
        for ent in entities:
            d = (ent.pos - self.camera.center.pos).magnitude() 
            if d < 5.5:
                if d < closestDist:
                    closestDist = d 
                    closestEnt = ent 
        if (closestEnt):
            closestEnt.actionKeyPressed(closestEnt, self.gameApp)



    def move(self, deltaPos):
        self.camera.center.pos += deltaPos

    def turn(self, deltaAngle):
        self.camera.center.angle =  (self.camera.center.angle  + deltaAngle) % (6.28318)