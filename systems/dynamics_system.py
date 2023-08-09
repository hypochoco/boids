from typing import List
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d

from structs import Vector3
from .system import System
from components.component import Component
from components.transform_component import TransformComponent


class DyanmicsSystem(System):

    randomized: float
    time_step: float
    max_velocity: float
    max_acceleration: float
    
    components: List[TransformComponent]

    init: bool

    def __init__(self, randomized: float=0):
        self.randomized = randomized
        self.time_step = 0.25
        self.max_velocity = 1.
        self.max_acceleration = 8.
        self.components = []

    def add_component(self, components: List[Component]):
        for component in components:
            if type(component) == TransformComponent:
                self.components.append(component)

    def reset(self):
        self.init = True
        for component in self.components:
            component.reset(self.randomized)

    def get_state(self):
        state = {}
        for component in self.components:
            state[component.entity_id] = component.get_state()
        return state
    
    def step(self, *args, **kwargs):
        acceleration_dict = {}
        sys_info = kwargs["sys_info"]
        resolution_dict = sys_info["resolution_dict"]
        separation_dict = sys_info["separation_dict"]
        for component in self.components:
            state = component.get_state()
            entity_id = component.entity_id

            # acceleration
            acceleration = Vector3()
            init_accel = Vector3() # init accel in a direction
            if self.init: 
                init_accel = Vector3(5, 0, 0)
            drag = self._calculate_drag(component.vel) # drag
            collision_accel = Vector3() # collision
            if entity_id in resolution_dict.keys(): 
                collision_accel = resolution_dict[entity_id]
            separation_accel = Vector3()
            if entity_id in separation_dict.keys():
                separation_accel = separation_dict[entity_id]
            
            # sum and propagation
            acceleration = init_accel + drag + collision_accel + separation_accel
            component.update_state(self._propagate(state, acceleration))
            acceleration_dict[entity_id] = acceleration.tolist()

        self.init = False
        sys_info["acceleration_dict"] = acceleration_dict
        return sys_info
            
    def _motion(self, t, y, a):
        return np.array([ # dx dy dz ddx ddy ddz
            y[3],
            y[4],
            y[5],
            a[0],
            a[1],
            a[2],
        ])

    def _propagate(self, state, a: Vector3):
        a = a.tolist()
        y0 = state
        t_eval = np.arange(0, self.time_step * 2, self.time_step / 2)
        sol = solve_ivp(
            self._motion,
            [0, self.time_step * 2],
            y0,
            method="RK45",
            t_eval=t_eval,
            args=(a,),
        )
        interp = interp1d(sol.t, sol.y.T, kind="cubic", axis=0)
        return interp(self.time_step)
    
    def _calculate_drag(self, velocity: Vector3):
        # crude drag approximation
        drag = Vector3()
        vel_mag = velocity.magnitude()
        if vel_mag > self.max_velocity:
            mag_dif = vel_mag - self.max_velocity
            drag = velocity.normalized() * (-mag_dif * self.time_step)
        return drag