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
    target_speed: float
    time_step: float
    
    components: List[TransformComponent]

    def __init__(self, randomized: float=0):
        self.randomized = randomized
        self.target_speed = 1
        self.time_step = 1
        self.components = []

    def add_component(self, components: List[Component]):
        for component in components:
            if type(component) == TransformComponent:
                self.components.append(component)

    def reset(self):
        for component in self.components:
            component.reset(self.randomized)

    def get_state(self):
        state = {}
        for component in self.components:
            state[component.entity_id] = component.get_state()
        return state
    
    def step(self, *args, **kwargs):
        action = np.zeros(shape=(3,))
        for component in self.components:
            state = component.get_state()

            # testing stuff...
            target_dir = Vector3(1, 1, 1)
            action = self._calculate_target_accel(Vector3(state[3], state[4], state[5]), target_dir)
            action = action.tolist()

            component.update_state(self._propagate(state, action))
        return None
            
    def _motion(self, t, y, a):
        return np.array([ # dx dy dz ddx ddy ddz
            y[3],
            y[4],
            y[5],
            a[0],
            a[1],
            a[2],
        ])

    def _propagate(self, state, a):
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
    
    def _calculate_target_accel(self, curr_vel: Vector3, target_dir: Vector3):
        # NOTE: calculate this using differential equations...
        target_dir_normalized = target_dir.normalized()
        return (target_dir_normalized - curr_vel) * (self.target_speed / self.time_step / 3)