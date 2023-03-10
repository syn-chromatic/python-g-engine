from turtle import Turtle, Screen, ScrolledCanvas

from components.color import RGBA
from components.utils import clamp_float


class GraphicsScreen:
    def __new__(cls) -> "GraphicsScreen":
        if not hasattr(cls, "instance"):
            cls.instance = super(GraphicsScreen, cls).__new__(cls)
            cls.turtle_screen = Screen()
            cls.turtle_screen.tracer(0)
            cls.turtle_screen.listen()

            cls.turtle_object = Turtle()
            cls.turtle_object.hideturtle()

        return cls.instance

    def set_screensize(self, width: int, height: int) -> None:
        self.turtle_screen.screensize(width, height)

    def set_background_color(self, color: RGBA) -> None:
        rgb = color.rgb_tuple
        self.turtle_screen.bgcolor(*rgb)

    def set_title(self, title: str) -> None:
        self.turtle_screen.title(title)

    def update(self) -> None:
        self.turtle_screen.update()

    def get_canvas(self) -> ScrolledCanvas:
        canvas = self.turtle_screen.getcanvas()
        return ScrolledCanvas(canvas)

    def get_pointer_xy(self) -> tuple[int, int]:
        canvas = self.get_canvas()
        return canvas.winfo_pointerxy()


class Graphics(GraphicsScreen):
    def __init__(self):
        super().__init__()

    # Turtle doesn't support alpha channel.
    # This is a limited (in functionality) workaround.
    def handle_alpha_component(self, color: RGBA) -> RGBA:
        bgcolor: tuple[float, float, float] = self.turtle_screen.bgcolor()
        rgba = color.rgba_tuple
        alpha_channel = color.alpha
        rgb = []
        for bg_channel, channel in zip(bgcolor, rgba[:3]):
            channel *= alpha_channel

            norm_dividend = channel - bg_channel
            norm_divisor = 1.0 - bg_channel

            ch_normalized = norm_dividend / norm_divisor
            ch_clamped = clamp_float(ch_normalized, bg_channel, 1.0)
            rgb.append(ch_clamped)

        color = RGBA.from_rgb_tuple(tuple(rgb))
        return color

    def set_draw_color(self, color: RGBA) -> None:
        rgb = color.rgb_tuple
        self.turtle_object.pencolor(*rgb)
        self.turtle_object.fillcolor(*rgb)

    def set_draw_thickness(self, size: int) -> None:
        self.turtle_object.pensize(size)

    def goto_point(self, point: tuple[float, float]) -> None:
        self.turtle_object.penup()
        self.turtle_object.goto(point)

    def draw_begin_fill(self, point: tuple[float, float]) -> None:
        self.turtle_object.penup()
        self.turtle_object.goto(*point)
        self.turtle_object.begin_fill()

    def draw_end_fill(self) -> None:
        self.turtle_object.end_fill()

    def draw_point_to_point(
        self, point1: tuple[float, float], point2: tuple[float, float]
    ) -> None:
        self.turtle_object.penup()
        self.turtle_object.goto(*point1)
        self.turtle_object.pendown()
        self.turtle_object.goto(*point2)
        self.turtle_object.penup()

    def draw_circle(
        self,
        point: tuple[float, float],
        radius: float,
        color: RGBA,
    ) -> None:
        x, y = point
        point = x, y - radius

        color = self.handle_alpha_component(color)
        self.set_draw_color(color)
        self.draw_begin_fill(point)
        self.turtle_object.circle(radius)
        self.draw_end_fill()

    def draw_line(
        self,
        point1: tuple[float, float],
        point2: tuple[float, float],
        thickness: int,
        color: RGBA,
    ) -> None:
        color = self.handle_alpha_component(color)
        self.set_draw_thickness(thickness)
        self.set_draw_color(color)
        self.draw_point_to_point(point1, point2)

    def draw_text(
        self,
        point: tuple[float, float],
        color: RGBA,
        text: str,
    ) -> None:
        self.set_draw_color(color)
        self.goto_point(point)
        self.turtle_object.write(text, font=("Arial", 24, "normal"))

    def clear_screen(self) -> None:
        self.turtle_object.clear()
