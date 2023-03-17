from turtle import Turtle, Screen, ScrolledCanvas

from components.color import RGBA
from components.utils import clamp_float


class GraphicsScreen:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.screen = Screen()
        self.turtle = Turtle()
        self.setup_coordinates(width, height)

    def get_screen_coordinates(
        self, width: int, height: int
    ) -> tuple[float, float, float, float]:
        h_width = width / 2
        h_height = height / 2

        llx = -h_width
        lly = -h_height
        urx = h_width
        ury = h_height
        return (llx, lly, urx, ury)

    def setup(self):
        self.screen.tracer(0)
        self.screen.listen()
        self.turtle.hideturtle()

    def setup_coordinates(self, width: int, height: int):
        coordinates = self.get_screen_coordinates(width, height)
        self.screen.setup(width, height)
        self.screen.setworldcoordinates(*coordinates)
        self.setup()

    def set_screensize(self, width: int, height: int) -> None:
        self.setup_coordinates(width, height)
        self.width = width
        self.height = height

    def set_background_color(self, color: RGBA) -> None:
        rgb = color.rgb_tuple
        self.screen.bgcolor(*rgb)

    def set_title(self, title: str) -> None:
        self.screen.title(title)

    def update(self) -> None:
        self.screen.update()

    def get_screensize(self) -> tuple[int, int]:
        width = self.screen.window_width()
        height = self.screen.window_height()
        return width, height

    def get_width(self) -> int:
        width = self.screen.window_width()
        return width

    def get_height(self) -> int:
        height = self.screen.window_height()
        return height

    def get_canvas(self) -> ScrolledCanvas:
        canvas = self.screen.getcanvas()
        return ScrolledCanvas(canvas)

    def get_pointer_xy(self) -> tuple[int, int]:
        canvas = self.get_canvas()
        return canvas.winfo_pointerxy()


class Graphics(GraphicsScreen):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)

    # Turtle doesn't support alpha channel.
    # This is a limited (in functionality) workaround.
    def handle_alpha_component(self, color: RGBA) -> RGBA:
        bgcolor: tuple[float, float, float] = self.screen.bgcolor()
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
        self.turtle.pencolor(*rgb)
        self.turtle.fillcolor(*rgb)

    def set_draw_thickness(self, size: int) -> None:
        self.turtle.pensize(size)

    def goto_point(self, point: tuple[float, float]) -> None:
        self.turtle.penup()
        self.turtle.goto(point)

    def draw_begin_fill(self, point: tuple[float, float]) -> None:
        self.turtle.penup()
        self.turtle.goto(*point)
        self.turtle.begin_fill()

    def draw_end_fill(self) -> None:
        self.turtle.end_fill()

    def draw_point_to_point(
        self, point1: tuple[float, float], point2: tuple[float, float]
    ) -> None:
        self.turtle.penup()
        self.turtle.goto(*point1)
        self.turtle.pendown()
        self.turtle.goto(*point2)

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
        self.turtle.circle(radius)
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
        font: tuple[str, int, str],
    ) -> None:
        self.goto_point(point)
        self.set_draw_color(color)
        self.turtle.pendown()
        self.turtle.write(arg=text, font=font, align="left")

    def clear_screen(self) -> None:
        self.turtle.clear()
