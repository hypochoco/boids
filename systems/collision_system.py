from typing import List
import numpy as np

from components.collision_component import CollisionComponent
from components.transform_component import TransformComponent
from components.component import Component
from .system import System
from structs import Vector3, Bounds

class CollisionSystem(System):

    time_step: float
    components: List[CollisionComponent]

    def __init__(self):
        super().__init__()
        self.time_step = 1.

    def add_component(self, components: List[Component]):
        for component in components:
            if type(component) is CollisionComponent:
                self.components.append(component)

    def step(self, *args, **kwargs):
        bounds: Bounds = kwargs["bounds"] if kwargs["bounds"] is not None else None
        entities = kwargs["entities"] if kwargs["entities"] is not None else {}

        collision_dict = {}

        return collision_dict
    
    # find the closest collision...
    # then also find the closest entity or something...
    # static and non static things...
    # find the closest distance that isn't bad
    


    def _find_nearest_collision(self, bounds: Bounds, entities):







        # loop through all entities with a collision component
        for i in range(len(self.components)):

            # t-value
            t = np.inf

            # find positions and velocities
            trans_comp_0 = None
            entity_id_0 = self.components[i].entity_id
            for component in entities[entity_id_0]:
                if type(component) is TransformComponent:
                    trans_comp_0 = component
            if trans_comp_0 is None: continue

            # straight line assumption
            predicted_0 = trans_comp_0.pos + trans_comp_0.vel * self.time_step

            # collision with bounds
            in_bounds = bounds.contains(predicted_0)
            if not in_bounds:
                normals = [
                    Vector3(1, 0, 0),
                    Vector3(0, 1, 0),
                    Vector3(0, 0, 1)
                ]
                points = [
                    Vector3(0, 0, 0),
                    Vector3(5, 5, 5)
                ]

                # deal with collisions...
                for i in range(6):
                    index = i % 3
                    pred_t = self._ray_plane_col(
                        trans_comp_0.pos,
                        predicted_0,
                        normals[index],
                        points[0 if i < 3 else 1]
                    )
                    # store the closest collision point
                    t = pred_t if pred_t < t and pred_t > 0 else t

            # check with other entities
            for j in range(len(self.components) - i):
                
                # find positions and velocities
                trans_comp_1 = None
                entity_id_1 = self.components[i+j].entity_id
                for component in entities[entity_id_1]:
                    if type(component) is TransformComponent:
                        trans_comp_1 = component
                if trans_comp_1 is None: continue

                # straight line assumption
                predicted_1 = trans_comp_1.pos + trans_comp_1.vel * self.time_step




    def _ray_plane_col(
        self, 
        pos: Vector3, 
        predicted: Vector3, 
        n: Vector3,
        point: Vector3
    ):
        eps = 1e-8
        ray_dir = predicted - pos
        denom = n.dot(ray_dir)
        if denom < eps: return np.inf
        numer = n.dot(point - pos)

        return numer / denom
