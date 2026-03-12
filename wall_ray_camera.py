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
        
    def lookVector(self):
        return Vector2(cos(self.angle),sin(self.angle))
    
    def normVector(self):
        return Vector2(-sin(self.angle),cos(self.angle))
  
    def contact(self, wall: Wall):
        """Returns the Vector2 contact position if it hits, else False."""
        x1, y1 = wall.p1.x, wall.p1.y
        x2, y2 = wall.p2.x, wall.p2.y
        cx, cy = self.pos.x, self.pos.y

        # m1: slope of wall, m2: slope of ray
        wall_dx = x2 - x1
        wall_dy = y2 - y1

        ray_dx = cos(self.angle)
        ray_dy = sin(self.angle)

        # --- Special cases ---

        wall_vertical = abs(wall_dx) < 1e-10
        ray_vertical  = abs(ray_dx)  < 1e-10

        if wall_vertical and ray_vertical:
            return False  # Both vertical (parallel)

        if wall_vertical:
            # Wall is vertical: X is fixed at x1
            m2 = ray_dy / ray_dx
            b2 = cy - m2 * cx
            X = x1
            Y = m2 * X + b2

        elif ray_vertical:
            # Ray is vertical: X is fixed at cx
            m1 = wall_dy / wall_dx
            b1 = y1 - m1 * x1
            X = cx
            Y = m1 * X + b1

        else:
            m1 = wall_dy / wall_dx
            m2 = ray_dy / ray_dx

            if abs(m1 - m2) < 1e-10:
                return False  # Parallel slopes, no intersection

            b1 = y1 - m1 * x1
            b2 = cy - m2 * cx

            # Intersection point
            X = (b2 - b1) / (m1 - m2)
            Y = m1 * X + b1

        if not (min(x1, x2) <= X <= max(x1, x2)):
            return False

        if abs(ray_dx) > 1e-10:
            t = (X - cx) / ray_dx
        else:
            t = (Y - cy) / ray_dy

        if t < 0:
            return False

        return Vector2(X, Y)

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
        
        
        hits = 0
        for i in range(self.ray_count):
            ray_angle = start_angle + (i * angle_step)
            ray = Ray(self.center.pos, ray_angle)
            
            hit = ray.firstContact(walls)
            if hit:
                wall, point = hit
                dist = self.center.pos.distance_to(point)
                view_data.append((dist, wall))
                hits+=1
            else:
                view_data.append(False)
        
        print("Num hits: ", hits)
        return view_data