from pygame import * 

class Entity:
    def __init__(self,pos,radius,AA,HDA,dialogueFile,dialogueLine,imgfile): 
        #AA stands for anger/agressionx, HDA stands for hp/def/atk. pass them in as TUPLES
        self.pos = (0,0)
        self.radius = 1
        self.texture = image.load(imgfile)
        self.textureSize = texture.get_size() #i think this is a tuple (x,y)   NOT a vector

            
    def loadFromFile(fileName:str) :
        """
            Loads an entity from a file. Returns an entity.
            STATIC method, so no self parameter. Access using: Entity.loadFromFile("myfile")
        """
        pass