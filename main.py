import pygame

from player import *
from wall_ray_camera import *
from controller import * 
from areaLoader import *
from listOfLists import *


def GameInit():

    init()
    screen = display.set_mode((1280, 720))
    clock =  time.Clock()
    running = True
    dt = 0

    A, B = 2.5, 0.00000000000001
    player = Player()
    areas = AreaLoader() 

    #increasing this value makes us look taller
    HORIZON = 0.575

    while running:
        for e in event.get():
            match(e.type):
                case pygame.QUIT:
                    running = False
                case pygame.KEYDOWN:
                    player.controller.process(e.dict.get('key'),clock.get_time(),"down")
                case pygame.KEYUP:
                    player.controller.process(e.dict.get('key'),clock.get_time(),"up")
                case _:
                    print(f"Unsupported event : {e.type}")

        player.controller.step(dt) #controller's update step, must be called every frame

        if  (areas.loadAround(player.area)):
            print("Loaded new area")
            
        walls  = ListOfLists(area.walls for area in areas.loadedAreas.values())
        entities  = [] #ListOfLists(area.entities for area in areas.loadedAreas.values())
        centerArea = areas.loadedAreas[areas.currentCenter]

        winSize = display.get_window_size()
        player.camera.ray_count = winSize[0]
        screenHeight = winSize[1]


        screen.fill(centerArea.ground)
        screen.fill(centerArea.sky,Rect(0,0,winSize[0],winSize[1] * HORIZON))
        (view,entview) = player.camera.view(walls,entities)
        # print(player.camera.center.pos, player.camera.center.angle)
        for (x,pixRow,ents) in zip(range(len(view)), view,entview):
            if (pixRow):
                dist:float = pixRow [0]
                wall:Wall  = pixRow[1]
                wallSize = screenHeight * (1 + A) / (dist + B)
                draw.line(display.get_surface(),wall.color,
                    Vector2(x,screenHeight * HORIZON + wallSize/2),
                    Vector2(x,screenHeight * HORIZON - wallSize/2)           
                )
            for (entity,dist,texpos) in ents:
                pass

            
        display.flip()
        dt = clock.tick(60) / 1000
    quit()


if __name__ == "__main__":
    GameInit()