from typing import List
import numpy as np
import math
import random

from components.collision_component import CollisionComponent
from components.transform_component import TransformComponent
from components.random_component import RandomComponent
from components.component import Component
from .system import System
from structs import Vector3, Bounds

class RandomSystem(System):

    components: List[RandomComponent]

    def __init__(self):
        super().__init__()

    def add_component(self, components: List[Component]):
        for component in components:
            if type(component) is RandomComponent:
                self.components.append(component)

    def step(self, *args, **kwargs):
        sys_info = kwargs["sys_info"]

        for component in self.components:
            if random.random() > 0.5: continue
            dir_list = self._directions(component.direction)
            component.direction = random.choice(dir_list)

        return sys_info
    
    def _directions(self, _dir: Vector3):
        _dir = _dir.normalized() # ensure normalized
        
        index = np.argmax(np.abs(_dir.numpy())) # find axes
        if index == 0:
            perp_1 = Vector3(-(_dir.z + _dir.y) / _dir.x, 1, 1).normalized()
        elif index == 1:
            perp_1 = Vector3(1, -(_dir.x + _dir.z) / _dir.y, 1).normalized()
        else:
            perp_1 = Vector3(1, 1, -(_dir.x + _dir.y) / _dir.z).normalized()
        perp_2 = _dir.cross(perp_1)

        dir_list = [] # construct dirs
        for magnitude in np.arange(0.1, 1., 0.1):
            for theta in np.arange(0.25, 2 * math.pi, 0.25):
                comp_1 = perp_1 * math.cos(theta) * magnitude
                comp_2 = perp_2 * math.sin(theta) * magnitude
                r = perp_1.magnitude() * magnitude
                comp_3_mag = math.sqrt(1 - r**2)
                comp_3 = _dir.normalized() * comp_3_mag
                new_dir = comp_1 + comp_2 + comp_3
                dir_list.append(new_dir)
        return dir_list