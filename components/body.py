from components.physics import Physics
from components.graphics import Graphics

from abc import ABC, abstractmethod


class Body(ABC):
    def __init__(self):
        self.physics: Physics
        self.color: tuple[float, float, float]

    @abstractmethod
    def set_color(self, color: tuple[float, float, float]) -> None:
        return

    @abstractmethod
    def draw_shape(self, graphics: Graphics) -> None:
        return
