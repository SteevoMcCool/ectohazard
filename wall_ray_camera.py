from math import *
from pygame import *

class Wall:
    def __init__(self, p1, p2):
        self.p1 = p1 
        self.p2 = p2   
        self.color = Color(127,127,127) 


        


        
class Ray:
    def __init__(self, pos, angle):
        self.pos = pos 
        self.angle = angle 

        # Calculate the direction vector from the angle
        self.dir = Vector2(cos(angle), sin(angle))
        
    #
    def contact(self, wall: Wall):
        """Returns the Vector2 contact position if it hits, else False."""

        # Retreive wall 2d collider position
        x1, y1 = wall.p1.x, wall.p1.y
        x2, y2 = wall.p2.x, wall.p2.y
        
        # Retreive ray dimensions on the 2d plane
        x3, y3 = self.pos.x, self.pos.y
        x4, y4 = self.pos.x + self.dir.x, self.pos.y + self.dir.y
        
        # Compute denominator, if it's 0 the wall and the ray are colinears 
        # or parallel and will not intercept so we can return false
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0:
            return False
            
        # 't' represents the distance from the ray origin (x3, y3) to the intersection point.
        # If t > 0, the intersection point lies in the direction the ray is pointing.
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den

        # 'u' represents the normalized position along the wall segment (between p1 and p2).
        # A value of 0.0 means the hit is exactly at p1, 1.0 means exactly at p2.
        # If u is outside the [0, 1] range, the ray missed the physical segment of the wall.
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
        
        if t > 0 and 0 <= u <= 1:
            return Vector2(x1 + t * (x2 - x1), y1 + t * (y2 - y1))
            
        return False

    def firstContact(self, walls: list[Wall]):
        """Returns the closest wall hit by the ray and the contact point."""
        closest_hit = None
        min_dist = float('inf')
        
        for wall in walls:
            hit = self.contact(wall)
            if hit:
                dist = self.pos.distance_to(hit)
                if dist < min_dist:
                    min_dist = dist
                    closest_hit = (wall, hit)
        return closest_hit if closest_hit else False
    
class Camera:
    def __init__(self, center: Ray, fov: float, ray_count: int = 512):
        self.center = center 
        self.fov = fov 
        self.ray_count = ray_count # Number of rays to cast in the FOV

    def view(self, walls: list[Wall]):
        """
        Shoots out rays across the FOV.
        Returns a list of (distance, wall) tuples for the 3D projection engine.
        """
        view_data = []
        angle_step = self.fov / self.ray_count
        start_angle = self.center.angle - (self.fov / 2)
        
        for i in range(self.ray_count):
            ray_angle = start_angle + (i * angle_step)
            ray = Ray(self.center.pos, ray_angle)
            
            hit = ray.firstContact(walls)
            if hit:
                wall, point = hit
                dist = self.center.pos.distance_to(point)
                view_data.append((dist, wall))
            else:
                view_data.append(None)
                
        return view_data