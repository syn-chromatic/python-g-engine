import pygame as pyg
import time
from turtle import Turtle, Screen, ScrolledCanvas

from components.shared_dcs import Polygons, Triangles, Quads, KeyRegister
from components.font import FontSettings
from components.color import RGBA
from components.graphics_abc import GraphicsABC
from components.utils import clamp_float

from typing import Callable, Optional


class TurtleGraphicsBase(GraphicsABC):
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.screen = Screen()
        self.turtle = Turtle()
        self.setup_coordinates(width, height)

    def update(self) -> None:
        self.screen.update()

    def setup(self):
        self.screen.tracer(0)
        self.screen.listen()
        self.turtle.hideturtle()

    def setup_coordinates(self, width: int, height: int):
        coordinates = self.get_screen_coordinates(width, height)
        self.screen.setup(width, height)
        self.screen.setworldcoordinates(*coordinates)
        self.setup()

    def register_onkeypress(
        self, func: Callable, key: str, is_repeatable: bool = True
    ) -> None:
        self.screen.onkeypress(func, key)

    def set_screensize(self, width: int, height: int) -> None:
        self.setup_coordinates(width, height)
        self.width = width
        self.height = height

    def set_background_color(self, color: RGBA) -> None:
        rgb = color.rgb_tuple
        self.screen.bgcolor(*rgb)

    def set_title(self, title: str) -> None:
        self.screen.title(title)

    def get_screensize(self) -> tuple[int, int]:
        width = self.screen.window_width()
        height = self.screen.window_height()
        return width, height

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


class TurtleGraphics(TurtleGraphicsBase):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)

    # Turtle doesn't support alpha channel.
    # This is a limited (in functionality) workaround.
    def handle_alpha_component(self, color: RGBA) -> RGBA:
        if color.alpha == 1.0:
            return color

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

    def draw_polygons(self, polygons: list[Polygons]):
        for polys in polygons:
            polys_type = polys.type
            if isinstance(polys_type, Triangles):
                self.draw_triangles(polys_type)

            elif isinstance(polys_type, Quads):
                self.draw_quads(polys_type)

    def draw_triangles(self, triangles: Triangles):
        vertices = triangles.vertices
        faces = triangles.faces
        shaders = triangles.shaders
        len_shaders = len(shaders)

        for idx, face in enumerate(faces):
            if any(i >= len(vertices) for i in face):
                print("Warning: Skipping face with out-of-bounds vertex indices.")
                continue

            v1, v2, v3 = [vertices[i] for i in face]
            p1 = v1.to_tuple()[:2]
            p2 = v2.to_tuple()[:2]
            p3 = v3.to_tuple()[:2]

            color = triangles.color
            color = tuple(ch / 255 for ch in color)

            if len_shaders > idx:
                shading = shaders[idx]
                color = tuple(ch * shading_ch for ch, shading_ch in zip(color, shading))

            self.turtle.pencolor("black")
            self.turtle.fillcolor(color)
            self.draw_begin_fill(p1)

            self.turtle.pendown()
            self.turtle.goto(p2)
            self.turtle.goto(p3)
            self.turtle.goto(p1)
            self.draw_end_fill()

    def draw_quads(self, quads: Quads):
        vertices = quads.vertices
        faces = quads.faces

        for face in faces:
            if any(i >= len(vertices) for i in face):
                print("Warning: Skipping face with out-of-bounds vertex indices.")
                continue

            v1, v2, v3, v4 = [vertices[i] for i in face]
            p1 = v1.to_tuple()[:2]
            p2 = v2.to_tuple()[:2]
            p3 = v3.to_tuple()[:2]
            p4 = v4.to_tuple()[:2]

            self.turtle.pencolor("black")
            self.turtle.fillcolor("lightgray")
            self.draw_begin_fill(p1)

            self.turtle.pendown()
            self.turtle.goto(p2)
            self.turtle.goto(p3)
            self.turtle.goto(p4)
            self.turtle.goto(p1)
            self.draw_end_fill()

    def draw_text(
        self, point: tuple[float, float], text: str, font_settings: FontSettings
    ) -> None:
        color = font_settings.font_color
        font_tuple = font_settings.font_tuple
        self.goto_point(point)
        self.set_draw_color(color)
        self.turtle.pendown()
        self.turtle.write(arg=text, font=font_tuple, align="left")

    def clear_screen(self) -> None:
        self.turtle.clear()


