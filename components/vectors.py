import math
from typing_extensions import Self


class Vector3D:
    __slots__ = ("x", "y", "z")

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"[{self.x:.3f}, {self.y:.3f}, {self.z:.3f}]"

    def multiply(self, num: float) -> Self:
        return Vector3D(self.x * num, self.y * num, self.z * num)

    def divide(self, num: float) -> Self:
        return Vector3D(self.x / num, self.y / num, self.z / num)

    def add_vector(self, vec: Self) -> Self:
        return Vector3D(self.x + vec.x, self.y + vec.y, self.z + vec.z)

    def subtract_vector(self, vec: Self) -> Self:
        return Vector3D(self.x - vec.x, self.y - vec.y, self.z - vec.z)

    def multiply_vector(self, vec: Self) -> Self:
        return Vector3D(self.x * vec.x, self.y * vec.y, self.z * vec.z)

    def get_midpoint(self, vec: Self) -> Self:
        x_mid = (self.x + vec.x) / 2.0
        y_mid = (self.y + vec.y) / 2.0
        z_mid = (self.z + vec.z) / 2.0
        return Vector3D(x_mid, y_mid, z_mid)

    def get_length_squared(self) -> float:
        return self.x**2.0 + self.y**2.0 + self.z**2.0

    def get_length(self) -> float:
        length_squared = self.get_length_squared()
        if length_squared == 0.0:
            return 0.0
        return math.sqrt(length_squared)

    def normalize(self) -> Self:
        length = self.get_length()
        if length == 0:
            return Vector3D(0.0, 0.0, 0.0)
        return Vector3D(self.x / length, self.y / length, self.z / length)

    def dot_product(self, vec: Self) -> float:
        return (self.x * vec.x) + (self.y * vec.y) + (self.z * vec.z)

    def cross_product(self, vec: Self) -> Self:
        x = self.y * vec.z - self.z * vec.y
        y = self.z * vec.x - self.x * vec.z
        z = self.x * vec.y - self.y * vec.x
        return Vector3D(x, y, z)

    def set_magnitude(self, magnitude: float) -> Self:
        length = self.get_length()
        x, y, z = self.x, self.y, self.z
        if length > 0:
            x = (self.x / length) * magnitude
            y = (self.y / length) * magnitude
            z = (self.z / length) * magnitude
        return Vector3D(x, y, z)