from components.vectors import Vector3D
from components.color import RGBA

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


class Circle:
    def __init__(
        self,
        vertices: tuple[Vector3D, Vector3D, Vector3D],
        face: tuple[int, int, int],
        shader: tuple[float, float, float],
    ):
        self.vertices = vertices
        self.face = face
        self.shader = shader


@dataclass
class KeyRegister:
    key: str
    scancode: int
    function: Callable
    press_time: float
    is_pressed: bool
    is_repeatable: bool


@dataclass
class FrameTime:
    average_fps: float
