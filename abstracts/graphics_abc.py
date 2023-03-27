from components.color import RGBA
from components.font import FontSettings
from components.polygons import Mesh, Triangle, Quad


from typing import Callable
from abc import ABC, abstractmethod


class GraphicsABC(ABC):
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def register_onkeypress(
        self, func: Callable, key: str, is_repeatable: bool = True
    ) -> None:
        pass

    @abstractmethod
    def set_screensize(self, width: int, height: int) -> None:
        pass

    @abstractmethod
    def set_background_color(self, color: RGBA) -> None:
        pass

    @abstractmethod
    def set_title(self, title: str) -> None:
        pass

    @abstractmethod
    def get_screensize(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def get_width(self) -> int:
        pass

    @abstractmethod
    def get_height(self) -> int:
        pass

    @abstractmethod
    def get_pointer_xy(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def set_draw_thickness(self, size: int) -> None:
        pass

    @abstractmethod
    def draw_circle(
        self,
        point: tuple[float, float],
        radius: float,
        color: RGBA,
    ) -> None:
        pass

    @abstractmethod
    def draw_line(
        self,
        point1: tuple[float, float],
        point2: tuple[float, float],
        thickness: int,
        color: RGBA,
    ) -> None:
        pass

    @abstractmethod
    def draw_polygons(self, mesh: Mesh) -> None:
        pass

    @abstractmethod
    def draw_triangle(self, triangle: Triangle) -> None:
        pass

    @abstractmethod
    def draw_quad(self, quad: Quad):
        pass

    @abstractmethod
    def draw_text(
        self, point: tuple[float, float], text: str, font_settings: FontSettings
    ) -> None:
        pass

    @abstractmethod
    def clear_screen(self) -> None:
        pass
