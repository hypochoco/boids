from typing import List

from components.component import Component

from .system import System
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

        sys_info = kwargs["sys_info"]
        proximity_dict = sys_info["proximity_dict"]
        entities = kwargs["entities"]
        separation_dict = {}

        # loop through all entities
        for component in self.components:
            id_0 = component.entity_id
            transform_component_0 = None
            for component in entities[id_0]:
                if type(component) is TransformComponent:
                    transform_component_0 = component
                    break
            if transform_component_0 is None: continue
            pos_0 = transform_component_0.pos

            dir = Vector3()
            if id_0 not in proximity_dict.keys(): continue
            for id_1 in proximity_dict[id_0]:
                transform_component_1 = None
                for component in entities[id_1]:
                    if type(component) is TransformComponent:
                        transform_component_1 = component
                        break
                if transform_component_1 is None: continue
                pos_1 = transform_component_1.pos

                # TODO: figure out scaling of this vector...
                dir += pos_1 - pos_0

            separation_dict[id_0] = dir.normalized() * -1

        sys_info["separation_dict"] = separation_dict
        return sys_info