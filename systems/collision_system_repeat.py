from typing import List
import numpy as np
import math

from components.collision_component import CollisionComponent
from components.transform_component import TransformComponent
from components.component import Component
from .system import System
from structs import Vector3, Bounds

class CollisionSystemRepeat(System):

    time_step: float
    proximity_dist: float
    components: List[CollisionComponent]

    def __init__(self):
        super().__init__()
        self.time_step = 1.
        self.proximity_dist = 4.

    def add_component(self, components: List[Component]):
        for component in components:
            if type(component) is CollisionComponent:
                self.components.append(component)

    def step(self, *args, **kwargs):
        sys_info = kwargs["sys_info"] # setup
        bounds: Bounds = kwargs["bounds"]
        entities = kwargs["entities"]

        for component in self.components: # bounds collisions

            # find transform component
            transform_component = self.get_component(component.entity_id, entities, TransformComponent)
            if transform_component is None: continue

            pos = transform_component.pos # handle bounds
            if not bounds.contains(transform_component.pos):
                new_pos = bounds.repeat(pos)
                transform_component.update_pos(new_pos)

        return sys_info