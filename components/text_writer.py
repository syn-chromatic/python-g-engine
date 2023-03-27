from components.graphics_abc import GraphicsABC
from components.font import FontSettings

from typing import Optional


class TextWriter:
    def __init__(self, font_settings: FontSettings):
        self.font_settings = font_settings
        self.tl_column: list[tuple[str, Optional[FontSettings]]] = []

    def add_text_top_left(self, text: str, font: Optional[FontSettings] = None):
        self.tl_column.append((text, font))

    def draw(self, graphics: GraphicsABC):
        width = graphics.get_width()
        height = graphics.get_height()

        for idx, (text, font_settings) in enumerate(self.tl_column, 1):
            if not font_settings:
                font_settings = self.font_settings
            text_xy = self.get_text_xy(font_settings, width, height, idx)
            graphics.draw_text(text_xy, text, font_settings)

        self.tl_column = []

    @staticmethod
    def get_padded_top_left_corner(
        width: int, height: int, padding_x: float, padding_y: float
    ) -> tuple[float, float]:
        top_left_x = (-width / 2.0) + padding_x
        top_left_y = (height / 2.0) - padding_y
        return top_left_x, top_left_y

    def get_text_xy(
        self, font_settings: FontSettings, width: int, height: int, idx: int
    ) -> tuple[float, float]:
        font_size = font_settings.font_size
        line_height = font_settings.line_height
        padding_percent = font_settings.padding_percent
        padding_x = width * (padding_percent / 100)
        padding_y = height * (padding_percent / 100)

        text_x = padding_x
        text_y = (font_size * line_height * idx) + (padding_y / line_height)

        text_xy = self.get_padded_top_left_corner(width, height, text_x, text_y)
        return text_xy
