import numpy as np
import math
from typing import List, Tuple

class Vector3:

    x: np.float64
    y: np.float64
    z: np.float64

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def sqr_magnitude(self):
        return self.x**2 + self.y**2 + self.y**2
    
    def magnitude(self):
        return math.sqrt(self.sqr_magnitude())
    
    def numpy(self):
        return np.array([self.x, self.y, self.z], dtype=np.float64)
    
    def normalized(self):
        norm = self.magnitude()
        return Vector3(self.x / norm, self.y / norm, self.z / norm)
    
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, other):
        return Vector3(self.x * other, self.y * other, self.z * other)
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other):
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x
        return Vector3(x, y, z)

    @staticmethod
    def sqr_distance(vec_0, vec_1):
        return (vec_0.x-vec_1.x)**2 + (vec_0.y-vec_1.y)**2 + (vec_0.z-vec_1.z)*2
    
    def __str__(self) -> str:
        output = f"[ {self.x}, {self.y}, {self.z} ]"
        return output
    
    def tolist(self) -> list:
        return [self.x, self.y, self.z]
    
class Bounds:
    
    bounds: List[Tuple[float, float]]
    
    def __init__(self, bounds: List[Tuple[float, float]]):
        # check bounds
        for bound in bounds:
            if bound[0] > bound[1]: raise Exception("[Bounds]: lower bound cannot be greater than upper bound!!")
        self.bounds = bounds

    def contains(self, pos: Vector3):
        if len(self.bounds) != 3: return False
        if self.bounds[0][0] > pos.x or pos.x > self.bounds[0][1]: return False
        if self.bounds[1][0] > pos.y or pos.y > self.bounds[1][1]: return False
        if self.bounds[1][0] > pos.z or pos.z > self.bounds[1][1]: return False
        return True
    
    def clamp(self, pos: Vector3):
        x = max(min(pos.x, self.bounds[0][1]), self.bounds[0][0])
        y = max(min(pos.y, self.bounds[1][1]), self.bounds[1][0])
        z = max(min(pos.z, self.bounds[2][1]), self.bounds[2][0]) 
        return Vector3(x, y, z)