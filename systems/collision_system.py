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
            if point is None: continue # stop if no collision found

            print(f"collision found!! {id_0}: {point}") # collision logging
            collision_dict[id_0] = point.tolist()

            for _dir in self._directions(vel_0): # collision resolution
                vel = _dir * vel_0.magnitude()
                _, point = self._bounds_collision(bounds, pos_0, pos_0 + vel * self.time_step * 3)
                if point is not None: continue
                resolution_dict[id_0] = vel * 0.5 - vel_0 * (1 / (self.time_step * t))

        return collision_dict, resolution_dict, proximity_dict

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
        if np.abs(denom) < eps: # vectors are perpendicular
            return 0 if np.abs((pos_0 - point_on_plane).dot(normal)) < eps else np.inf
        numer = normal.dot(point_on_plane - pos_0)
        return numer / denom

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
                if t_raw >= 0 and t_raw <= 1: t = min(t, t_raw)
        return t, (pos_f - pos_0) * t + pos_0