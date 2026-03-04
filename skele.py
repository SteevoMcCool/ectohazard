#note- Vector2 represents pygames Vector2 class, im unable to import it rn

class Wall:
    def __init__(self,p1:Vector2, p2:Vector2):
        self.p1 = p1 
        self.p2 = p2   #the wall goes from position 1 to position 2 
        self.render = None 
    def addRender(self,color,texture):
        self.render = {
            "color": color,
            "texture":texture
        } #if no texture is provided, it renders as the solid color
        
    
class Ray:
    def __init__(self,pos:Vector2, angle:float):
        self.pos = pos 
        self.angle = angle #the origin pos and the angle of the Ray
    def contact(self,wall:Wall):
        #TODO: returns the contact position between the ray and the Wall
        # If they do not collide, returns FALSE 
        pass
    def firstContact(self, walls:[Wall]):
        #TODO: returns the first wall that the ray hits out of the many walls
        pass
    
class Camera:
    def __init__(self, center:Ray,fov:float):
        self.center = center 
        self.fov = fov 
        #the center ray contains the position and direction of the camera

    def render(self,walls:[Wall]):
        #TODO- shoots out a bunch of rays, from at different agled from the center, from  -fov to +fov 
        # renders the walls to the screen using the wall's color (we can account for the textures later)
        # this essentially displays a single "frame" of our game