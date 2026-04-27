from controller import * 
from areaLoader import *
from inventory import *


class Player:
    def __init__(self,gameApp):
        self.camera = Camera(Ray(Vector2(32,32),0),1)
        self.controller = Controller()
        self.inventory = Inventory()
        self.invSlotEquipped = 0
        self.speed = 10
        self.area = 1
        self.gameApp = gameApp
        self.controller.addBind(K_w,whileDown= lambda dt: self.move(dt*self.speed* self.camera.center.lookVector()))
        self.controller.addBind(K_s,whileDown= lambda dt: self.move(-dt*self.speed* self.camera.center.lookVector()))
        self.controller.addBind(K_d,whileDown= lambda dt: self.turn(0.85*  dt))
        self.controller.addBind(K_a,whileDown= lambda dt: self.turn(0.85* -dt))

        #binds "action" to both "e" and "f"
        self.controller.addBind(K_e,up=lambda t: self.actionKeyPressed() if t < 0.120 else 0)
        self.controller.addBind(K_f,up=lambda t: self.actionKeyPressed() if t < 0.120 else 0)


        self.controller.addBind(K_i,up= lambda t: self.inventory.toggle() if t < 0.120 else 0)
        
        self.controller.addBind(K_MINUS)
        self.controller.addBind(K_PLUS)

        #navigating your hotbar
        self.controller.addBind(K_1,up = lambda _: self.equipItem(0))
        self.controller.addBind(K_2,up = lambda _: self.equipItem(1))
        self.controller.addBind(K_3,up = lambda _: self.equipItem(2))
        self.controller.addBind(K_4,up = lambda _: self.equipItem(3))


    def equipItem(slot):
        pass


    def actionKeyPressed(self):
        pass
    def move(self, deltaPos):
        self.camera.center.pos += deltaPos

    def turn(self, deltaAngle):
        self.camera.center.angle =  (self.camera.center.angle  + deltaAngle) % (6.28318)