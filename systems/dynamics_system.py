from typing import List
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d
import random

from structs import Vector3
from .system import System
from components.component import Component
from components.transform_component import TransformComponent
from components.random_component import RandomComponent


class DyanmicsSystem(System):

    randomized: float
    time_step: float
    max_velocity: float
    max_acceleration: float
    
    components: List[TransformComponent]

    init: bool

    def __init__(self):
        self.time_step = 0.25
        self.max_velocity = 1.
        self.max_acceleration = 10.
        self.components = []

    def add_component(self, components: List[Component]):
        for component in components:
            if type(component) == TransformComponent:
                self.components.append(component)

    def reset(self):
        self.init = True
        for component in self.components:
            component.reset()
            rand_0 = random.random() * 10 + 2
            rand_1 = random.random() * 10 + 2
            rand_2 = random.random() * 10 + 2
            component.pos = Vector3(rand_0, rand_1, rand_2)

    def get_state(self):
        state = {}
        for component in self.components:
            state[component.entity_id] = component.get_state()
        return state
    
    def step(self, *args, **kwargs):
        sys_info = kwargs["sys_info"]
        entities = kwargs["entities"]

        acceleration_dict = {} # logging information

        # resolution_dict = sys_info["resolution_dict"]
        alignment_dict = sys_info["alignment_dict"]
        cohesion_dict = sys_info["cohesion_dict"]
        separation_dict = sys_info["separation_dict"]

        for component in self.components: # acceleration calculation

            alignment = alignment_dict[component.entity_id] if component.entity_id in alignment_dict.keys() else None # average direction
            cohesion = cohesion_dict[component.entity_id] if component.entity_id in cohesion_dict.keys() else None # distance to average position
            separation = separation_dict[component.entity_id] if component.entity_id in separation_dict.keys() else None # normalized vector

            if alignment is None and cohesion is None and separation is None: # random if no components
                random_component = self.get_component(component.entity_id, entities, RandomComponent)
                acceleration = random_component.direction

                component.update_state(self._propagate(component.get_state(), acceleration))
                acceleration_dict[component.entity_id] = acceleration.tolist()

                continue
            
            if alignment is None: alignment = Vector3()
            if cohesion is None: cohesion = Vector3()
            if separation is None: separation = Vector3()

            acceleration = alignment * 0.85 + cohesion * 1.125 - separation # nice 
            # acceleration = alignment * 0.85 + cohesion * 1.125 - separation * 1.125

            component.update_state(self._propagate(component.get_state(), acceleration))
            acceleration_dict[component.entity_id] = acceleration.tolist()            

        sys_info["acceleration_dict"] = acceleration_dict
        return sys_info
            
    def _motion(self, t, y, a):
        velocity = Vector3(y[3], y[4], y[5])
        acceleration = Vector3(a[0], a[1], a[2])
        if velocity.magnitude() >= self.max_velocity:
            projection = acceleration.project(velocity.normalized())
            acceleration = acceleration - projection
        return np.array(
            velocity.tolist() + acceleration.tolist()
        )

    def _propagate(self, state, a: Vector3):
        t_eval = np.arange(0, self.time_step * 2, self.time_step / 2)
        sol = solve_ivp(
            self._motion,
            [0, self.time_step * 2],
            state,
            method="RK45",
            t_eval=t_eval,
            args=(a.tolist(),),
        )
        interp = interp1d(sol.t, sol.y.T, kind="cubic", axis=0)
        return interp(self.time_step)