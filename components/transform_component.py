import numpy as np
import numpy.typing as npt
import random

from .component import Component
from structs import Vector3

class TransformComponent(Component):

    pos: Vector3
    vel: Vector3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.pos = Vector3()
        self.vel = Vector3()

    def reset(self):
        self.pos = Vector3()
        self.vel = Vector3()

    def get_state(self):
        return np.append(self.pos.numpy(), self.vel.numpy())
    
    def update_state(self, state: npt.NDArray):
        self.pos = Vector3(state[0], state[1], state[2])
        self.vel = Vector3(state[3], state[4], state[5])

    def update_pos(self, pos: Vector3):
        self.pos = pos

    def __str__(self) -> str:
        output = f"[TransformComponent]: pos: {self.pos}, vel: {self.vel}"
        return output
    