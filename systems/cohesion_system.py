from typing import List
import numpy as np

from .system import System
from components.component import Component
from components.cohesion_component import CohesionComponent
from components.transform_component import TransformComponent
from structs import Vector3

class CohesionSystem(System):

    components: List[CohesionComponent]

    def __init__(self):
        super().__init__()

    def add_component(self, components: List[Component]):
        for component in components:
            if type(component) == CohesionComponent:
                self.components.append(component)

    def step(self, *args, **kwargs):

        sys_info = kwargs["sys_info"]
        proximity_dict = sys_info["proximity_dict"]
        entities = kwargs["entities"]

        cohesion_dict = {}

        for component in self.components: # separation
            transform_component = self.get_component(component.entity_id, entities, TransformComponent)
            if transform_component is None: continue
            if component.entity_id not in proximity_dict.keys(): continue

            count = 0
            position_sum = Vector3()
            for other_entity_id in proximity_dict[component.entity_id]:
                count += 1
                other_transform_component = self.get_component(other_entity_id, entities, TransformComponent)
                position_sum = position_sum + other_transform_component.pos

            if count == 0: continue
            average_position = position_sum * (1 / count)
            cohesion_dict[component.entity_id] = average_position - transform_component.pos

        sys_info["cohesion_dict"] = cohesion_dict
        return sys_info