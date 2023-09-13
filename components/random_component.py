from .component import Component
from structs import Vector3

class RandomComponent(Component):
    
    count: int
    direction: Vector3

    def __init__(self, entity_id: str = ''):
        super().__init__(entity_id)

        self.direction = Vector3(1, 1, 1)