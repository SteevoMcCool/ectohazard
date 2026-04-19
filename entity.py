import os

from gamepaths import *
from pygame import * 


class Entity:

    # Albert                0
    # 0, 9                  1
    # 50, 100, 10           2 hp/def/atk
    # (150, 300)/(1)        3 pos/radius
    # [] list of status     4 strings 
    # albertdialogue.dtxt   5
    # 1                     6
    # texture.png           7
    def __init__(self, filename):
        with open(filename, 'r') as f:
            line_table = f.readlines()
            length = len(line_table)
            if length != 8:
                raise Exception("File format not supported (refer to README.md)")
            
            for i in range(length):
                line = line_table[i]
                match i:
                    case 0:
                        self.name = line.strip()
                    case 1:
                        sub_tokens = line.split(',')
                        self.agression = int(sub_tokens[0].strip())
                        self.activity = int(sub_tokens[1].strip())
                    case 2:
                        sub_tokens = line.split(',')
                        self.hp = int(sub_tokens[0].strip())
                        self.defc = int(sub_tokens[1].strip())
                        self.atk = int(sub_tokens[2].strip())
                    case 3:
                        sub_tokens = line.split('/')
                        self.pos = tuple(map(int, sub_tokens[0].strip("()").split(","))) 
                        self.radius = sub_tokens[1].strip().strip("()")
                    case 4:
                        sub_tokens = line.split(',')
                        self.status = []
                        for token in sub_tokens:
                            self.status.append(token.strip())
                    case 5:
                        self.dialog_file = line.strip()
                    case 6:
                        self.dialog_lines = line.strip()
                    case 7:
                        self.texture = image.load(os.path.join(f'{TEXTURE_PATH}', line.strip()))
                    case _:
                        raise Exception("File format is unsuported (refer to README.md)")
        

    def log(self):
        print(f"Name = {self.name}")
        print(f"Agression = {self.agression}")
        print(f"Activity = {self.activity}")
        print(f"HP = {self.hp}")
        print(f"DEF = {self.defc}")
        print(f"ATK = {self.atk}")
        print(f"Position = {self.pos}")
        print(f"Radius = {self.radius}")
        print(f"Dialog file = {self.dialog_file}")
        print(f"Dialog lines = {self.dialog_lines}")