class PygGraphicsBase(GraphicsABC):
    def __init__(self, width: int, height: int) -> None:
        pyg.init()
        self.width = width
        self.height = height
        self.screen = pyg.display.set_mode((width, height))
        self.clock = pyg.time.Clock()
        self.default_font = pyg.font.get_default_font()
        self.bg_color = RGBA(1.0, 1.0, 1.0, 1.0)
        # self.registered_keys: dict[int, dict[str, Union[Callable, bool, float]]] = {}
        self.registered_keys: list[KeyRegister] = []

    def update(self) -> None:
        events = self.get_events()
        self.set_onkeypress(events)
        self.event_onkeypress()
        # print("frame")
        pyg.display.flip()
        self.clock.tick(60)

    def set_screensize(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.screen = pyg.display.set_mode((width, height))

    def set_background_color(self, color: RGBA) -> None:
        self.bg_color = color

    def set_title(self, title: str) -> None:
        self.title = title
        pyg.display.set_caption(title)

    def get_available_scancode(self, key: str) -> Optional[int]:
        scancodes = {
            "up": 1073741906,
            "down": 1073741905,
            "right": 1073741903,
            "left": 1073741904,
        }
        key = key.lower()
        if key in scancodes:
            return scancodes[key]

    def add_key_register(
        self, key: str, scancode: int, func: Callable, is_repeatable: bool
    ):
        unix_time = time.time()
        key_register = KeyRegister(
            key=key,
            scancode=scancode,
            function=func,
            press_time=unix_time,
            is_pressed=False,
            is_repeatable=is_repeatable,
        )
        self.registered_keys.append(key_register)

    def register_onkeypress(
        self, func: Callable, key: str, is_repeatable: bool = True
    ) -> None:
        if len(key) == 1:
            scancode = ord(key)
            self.add_key_register(key, scancode, func, is_repeatable)

        elif len(key) > 1:
            scancode = self.get_available_scancode(key)
            if not scancode:
                print(f"WARNING: '{key}' FAILED TO REGISTER.")
                return
            self.add_key_register(key, scancode, func, is_repeatable)

    def set_onkeypress(self, events: list[pyg.event.Event]):
        pressed = pyg.key.get_pressed()

        for event in events:
            if event.type == pyg.KEYDOWN:
                for key_register in self.registered_keys:
                    scancode = key_register.scancode
                    if pressed[scancode]:
                        unix_time = time.time()
                        key_register.is_pressed = True
                        key_register.press_time = unix_time

            if event.type == pyg.KEYUP:
                for key_register in self.registered_keys:
                    scancode = key_register.scancode
                    is_repeatable = key_register.is_repeatable
                    if not pressed[scancode] and is_repeatable:
                        unix_time = time.time()
                        key_register.is_pressed = False
                        key_register.press_time = unix_time

    def event_onkeypress(self):
        key_delay = 0.03
        for key_register in self.registered_keys:
            if key_register.is_pressed:
                press_time = key_register.press_time

                unix_time = time.time()
                time_interval = unix_time - press_time
                if key_register.is_repeatable:
                    if time_interval > key_delay:
                        key_register.function()

                else:
                    key_register.function()
                    key_register.is_pressed = False

    def get_events(self) -> list[pyg.event.Event]:
        events = pyg.event.get()
        return events

    def get_screensize(self) -> tuple[int, int]:
        width = self.screen.get_rect().width
        height = self.screen.get_rect().height
        return width, height

    def get_width(self) -> int:
        width = self.screen.get_rect().width
        return width

    def get_height(self) -> int:
        height = self.screen.get_rect().height
        return height

    def get_pointer_xy(self) -> tuple[int, int]:
        pointer_pos = pyg.mouse.get_pos()
        return pointer_pos

    def get_centered_coordinates(
        self, position: tuple[float, float]
    ) -> tuple[float, float]:
        cx, cy = self.screen.get_rect().center
        position = position[0] + cx, -position[1] + cy
        return position


class PygGraphics(PygGraphicsBase):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)

    def set_draw_thickness(self, size: int) -> None:
        pass

    def goto_point(self, point: tuple[float, float]) -> None:
        pass

    def draw_begin_fill(self, point: tuple[float, float]) -> None:
        pass

    def draw_end_fill(self) -> None:
        pass

    def draw_point_to_point(
        self, point1: tuple[float, float], point2: tuple[float, float]
    ) -> None:
        pass

    def draw_circle(
        self,
        point: tuple[float, float],
        radius: float,
        color: RGBA,
    ) -> None:
        x, y = point
        rgb_tuple = tuple(int(channel * 255) for channel in color.rgb_tuple)
        pyg.draw.circle(self.screen, rgb_tuple, (int(x), int(y)), int(radius))

    def draw_line(
        self,
        point1: tuple[float, float],
        point2: tuple[float, float],
        thickness: int,
        color: RGBA,
    ) -> None:
        rgb_tuple = tuple(int(channel * 255) for channel in color.rgb_tuple)
        pyg.draw.line(self.screen, rgb_tuple, point1, point2, thickness)

    def draw_polygons(self, polygons: list[Polygons]):
        for polys in polygons:
            polys_type = polys.type
            if isinstance(polys_type, Triangles):
                self.draw_triangles(polys_type)

            elif isinstance(polys_type, Quads):
                self.draw_quads(polys_type)

    def draw_triangles(self, triangles: Triangles):
        vertices = triangles.vertices
        faces = triangles.faces
        shaders = triangles.shaders

        len_shaders = len(shaders)

        for idx, face in enumerate(faces):
            if any(i >= len(vertices) for i in face):
                print("Warning: Skipping face with out-of-bounds vertex indices.")
                continue

            v1, v2, v3 = [vertices[i] for i in face]

            p1 = v1.to_tuple()[:2]
            p2 = v2.to_tuple()[:2]
            p3 = v3.to_tuple()[:2]

            p1 = self.get_centered_coordinates(p1)
            p2 = self.get_centered_coordinates(p2)
            p3 = self.get_centered_coordinates(p3)

            points = [p1, p2, p3]
            color = triangles.color
            line_shading = (0.5, 0.5, 0.5)
            line_color = tuple(
                int(ch * shading_ch) for ch, shading_ch in zip(color, line_shading)
            )

            if len_shaders > idx:
                shading = shaders[idx]
                color = tuple(
                    int(ch * shading_ch) for ch, shading_ch in zip(color, shading)
                )

            pyg.draw.polygon(self.screen, color, points)
            pyg.draw.lines(self.screen, (5, 5, 5), True, points, 1)

    def draw_quads(self, quads: Quads):
        vertices = quads.vertices
        faces = quads.faces

        for face in faces:
            if any(i >= len(vertices) for i in face):
                print("Warning: Skipping face with out-of-bounds vertex indices.")
                continue

            v1, v2, v3, v4 = [vertices[i] for i in face]

            p1 = v1.to_tuple()[:2]
            p2 = v2.to_tuple()[:2]
            p3 = v3.to_tuple()[:2]
            p4 = v4.to_tuple()[:2]

            p1 = self.get_centered_coordinates(p1)
            p2 = self.get_centered_coordinates(p2)
            p3 = self.get_centered_coordinates(p3)
            p4 = self.get_centered_coordinates(p4)

            points = [p1, p2, p3, p4]

            pyg.draw.polygon(self.screen, (200, 200, 200), points)
            pyg.draw.lines(self.screen, (0, 0, 0), True, points, 1)

    def draw_text(
        self, point: tuple[float, float], text: str, font_settings: FontSettings
    ) -> None:
        point = self.get_centered_coordinates(point)
        font = pyg.font.Font(self.default_font, font_settings.font_tuple[1])
        color = font_settings.font_color
        rgb_tuple = tuple(int(channel * 255) for channel in color.rgb_tuple)
        text_surface = font.render(text, True, rgb_tuple)
        self.screen.blit(text_surface, point)

    def clear_screen(self) -> None:
        rgb_tuple = self.bg_color.rgb_tuple
        rgb_tuple = tuple(int(channel * 255) for channel in rgb_tuple)
        self.screen.fill(rgb_tuple)
