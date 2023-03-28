from components.vectors import Vector3D
from components.color import RGBA

from typing import Union


class Triangle:
    def __init__(
        self,
        vertices: tuple[Vector3D, Vector3D, Vector3D],
        face: tuple[int, int, int],
        shader: RGBA = RGBA(1.0, 1.0, 1.0, 1.0),
        color: RGBA = RGBA(1.0, 1.0, 1.0, 1.0),
    ):
        self.vertices = vertices
        self.face = face
        self.shader = shader
        self.color = color


class Quad:
    def __init__(
        self,
        vertices: tuple[Vector3D, Vector3D, Vector3D, Vector3D],
        face: tuple[int, int, int, int],
        shader: RGBA = RGBA(1.0, 1.0, 1.0, 1.0),
        color: RGBA = RGBA(1.0, 1.0, 1.0, 1.0),
    ) -> None:
        self.vertices = vertices
        self.face = face
        self.shader = shader
        self.color = color


class Mesh:
    def __init__(self, polygons: list[Union[Triangle, Quad]]) -> None:
        self.polygons = polygons
