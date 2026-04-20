import pygame
from pygame import *

from player import Player
from areaLoader import AreaLoader
from listOfLists import ListOfLists
from menu import MainMenu, PauseMenu

class GameApp:

    def __init__(self):
        init()

        self.screen = display.set_mode((1280, 720))
        display.set_caption("Ectohazard")
        self.clock = time.Clock()
        
        self.process_running = True
        self.game_running = False
        self.dt = 0

        self.player = Player()
        self.areas = AreaLoader()
        
        self.main = MainMenu(self)
        self.pause = PauseMenu(self)

        # Bind ESC key to open pause menu
        self.player.controller.addBind(K_ESCAPE, down=lambda z: self.pause.menu.enable())

    def render_game(self, A, B, HORIZON):
        """Handle 3D rendering and world updates"""
        self.player.controller.step(self.dt)

        if self.areas.loadAround(self.player.area):
            print("Loaded new area")

        walls = ListOfLists(area.walls for area in self.areas.loadedAreas.values())
        entities = [] 
        centerArea = self.areas.loadedAreas[self.areas.currentCenter]

        winSize = display.get_window_size()
        screenHeight = winSize[1]
        self.player.camera.ray_count = winSize[0]

        # Draw floor and sky
        self.screen.fill(centerArea.ground)
        self.screen.fill(centerArea.sky, Rect(0, 0, winSize[0], winSize[1] * HORIZON))

        view, entview = self.player.camera.view(walls, entities)

        # Render wall columns
        for x, pixRow, ents in zip(range(len(view)), view, entview):
            if pixRow:
                dist, wall = pixRow[0], pixRow[1]
                wallSize = screenHeight * (1 + A) / (dist + B)
                
                draw.line(self.screen, wall.color,
                    Vector2(x, screenHeight * HORIZON + wallSize/2),
                    Vector2(x, screenHeight * HORIZON - wallSize/2)
                )

    def run(self):
        """Main application loop"""
        A, B = 2.5, 0.0001
        HORIZON = 0.575

        while self.process_running:
            events = event.get()
            
            for e in events:
                if e.type == QUIT:
                    self.process_running = False
                
                # Player inputs only if game is active and not paused
                if self.game_running and not self.pause.menu.is_enabled():
                    if e.type == KEYDOWN:
                        self.player.controller.process(e.key, self.dt, "down")
                    elif e.type == KEYUP:
                        self.player.controller.process(e.key, self.dt, "up")

            # --- Safe State Management ---
            if not self.game_running:
                # Check if main menu is enabled (Redundancy here is crucial do not simplify !)
                if self.main.menu.is_enabled():
                    self.main.menu.update(events)
                if self.main.menu.is_enabled():
                    self.main.menu.draw(self.screen)
            else:
                # Game is running
                self.render_game(A, B, HORIZON)

                # Check if pause menu is enabled (Redundancy here is crucial do not simplify !)
                if self.pause.menu.is_enabled():
                    self.pause.menu.update(events)
                if self.pause.menu.is_enabled():
                    self.pause.menu.draw(self.screen)

            display.flip()
            self.dt = self.clock.tick(60) / 1000

        quit()

if __name__ == "__main__":
    app = GameApp()
    app.run()