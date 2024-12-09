from dataclasses import dataclass


@dataclass
class SubField:
    id: float
    xMin: float
    xMax: float
    yMin: float
    yMax: float
    mf: float
