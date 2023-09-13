from typing import List

from components.component import Component

class System():

    components: List[Component]

    def __init__(self):
        self.components = []

    def reset(self):
        pass

    def step(self, *args, **kwargs):
        pass

    def add_component(self, components: List[Component]):
        pass

    def get_component(self, entity_id, entities, _type):
        for component in entities[entity_id]:
            if type(component) is _type:
                return component
        return None
