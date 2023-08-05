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