from typing import List
from dataclasses import dataclass, field


@dataclass
class Coord:
    def __init__(self, x, y):
        self.x: int = int(x)
        self.y: int = int(y)

    def __str__(self):
        return f'({self.x}, {self.y})'


@dataclass
class Polygon:

    layer: int = 0
    datatype: int = 0
    V: int = 0
    vertices: List[Coord] = field(default_factory=list)

    def __str__(self):
        vertices_str = ', '.join(str(c) for c in self.vertices)
        return f"""
        Layer: {self.layer},
        Datatype: {self.datatype},
        V: {self.V},
        Vertices: [{vertices_str}]
        """
