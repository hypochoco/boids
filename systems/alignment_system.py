from typing import List
import numpy as np

from .system import System
from components.component import Component
from components.alignment_component import AlignmentComponent
from components.transform_component import TransformComponent
from structs import Vector3

class AlignmentSystem(System):

    components: List[AlignmentComponent]

    def __init__(self):
        super().__init__()

    def add_component(self, components: List[Component]):
        for component in components:
            if type(component) == AlignmentComponent:
                self.components.append(component)

    def step(self, *args, **kwargs):

        sys_info = kwargs["sys_info"]
        proximity_dict = sys_info["proximity_dict"]
        entities = kwargs["entities"]

        alignment_dict = {}

        for component in self.components: # alignment
            transform_component = self.get_component(component.entity_id, entities, TransformComponent)
            if transform_component is None: continue
            if component.entity_id not in proximity_dict.keys(): continue

            count = 0
            direction_sum = Vector3()
            for other_entity_id in proximity_dict[component.entity_id]:
                count += 1
                other_transform_component = self.get_component(other_entity_id, entities, TransformComponent)
                direction_sum = direction_sum + other_transform_component.vel.normalized()

            if count == 0: continue
            average_direction = direction_sum * (1 / count)
            alignment_dict[component.entity_id] = average_direction

        sys_info["alignment_dict"] = alignment_dict
        return sys_info