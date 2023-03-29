from components.vectors import Vector3D

from dataclasses import dataclass


@dataclass(frozen=True)
class RGBA:
    red: float
    green: float
    blue: float
    alpha: float

    @property
    def rgb_tuple(self) -> tuple[float, float, float]:
        return (self.red, self.green, self.blue)

    @property
    def rgb_tuple_u8(self) -> tuple[int, int, int]:
        red = int(self.red * 255)
        green = int(self.green * 255)
        blue = int(self.blue * 255)
        return (red, green, blue)

    @property
    def rgba_tuple(self) -> tuple[float, float, float, float]:
        return (self.red, self.green, self.blue, self.alpha)

    @classmethod
    def from_rgb(cls, red: float, green: float, blue: float) -> "RGBA":
        """Create the RGBA dataclass from RGB parameters
        with the alpha channel set to 1.0."""
        return RGBA(red, green, blue, 1.0)

    @classmethod
    def from_vector(cls, vector: Vector3D):
        """Create the RGBA dataclass from a Vector3D object
        with the alpha channel set to 1.0."""
        return RGBA(vector.x, vector.y, vector.z, 1.0)

    @classmethod
    def from_rgba_tuple(cls, rgba: tuple[float, float, float, float]) -> "RGBA":
        "Create the RGBA dataclass from an (R, G, B, A) tuple."
        return RGBA(rgba[0], rgba[1], rgba[2], rgba[3])

    @classmethod
    def from_rgb_tuple(cls, rgb: tuple[float, float, float]) -> "RGBA":
        """Create the RGBA dataclass from an (R, G, B) tuple
        with the alpha channel set to 1.0."""
        return RGBA(rgb[0], rgb[1], rgb[2], 1.0)

    def multiply(self, color: "RGBA") -> "RGBA":
        red = self.red * color.red
        green = self.green * color.green
        blue = self.blue * color.blue
        alpha = self.alpha * color.alpha
        return RGBA(red, green, blue, alpha)

    def clamp(self, min_value: float, max_value: float) -> "RGBA":
        red = max(min_value, min(self.red, max_value))
        green = max(min_value, min(self.green, max_value))
        blue = max(min_value, min(self.red, max_value))
        alpha = max(min_value, min(self.red, max_value))
        return RGBA(red, green, blue, alpha)
