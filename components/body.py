from components.physics import Physics
from components.graphics import Graphics
from components.camera import Camera
from components.color import RGBA

from abc import ABC, abstractmethod


class Body(ABC):
    def __init__(self):
        self.physics: Physics
        self.color: RGBA

    @abstractmethod
    def set_color(self, color: RGBA) -> None:
        return

    @abstractmethod
    def draw(self, graphics: Graphics, camera: Camera) -> None:
        return
