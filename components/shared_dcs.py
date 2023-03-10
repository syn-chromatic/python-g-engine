from components.vector_3d import Vector3D

from dataclasses import dataclass
from typing import Optional


@dataclass
class CollisionProperties:
    self_position: Vector3D
    target_position: Vector3D
    self_shifted: Vector3D
    target_shifted: Vector3D
    direction: Vector3D


@dataclass
class PhysicsProperties:
    collision: Optional[CollisionProperties]
