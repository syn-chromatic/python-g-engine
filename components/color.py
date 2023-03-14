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
    def rgba_tuple(self) -> tuple[float, float, float, float]:
        return (self.red, self.green, self.blue, self.alpha)

    @classmethod
    def from_rgba_tuple(cls, rgba: tuple[float, float, float, float]) -> "RGBA":
        "Create the RGBA dataclass from an (R, G, B, A) tuple."
        return RGBA(rgba[0], rgba[1], rgba[2], rgba[3])

    @classmethod
    def from_rgb_tuple(cls, rgb: tuple[float, float, float]) -> "RGBA":
        """Create the RGBA dataclass from an (R, G, B) tuple
        with the alpha channel set to 1.0."""
        return RGBA(rgb[0], rgb[1], rgb[2], 1.0)
