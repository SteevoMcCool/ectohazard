import pygame
import os
from pygame import Surface, font, K_i, K_e

from gamepaths import *
from controller import Controller
from entity import Entity
from areaLoader import AreaLoader
from player import Player
from wall_ray_camera import *
from gamepaths import getFile

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


class Item:
    def __init__(self, name, texture, custom_properties=None):
        self.name = name
        self.texture = texture
        
        if custom_properties:
            for prop_name, prop_value in custom_properties.items():
                # Set the custom property as an attribute on the object
                setattr(self, prop_name, prop_value)


def Load_Inventory(filenames, directory):
    Inventory = []

    for fname in filenames:
        file_path = getFile(directory, fname, 'item')
        
        if file_path and os.path.exists(file_path):
            with open(file_path, 'r') as f:
                lines = f.readlines()
                
                if len(lines) >= 2:
                name = lines[0].strip()
                texture = lines[1].strip()
                
                new_item = Item(name, texture)
                
                for line in lines[2:]:
                    if "=" in line:
                        parts = line.split("=")
                        key = parts[0].strip()
                        value_str = parts[1].strip()
                        value = eval(value_str)
                        setattr(new_item, key, value)
                
                Inventory.append(new_item)
    return Inventory

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
