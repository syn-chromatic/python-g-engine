from components.vectors import Vector3D

from dataclasses import dataclass
from typing import Optional, Union, Callable


@dataclass
class CollisionProperties:
    self_position: Vector3D
    target_position: Vector3D
    self_shifted: Vector3D
    target_shifted: Vector3D
    direction: Vector3D


@dataclass
class CollisionVel:
    v1i: float
    v1f: float
    v2i: float
    v2f: float


@dataclass
class PhysicsProperties:
    collision: Optional[CollisionProperties]


class Circles:
    def __init__(
        self,
        vertices: list[tuple[float, float, float]],
        faces: list[tuple[int, int, int]],
    ):
        self.vertices = vertices
        self.faces = faces


class Triangles:
    def __init__(
        self,
        vertices: list[tuple[float, float, float]],
        faces: list[tuple[int, int, int]],
    ):
        self.vertices = vertices
        self.faces = faces


class Quads:
    def __init__(
        self,
        vertices: list[tuple[float, float, float]],
        faces: list[tuple[int, int, int, int]],
    ):
        self.vertices = vertices
        self.faces = faces


class Polygons:
    def __init__(self, type: Union[Triangles, Quads, Circles]):
        self.type = type


@dataclass
class KeyRegister:
    key: str
    scancode: int
    function: Callable
    press_time: float
    is_pressed: bool
    is_repeatable: bool
