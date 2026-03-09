from pygame import * 
from skele import *
from controller import * 
init()
screen = display.set_mode((1280, 720))
clock =  time.Clock()
running = True
dt = 0

class Player: 
    def __init__(self):
        self.camera = Camera(Ray(Vector2(0,0),0),70)
        self.controller = Controller()
        self.speed = 100
        
        self.controller.addBind(K_w,whileDown= (lambda dt: self.camera.center.pos.Y +=100*dt) )
        self.controller.addBind(K_s,whileDown= (lambda dt: self.camera.center.pos.Y -= 100 * dt))

        self.controller.addBind(K_d,whileDown= (lambda dt: self.camera.center.pos.X += 100 * dt))
        self.controller.addBind(K_a,whileDown= (lambda dt: self.camera.center.pos.X -= 100 * dt))

        

while running:

    for event in event.get():
        if event.type == QUIT:
            running = False


    

    

    dt = clock.tick(60) / 1000

quit()