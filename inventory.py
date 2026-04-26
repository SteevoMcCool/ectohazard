import pygame
from pygame import *

from gamepaths import *
from controller import Controller
from entity import Entity
from areaLoader import AreaLoader
from player import Player
from wall_ray_camera import *

import ItemBehaviors

class Item: 
    def __init__(self, sourceItemName):
        with open(getFile("workingDir",sourceItemName + ".itxt","item")) as f:
            self.data = {}
            lc = 0
            for line in f:
                if lc== 0:
                    self.name = line 
                elif lc == 1:
                    #TODO - loads the texture 
                    self.texture =  image.load(os.path.join(f'{TEXTURE_PATH}', line.strip())) 
                else:
                    name, value = line.split('=')
                    self.data[name.strip()] =  eval(value.strip())
                lc+=1
        self.update, self.button1down, self.button1up, self.button2down, self.button2up = None,None,None,None,None
        try:
            self.behavior = ItemBehaviors[sourceItemName]
            self.update = self.behavior.update
            self.button1down = self.behavior.button1down
            self.button1up = self.behavior.button1up
            self.button2down = self.behavior.button2down
            self.button2up = self.behavior.button2up        
        except:
            print("Error accessing behavior: ", sourceItemName)
class Inventory:
    # ui size
    UI_WIDTH = 300
    UI_HEIGHT = 400
    UI_POS = (50, 50)

    # text pos
    TEXT_X = 70
    TEXT_Y = 80
    TEXT_SPACE = 35

    BG_COLOR = (20, 20, 20)
    TEXT_COLOR = (255, 255, 255)
    ALPHA = 180

    def __init__(self, capacity=12):
        self.items = []
        self.capacity = capacity
        self.is_open = False

        # make font one time only
        self.ui_font = font.SysFont("Arial", 22)

    def toggle(self, _=None):
        # open / close bag
        self.is_open = not self.is_open
        print(f"Inventory is {'open' if self.is_open else 'close'}")

    def add(self, entity):
        # check full first
        if len(self.items) >= self.capacity:
            print("Inventory is full")
            return False

        self.items.append(entity)
        return True

    def draw_ui(self, screen):
        if not self.is_open:
            return

        # dark back panel
        overlay = Surface((self.UI_WIDTH, self.UI_HEIGHT))
        overlay.set_alpha(self.ALPHA)
        overlay.fill(self.BG_COLOR)
        screen.blit(overlay, self.UI_POS)

        for i, item in enumerate(self.items):
            # safe name check
            item_name = getattr(item, "name", "Unknown Item")

            text = self.ui_font.render(
                f"{i + 1}. {item_name}",
                True,
                self.TEXT_COLOR
            )

            screen.blit(
                text,
                (self.TEXT_X, self.TEXT_Y + i * self.TEXT_SPACE)
            )





"""these actions will belong to the Player class
# create inv
player_inv = Inventory(capacity=10)

# controller
ctrl = Controller()

# key I open inv
ctrl.addBind(K_i, down=player_inv.toggle)

# key E pickup   <- this will belong to the Entity behavior file
ctrl.addBind(K_e, down=handle_pickup_input)

def handle_pickup_input(_=None):
    # get current area
    area = loader.loadedAreas.get(loader.currentCenter)

    if not area:
        return

    # use copy list, remove more safe
    for entity in area.entities[:]:

        # only item can pickup
        if "item" not in getattr(entity, "status", []):
            continue

        distance = player.pos.distance_to(entity.pos)

        # near enough
        if distance < 60:
            if player_inv.add(entity):
                area.entities.remove(entity)
                print(f"Get: {entity.name}")

            # one item each press
            break
"""