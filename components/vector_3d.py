import math
from typing_extensions import Self


class Vector3D:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        self.x = x
        self.y = y
        self.z = z

    def multiply(self, num: float) -> Self:
        return Vector3D(self.x * num, self.y * num, self.z * num)

    def divide(self, num: float) -> Self:
        return Vector3D(self.x / num, self.y / num, self.z / num)

    def add_vector(self, vec: Self) -> Self:
        return Vector3D(self.x + vec.x, self.y + vec.y, self.z + vec.z)

    def subtract_vector(self, vec: Self) -> Self:
        return Vector3D(self.x - vec.x, self.y - vec.y, self.z - vec.z)

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
            return Vector3D(0, 0, 0)
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
