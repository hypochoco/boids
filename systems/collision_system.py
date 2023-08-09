from typing import List
import numpy as np
import math

from components.collision_component import CollisionComponent
from components.transform_component import TransformComponent
from components.component import Component
from .system import System
from structs import Vector3, Bounds

class CollisionSystem(System):

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
        bounds: Bounds = kwargs["bounds"] if kwargs["bounds"] is not None else None
        entities = kwargs["entities"] if kwargs["entities"] is not None else {}
        out = self._resolve_nearest_collision(bounds, entities)
        sys_info = {
            "collision_dict": out[0],
            "resolution_dict": out[1],
            "proximity_dict": out[2],
        }
        return sys_info
    
    def _resolve_nearest_collision(self, bounds: Bounds, entities):
        collision_dict = {}
        resolution_dict = {}
        proximity_dict = {}
        for i in range(len(self.components)): # loop through all entities
            id_0 = self.components[i].entity_id # init variables
            transform_component_0 = None
            for component in entities[id_0]:
                if type(component) is TransformComponent:
                    transform_component_0 = component
            if transform_component_0 is None: continue
            pos_0 = transform_component_0.pos
            vel_0 = transform_component_0.vel

            # dynamic collisions (other enetities)
            for j in range(1, len(self.components) - i):
                transform_component_1 = None # init variables
                id_1 = self.components[i+j].entity_id
                for component in entities[id_1]:
                    if type(component) is TransformComponent:
                        transform_component_1 = component
                if transform_component_1 is None: continue

                # straight line assumption
                if (pos_0 - transform_component_1.pos).sqr_magnitude() < self.proximity_dist:
                    if id_0 not in proximity_dict.keys(): proximity_dict[id_0] = [] 
                    if id_1 not in proximity_dict.keys(): proximity_dict[id_1] = [] 
                    proximity_dict[id_0].append(id_1)
                    proximity_dict[id_1].append(id_0)
                # predicted_1 = trans_comp_1.pos + trans_comp_1.vel * self.time_step

            # static collisions (bounds collisions)
            t, point = self._bounds_collision( # first collision
                bounds, 
                pos_0, 
                pos_0 + vel_0 * self.time_step
            )
            if point is None: break # stop if no collision found

            collision_dict[id_0] = point.tolist() # collision logging

            for vel in self._directions(vel_0): # collision resolution
                _, point = self._bounds_collision(bounds, pos_0, pos_0 + vel * self.time_step * 3)
                if point is not None: continue
                resolution_dict[id_0] = vel * 0.5 - vel_0 * (1 / (self.time_step * t))

        return collision_dict, resolution_dict, proximity_dict

    def _directions(self, vel: Vector3):
        directions = []
        eps = 1e-8
        vel_magnitude = vel.magnitude()
        if vel_magnitude < eps: return directions
        
        # cases of axis
        index = np.argmax(vel.tolist())
        if index == 0:
            perp_1 = Vector3(-(vel.z + vel.y) / vel.x, 1, 1).normalized()
        elif index == 1:
            perp_1 = Vector3(1, -(vel.x + vel.z) / vel.y, 1).normalized()
        else:
            perp_1 = Vector3(1, 1, -(vel.x + vel.y) / vel.z).normalized()
    
        perp_2 = vel.cross(perp_1).normalized()
        for magnitude in np.arange(0.1, 10.0, 0.1):
            for theta in np.arange(0., 2 * math.pi, 0.1):
                new_dir = perp_1 * magnitude * math.cos(theta) + \
                    perp_2 * magnitude * math.sin(theta) + vel
                new_dir = new_dir.normalized() * vel_magnitude
                directions.append(new_dir)
        return directions

    def _bounds_collision(
        self,
        bounds: Bounds,
        pos_0: Vector3,
        pos_f: Vector3,
    ):
        if bounds.contains(pos_f): return np.inf, None # stop if in bounds
        normals = [
            Vector3(1, 0, 0),
            Vector3(0, 1, 0),
            Vector3(0, 0, 1)
        ]
        bound_points = [
            Vector3(0, 0, 0),
            Vector3(bounds.bounds[0][1], bounds.bounds[1][1], bounds.bounds[2][1])
        ]
        t = np.inf
        for i in range(3): # loop through all six planes of a box
            for j in range(2):
                t_raw = self._ray_plane_collision(
                    pos_0,
                    pos_f,
                    normals[i],
                    bound_points[j]
                )
                if t_raw > 0 and t_raw <= 1: t = min(t, t_raw)
        return t, (pos_f - pos_0) * t + pos_0
            

    def _ray_plane_collision(
        self, 
        pos_0: Vector3, 
        pos_f: Vector3, 
        normal: Vector3,
        point_on_plane: Vector3
    ):
        eps = 1e-8
        ray_dir = pos_f - pos_0
        denom = normal.dot(ray_dir)
        if denom < eps: return np.inf
        numer = normal.dot(point_on_plane - pos_0)
        return numer / denom
