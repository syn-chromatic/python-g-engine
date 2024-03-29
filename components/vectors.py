import math


class Vector3D:
    __slots__ = ("x", "y", "z")

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"[{self.x:.2f}, {self.y:.2f}, {self.z:.2f}]"

    def to_tuple(self) -> tuple[float, float, float]:
        x = self.x
        y = self.y
        z = self.z
        return (x, y, z)

    def clamp(self, min_value: float, max_value: float) -> "Vector3D":
        x = max(min_value, min(self.x, max_value))
        y = max(min_value, min(self.y, max_value))
        z = max(min_value, min(self.z, max_value))
        return Vector3D(x, y, z)

    def add(self, num: float) -> "Vector3D":
        x = self.x + num
        y = self.y + num
        z = self.z + num

        return Vector3D(x, y, z)

    def subtract(self, num: float) -> "Vector3D":
        x = self.x - num
        y = self.y - num
        z = self.z - num

        return Vector3D(x, y, z)

    def multiply(self, num: float) -> "Vector3D":
        x = self.x * num
        y = self.y * num
        z = self.z * num

        return Vector3D(x, y, z)

    def divide(self, num: float) -> "Vector3D":
        x = self.x / num
        y = self.y / num
        z = self.z / num

        return Vector3D(x, y, z)

    def add_vector(self, vec: "Vector3D") -> "Vector3D":
        x = self.x + vec.x
        y = self.y + vec.y
        z = self.z + vec.z

        return Vector3D(x, y, z)

    def subtract_vector(self, vec: "Vector3D") -> "Vector3D":
        x = self.x - vec.x
        y = self.y - vec.y
        z = self.z - vec.z

        return Vector3D(x, y, z)

    def multiply_vector(self, vec: "Vector3D") -> "Vector3D":
        x = self.x * vec.x
        y = self.y * vec.y
        z = self.z * vec.z

        return Vector3D(x, y, z)

    def divide_vector(self, vec: "Vector3D") -> "Vector3D":
        x = self.x / vec.x
        y = self.y / vec.y
        z = self.z / vec.z

        return Vector3D(x, y, z)

    def normalize(self) -> "Vector3D":
        length = self.get_length()
        if length == 0:
            return Vector3D(0.0, 0.0, 0.0)
        x = self.x / length
        y = self.y / length
        z = self.z / length

        return Vector3D(x, y, z)

    def dot_product(self, vec: "Vector3D") -> float:
        x = self.x * vec.x
        y = self.y * vec.y
        z = self.z * vec.z

        return x + y + z

    def cross_product(self, vec: "Vector3D") -> "Vector3D":
        x = self.y * vec.z - self.z * vec.y
        y = self.z * vec.x - self.x * vec.z
        z = self.x * vec.y - self.y * vec.x
        return Vector3D(x, y, z)

    def set_magnitude(self, magnitude: float) -> "Vector3D":
        length = self.get_length()
        x, y, z = self.x, self.y, self.z
        if length > 0:
            x = (self.x / length) * magnitude
            y = (self.y / length) * magnitude
            z = (self.z / length) * magnitude
        return Vector3D(x, y, z)

    def lerp_interpolation(self, vec: "Vector3D", t: float) -> "Vector3D":
        x = self.x + (vec.x - self.x) * t
        y = self.y + (vec.y - self.y) * t
        z = self.z + (vec.z - self.z) * t
        return Vector3D(x, y, z)

    def get_midpoint(self, vec: "Vector3D") -> "Vector3D":
        x = (self.x + vec.x) / 2.0
        y = (self.y + vec.y) / 2.0
        z = (self.z + vec.z) / 2.0

        return Vector3D(x, y, z)

    def get_length_squared(self) -> float:
        x = self.x**2.0
        y = self.y**2.0
        z = self.z**2.0

        return x + y + z

    def get_length(self) -> float:
        length_squared = self.get_length_squared()
        if length_squared == 0.0:
            return 0.0
        return math.sqrt(length_squared)

    def get_distance(self, vec: "Vector3D") -> float:
        x = (self.x - vec.x) ** 2
        y = (self.y - vec.y) ** 2
        z = (self.z - vec.z) ** 2

        distance = math.sqrt(x + y + z)
        return distance
