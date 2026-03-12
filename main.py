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
        self.camera = Camera(Ray(Vector2(0,0),0),70)
        self.controller = Controller()
        self.speed = 100
        self.area = 135
        self.controller.addBind(K_w,whileDown= lambda dt: self.move(0, 100*dt) )
        self.controller.addBind(K_s,whileDown= lambda dt: self.move(0,-100*dt))

        self.controller.addBind(K_d,whileDown= lambda dt: self.move(100*dt, 0))
        self.controller.addBind(K_a,whileDown= lambda dt: self.move(-100*dt,0))
    def move(self,deltaX,deltaY):
        self.camera.center.pos += Vector2(deltaX,deltaY)

A,B = 0.1,0.1
player = Player()
areas = AreaLoader() 


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
    screen.fill(Color(60,120,240),Rect(0,0,winSize[0],winSize[1]/2))
    view = player.camera.view([
        Wall(Vector2(100,-100),Vector2(100,100)),
        Wall(Vector2(-100,-100),Vector2(-100,100)),
        Wall(Vector2(-100,100),Vector2(100,100)),
        Wall(Vector2(-100,-100),Vector2(100,-100)),

    ])
    print(player.camera.center.pos, player.camera.center.angle)
    for (x,pixRow) in zip(range(len(view)), view):
        if (pixRow):
            print(pixRow)
            dist:float = pixRow [0]
            wall:Wall  = pixRow[1]
            wallSize = screenHeight * (1 + A) / (dist + B)
            draw.line(display.get_surface(),wall.color,
                Vector2(x,screenHeight/2 + wallSize/2),
                Vector2(x,screenHeight/2 - wallSize/2)           
            )

    
    display.flip()
    dt = clock.tick(60) / 1000


quit()