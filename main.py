import pygame
from pygame import *

from player import Player
from areaLoader import *
from listOfLists import ListOfLists
from menu import MainMenu, PauseMenu
from entity import Entity
from inventory import * 
class GameApp:

    def __init__(self):
        init()
        self.tempenties = [] 
        self.screen = display.set_mode((1280, 720))
        display.set_caption("Ectohazard")
        self.clock = time.Clock()
        
        self.process_running = True
        self.game_running = False
        self.dt = 0

        self.player = Player(self)
        self.areas = AreaLoader()
        
        self.main = MainMenu(self)
        self.pause = PauseMenu(self)
        self.approachedEnts = set()

        self.terminalOut = ""
        self.terminalIn = ""
        self.terminalWaiting = False
        self.terminalWaitingFinished=None
        self.terminalFont = font.Font(None,30)
        # Bind ESC key to open pause menu
        self.player.controller.addBind(K_ESCAPE, down=lambda z: self.pause.menu.enable())


    def print(self,*args,end="\n",sep=" \t"):
        count = len(args)
        idx = 0
        for arg in args:
            idx+=1
            self.terminalOut+= str(arg) + (sep if idx < count else end) 

    def input(self,prompt,when_done=None):
        self.terminalWaiting = True
        self.terminalWaitingFinished = when_done
        self.terminalOut += prompt
        #return input(prompt)


    def render_gui(self):
        #STEP1: render inventory gui
        inventory = self.player.inventory
        winSize = display.get_window_size()
        basePosY  = 2/3*winSize[1] + winSize[1]*105/500
        baseHeight = 0.12 * winSize[1]

        baseWidth = 0.12 * winSize[1]
        basePosX = 0.5*winSize[0] - baseWidth*2 - 10
        for i in range(0,4):
            px = basePosX + i*(baseWidth+5) 
            self.screen.fill(
                    Color(67,67,67), 
                    Rect(px, basePosY, baseWidth, baseHeight),       
            )
            if i < len(inventory.items):
                item:Item = inventory.items[i]
                self.screen.blit(transform.scale(item.texture,(baseWidth-4,baseHeight-4)), (px,basePosY))

                
            self.screen.blit(
                self.terminalFont.render(str(i+1),True,Color(255,255,255)), 
                (basePosX + i*(baseWidth+5) , basePosY)
            )


        #STEP2: 
        pass
    def render_game(self, A, B, HORIZON):
        """Handle 3D rendering and world updates"""
        self.player.controller.step(self.dt)

        aX = self.player.camera.center.pos.x // AREAINNERSIZE[0]
        aY = self.player.camera.center.pos.y // AREAINNERSIZE[1]
        self.player.area = aY * 32 + aX
        if self.areas.loadAround(self.player.area):
            print("Loaded new area")
        walls = ListOfLists(area.walls for area in self.areas.loadedAreas.values())
        entities =  ListOfLists(area.entities for area in self.areas.loadedAreas.values())
        entities.addList(self.tempenties)
        centerArea = self.areas.loadedAreas[self.areas.currentCenter]

        winSize = display.get_window_size()
        screenHeight = winSize[1]
        self.player.camera.ray_count = winSize[0]

        # Draw floor and sky
        self.screen.fill(centerArea.ground)
        self.screen.fill(centerArea.sky, Rect(0, 0, winSize[0], winSize[1] * HORIZON))

        view, entview = self.player.camera.view(walls, entities)

        inventory,idx = self.player.inventory, self.player.invSlotEquipped
        if (idx < len(inventory.items)):
            item = inventory.items[idx]
            item.update(item,self)

        for ent in entities:
            if (ent.update):
                ent.update(ent,self)
            if (ent.pos - self.player.camera.center.pos).magnitude() < 1.75:
                if ent not in self.approachedEnts:
                    self.approachedEnts.add(ent)
                    ent.approached(ent,self.player, self)
            elif (ent.pos - self.player.camera.center.pos).magnitude() > 4.25:
                if ent in self.approachedEnts:
                    self.approachedEnts.remove(ent)

        # Render wall columns
        for x, pixRow, ents in zip(range(len(view)), view, entview):
            if pixRow:
                dist, wall = pixRow[0], pixRow[1]
                wallSize = screenHeight * (1 + A) / (dist + B)
                draw.line(self.screen, wall.color,
                    Vector2(x, screenHeight * HORIZON + wallSize/2),
                    Vector2(x, screenHeight * HORIZON - wallSize/2)
                )
            for (entity, contactpos, distance, texturepos) in ents:
                entSize = screenHeight * (1 + A)/1.5 /(distance+ B)
                #draw.line(self.screen, Color(255,255,255),
                #    Vector2(x, screenHeight * HORIZON + entSize/2),
                #    Vector2(x, screenHeight * HORIZON - entSize/2)
                #)
                texture = entity.texture
                tex_width  = texture.get_width()
                tex_height = texture.get_height()
                tex_x = int(round(texturepos*tex_width)) 
                if (tex_x >= tex_width  or tex_x < 0):
                    continue;
                if (entSize > screenHeight*5):
                    # "HUGE"
                    continue
                tex_column = texture.subsurface(Rect(tex_x, 0, 1, tex_height))

                scaled_column = transform.scale(tex_column, (1, entSize))

                self.screen.blit(scaled_column, (x, screenHeight * HORIZON - entSize/3.25))
    
    def respondToSpeaker(self,speaker,response,options):
        self.terminalOut = ""
        self.terminalIn = ""
        if (response == -1): 
            return speaker.chatted(speaker,-1,self)

        try:
            assert 1 <= (r := int(response)) <= len(options)
            speaker.chatted(speaker,r,self)
        except:
            return self.displayDialogueYield(speaker,"Please enter valid number in range.",options)

    def displayDialogueYield(self,speaker:Entity,text:str,options:list[str] = []):
        self.print(f"{speaker.name}: {text}")
        if (not options) or len(options) == 0:
            self.input("Ok? ", when_done= lambda x: self.respondToSpeaker(speaker,-1,options))
            return 1
        else:
            idx = 0
            for option in options:
                self.print(f"[{idx:=idx+1} {option}] ",end="")
                self.input("Choose: ", when_done= lambda x: self.respondToSpeaker(speaker,x,options))
    
    def run(self):
        """Main application loop"""
        A, B = 2.5, 0.0001
        HORIZON = 0.5

        while self.process_running:
            events:list[event.Event] = event.get()
            
            for e in events:
                if e.type == QUIT:
                    self.process_running = False
                
                # Player inputs only if game is active and not paused
                if self.terminalWaiting:
                    if e.type == KEYDOWN:
                        if (e.key == 13):
                            self.terminalWaiting = False
                            if (self.terminalWaitingFinished): 
                                self.terminalWaitingFinished(self.terminalIn)
                                self.terminalIn = ""
                                self.terminalWaitingFinished = None
                        else:
                            self.terminalIn +=  chr(e.key) 
                    elif e.type == KEYUP and self.player.controller.activePresses.get(e.key,None):
                        self.player.controller.process(e.key, self.dt, "up")
                elif self.game_running and not self.pause.menu.is_enabled():
                    if e.type == KEYDOWN:
                        self.player.controller.process(e.key, self.dt, "down")
                    elif e.type == KEYUP:
                        self.player.controller.process(e.key, self.dt, "up")


                
            if self.terminalWaiting:
                winSize = display.get_window_size()
                self.screen.fill(
                        Color(25,20,30), 
                        Rect(1/16*winSize[0], 2/3*winSize[1], winSize[0]*7/8,winSize[1]*1/5)
                    )
                linedx = 0
                for line in (self.terminalOut + self.terminalIn).split('\n'):
                    self.screen.blit(
                        self.terminalFont.render(line ,True,Color(240,240,250)),
                        (1/16*winSize[0] + 5 ,2/3*winSize[1] + 5 + (linedx:=linedx+30)-30 )
                    )
                display.flip()
                self.dt = self.clock.tick(60) / 1000
                continue

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
                if (self.player.invSlotEquipped < len(self.player.inventory.items)):
                    item = self.player.inventory.items[self.player.invSlotEquipped]
                    self.screen.blit(
                        transform.scale(item.texture,display.get_window_size()), (0,0)
                    )

                self.render_gui()
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