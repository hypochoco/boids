from typing import List
import numpy as np

from .system import System
from components.component import Component
from components.separation_component import SeparationComponent
from components.transform_component import TransformComponent
from structs import Vector3

class SeparationSystem(System):

    components: List[SeparationComponent]

    def __init__(self):
        super().__init__()

    def add_component(self, components: List[Component]):
        for component in components:
            if type(component) == SeparationComponent:
                self.components.append(component)

    def step(self, *args, **kwargs):

        sys_info = kwargs["sys_info"] # grab info
        proximity_dict = sys_info["proximity_dict"]
        entities = kwargs["entities"]

        separation_dict = {}

        for component in self.components: # separation
            transform_component = self.get_component(component.entity_id, entities, TransformComponent)
            if transform_component is None: continue
            if component.entity_id not in proximity_dict.keys(): continue

            separation = Vector3()
            for other_entity_id in proximity_dict[component.entity_id]:
                other_transform_component = self.get_component(other_entity_id, entities, TransformComponent)
                directional = other_transform_component.pos - transform_component.pos
                if directional.magnitude() < 1e-8: continue
                separation = separation + directional.normalized() * (1 / directional.magnitude())
            if separation.magnitude() < 1e-8: continue
            separation_dict[component.entity_id] = separation.normalized()

        sys_info["separation_dict"] = separation_dict
        return sys_info