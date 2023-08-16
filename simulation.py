import numpy as np
import numpy.typing as npt
from typing import List, Dict
import json

from components.component import Component
from components.transform_component import TransformComponent
from components.collision_component import CollisionComponent
from components.separation_component import SeparationComponent
from systems.system import System
from systems.dynamics_system import DyanmicsSystem
from systems.collision_system import CollisionSystem
from systems.separation_system import SeparationSystem
from structs import Bounds

class Simulation:

    n: int
    count: int 
    max_count: int
    bounds: Bounds
    systems: List[System]
    entities: Dict[str, List[Component]]

    obs_history: List[Dict[str, npt.NDArray]]
    collision_history: List[Dict[str, npt.NDArray]]
    acceleration_history: List[Dict[str, npt.NDArray]]
    
    def __init__(self, n=5, max_count=25) -> None:
        self.n = n
        self.max_count = max_count
        # self.bounds = Bounds([
        #     (0, 5),
        #     (0, 5),
        #     (0, 5),
        # ])
        self.bounds = Bounds([
            (0, 15),
            (0, 15),
            (0, 15),
        ])
        self.systems = [
            CollisionSystem(),
            SeparationSystem(),
            DyanmicsSystem(1),
        ]
        components = [
            "CollisionComponent",
            "SeparationComponent",
            "TransformComponent"
        ]
        self.entities = {}
        for i in range(self.n):
            self.entities[str(i)] = [eval(comp)(entity_id=str(i)) for comp in components]
            for system in self.systems:
                system.add_component(self.entities[str(i)])

    def reset(self):
        self.count = 0
        for system in self.systems: # reset all systems
            system.reset()
        state = {}
        for system in self.systems: # get init state from dynamics
            if type(system) is DyanmicsSystem:
                state = system.get_state()
        self.obs_history = [] # save state for animation
        self.obs_history.append(state)
        self.collision_history = []
        self.acceleration_history = []
        return state

    def step(self, sys_info=None):
        self.count += 1 # count
        for system in self.systems: # step all systems
            if type(system) is DyanmicsSystem: dynamics_system = system
            sys_info = system.step(
                sys_info=sys_info,
                bounds=self.bounds,
                entities=self.entities,
            )
        state = dynamics_system.get_state() # get and save state
        self.obs_history.append(state)
        self.collision_history.append(sys_info["collision_dict"])
        self.acceleration_history.append(sys_info["acceleration_dict"])
        return state, self.count >= self.max_count
        
    def save_simulation(self):
        data = {
            "obs": self.obs_history,
            "collisions": self.collision_history,
            "acceleration": self.acceleration_history
        }

        for key in data:
            for item in data[key]:
                for key in item:
                    item[key] = list(item[key])
        with open('outputs/data.json', 'w') as f:
            json.dump(data, f, ensure_ascii=False)