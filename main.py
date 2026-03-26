from pygame import * 
from wall_ray_camera import *
from controller import * 
from areaLoader import *
init()
screen = display.set_mode((1280, 720))
clock =  time.Clock()
running = True
dt = 0

class Player: 
    def __init__(self):
        self.camera = Camera(Ray(Vector2(0,0),0),1)
        self.controller = Controller()
        self.speed = 10
        self.area = 135
        self.controller.addBind(K_w,whileDown= lambda dt: self.move(dt*self.speed* self.camera.center.lookVector()))
        self.controller.addBind(K_s,whileDown= lambda dt: self.move(-dt*self.speed* self.camera.center.lookVector()))

        self.controller.addBind(K_d,whileDown= lambda dt: self.turn(0.85* dt) )
        self.controller.addBind(K_a,whileDown= lambda dt: self.turn(0.85* -dt))
    def move(self,deltaPos):
        self.camera.center.pos += deltaPos
    def turn(self,deltaAngle):
        self.camera.center.angle =  (self.camera.center.angle  + deltaAngle) % (6.28318)

A,B = 2.2,0.0001
player = Player()
areas = AreaLoader() 

HORIZON =0.575 #increasing this value makes us look taller
while running:

    for e in event.get():
        if e.type == QUIT:
            running = False
        elif e.type == KEYDOWN:
            player.controller.process(e.dict.get('key'),clock.get_time(),"down")
        elif e.type == KEYUP:
            player.controller.process(e.dict.get('key'),clock.get_time(),"up")
    
    player.controller.step(dt) #controller's update step, must be called every frame
    areas.loadAround(player.area)

    winSize = display.get_window_size()
    player.camera.ray_count = winSize[0]
    screenHeight = winSize[1]
    screen.fill(Color(100,220,100))
    screen.fill(Color(60,120,240),Rect(0,0,winSize[0],winSize[1] * HORIZON))
    view = player.camera.view([
        Wall(Vector2(20,-20),Vector2(20.1,20.1)),
        Wall(Vector2(-20,-20),Vector2(-20.1,20.1)),
        Wall(Vector2(-20,20),Vector2(20.1,20.1)),
        Wall(Vector2(-20,-20),Vector2(20.1,-20.1)),
    ])
    print(player.camera.center.pos, player.camera.center.angle)
    for (x,pixRow) in zip(range(len(view)), view):
        if (pixRow):
            dist:float = pixRow [0]
            wall:Wall  = pixRow[1]
            wallSize = screenHeight * (1 + A) / (dist + B)
            draw.line(display.get_surface(),wall.color,
                Vector2(x,screenHeight * HORIZON + wallSize/2),
                Vector2(x,screenHeight * HORIZON - wallSize/2)           
            )
    

    
    display.flip()
    dt = clock.tick(60) / 1000


quit()