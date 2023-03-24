from components.color import RGBA

from dataclasses import dataclass


class FontType:
    font: str
    style: str


class ArialFontNormal(FontType):
    font: str = "Arial"
    style: str = "normal"


class ArialFontBold(FontType):
    font: str = "Arial"
    style: str = "bold"


@dataclass
class FontSettings:
    font_type: FontType
    font_size: int
    font_color: RGBA
    line_height: float
    padding_percent: int

    @property
    def font_tuple(self) -> tuple[str, int, str]:
        font_name = self.font_type.font
        font_size = self.font_size
        font_style = self.font_type.style
        return (font_name, font_size, font_style)
