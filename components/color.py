from dataclasses import dataclass


@dataclass(frozen=True)
class RGBA:
    red: float
    green: float
    blue: float
    alpha: float

    def __new__(cls, *args, **kwargs) -> "RGBA":
        cls.__set_data__(*args, **kwargs)
        instance = super(RGBA, cls).__new__(RGBA)
        return instance

    @classmethod
    def __set_data__(cls, red: float, green: float, blue: float, alpha: float) -> None:
        cls.red = red
        cls.green = green
        cls.blue = blue
        cls.alpha = alpha

    @property
    def rgb_tuple(self) -> tuple[float, float, float]:
        return (self.red, self.green, self.blue)

    @property
    def rgba_tuple(self) -> tuple[float, float, float, float]:
        return (self.red, self.green, self.blue, self.alpha)

    @classmethod
    def from_tuple(cls, rgba: tuple[float, float, float, float]) -> "RGBA":
        "Create the RGBA dataclass from a tuple."
        return cls.__new__(cls, *rgba)

    @classmethod
    def from_rgb_tuple(cls, rgb: tuple[float, float, float]) -> "RGBA":
        "Create the RGBA dataclass from a tuple with the alpha channel set to 1.0."
        rgba = (*rgb, 1.0)
        return cls.__new__(cls, *rgba)
