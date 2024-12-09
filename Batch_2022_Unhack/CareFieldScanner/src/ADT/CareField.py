from dataclasses import dataclass


@dataclass
class CareField:
    id: float
    xMin: float
    xMax: float
    yMin: float
    yMax: float

    def __str__(self) -> str:
        return f"CareField(id={self.id}, xMin={self.xMin}, xMax={self.xMax}, yMin={self.yMin}, yMax={self.yMax})"