from .component import Component
from structs import Vector3

class CollisionComponent(Component):
    
    def __init__(self, entity_id: str = ''):
        super().__init__(entity_id)