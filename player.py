from controller import * 
from areaLoader import *

class Player:

    def __init__(self):
        self.camera = Camera(Ray(Vector2(32,32),0),1)
        self.controller = Controller()
        self.speed = 10
        self.area = 1
        self.controller.addBind(K_w,whileDown= lambda dt: self.move(dt*self.speed* self.camera.center.lookVector()))
        self.controller.addBind(K_s,whileDown= lambda dt: self.move(-dt*self.speed* self.camera.center.lookVector()))

        self.controller.addBind(K_d,whileDown= lambda dt: self.turn(0.85*  dt))
        self.controller.addBind(K_a,whileDown= lambda dt: self.turn(0.85* -dt))

    def move(self, deltaPos):
        self.camera.center.pos += deltaPos

    def turn(self, deltaAngle):
        self.camera.center.angle =  (self.camera.center.angle  + deltaAngle) % (6.28318)