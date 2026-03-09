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

        self.controller.addBind(K_w,whileDown= lambda dt: self.move(0, 100*dt) )
        self.controller.addBind(K_s,whileDown= lambda dt: self.move(0,-100*dt))

        self.controller.addBind(K_d,whileDown= lambda dt: self.move(100*dt, 0))
        self.controller.addBind(K_a,whileDown= lambda dt: self.move(-100*dt,0))
    def move(self,deltaX,deltaY):
        self.camera.center.pos += Vector2(deltaX,deltaY)

player = Player()
while running:

    for e in event.get():
        if e.type == QUIT:
            running = False
        elif e.type == KEYDOWN:
            player.controller.process(e.dict.get('key'),clock.get_time(),"down")
        elif e.type == KEYUP:
            player.controller.process(e.dict.get('key'),clock.get_time(),"up")
    
    player.controller.step(dt) #controller's update step, must be called every frame

    print(player.camera.center.pos)
    display.flip()

    dt = clock.tick(60) / 1000

quit()