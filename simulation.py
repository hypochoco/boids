import numpy as np
import numpy.typing as npt
from typing import List, Dict
import json

from components.component import Component
from components.transform_component import TransformComponent
from components.collision_component import CollisionComponent
from systems.system import System
from systems.dynamics_system import DyanmicsSystem
from systems.collision_system import CollisionSystem
from structs import Bounds

class Simulation:

    n: int
    count: int 
    max_count: int
    bounds: Bounds
    systems: List[System]
    entities: Dict[str, List[Component]]
    obs_history: List[Dict[str, npt.NDArray]]
    
    def __init__(self, n=5, max_count=20) -> None:
        self.n = n
        self.max_count = max_count
        self.bounds = Bounds([
            (0, 5),
            (0, 5),
            (0, 5),
        ])
        self.systems = [
            CollisionSystem(),
            DyanmicsSystem(1),
        ]
        components = [
            "CollisionComponent",
            "TransformComponent"
        ]
        self.entities = {}
        for i in range(self.n):
            self.entities[str(i)] = [eval(comp)(entity_id=str(i)) for comp in components]
            for system in self.systems:
                system.add_component(self.entities[str(i)])

    def reset(self):
        self.count = 0 # init variables

        # running through all the systems
        for system in self.systems:
            system.reset()

        # get state of all entites...
        state = {}
        for system in self.systems:
            if type(system) is DyanmicsSystem:
                state = system.get_state()

        # save state history
        self.obs_history = []
        self.obs_history.append(state)

        # return obs
        return state

    def step(self, action=None):
        self.count += 1

        # update systems
        for system in self.systems:
            action = system.step(
                entities=self.entities, 
                action=action,
                bounds=self.bounds,
            )
            if type(system) is DyanmicsSystem: dynamics_system = system

        # get state
        state = dynamics_system.get_state()
        self.obs_history.append(state)
        return state, self.count >= self.max_count
        
    def save_simulation(self):
        data = self.obs_history
        
        # prep data for json dumping
        for item in data:
            for key in item:
                item[key] = list(item[key])
        with open('outputs/data.json', 'w') as f:
            json.dump(data, f, ensure_ascii=False)