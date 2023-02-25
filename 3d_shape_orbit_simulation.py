import math

import random
import time

from turtle import Turtle, Screen
from typing_extensions import Self


class GraphicsScreen:
    def __init__(self):
        self.turtle_screen = Screen()
        self.turtle_screen.tracer(0)

    def set_screensize(self, width: int, height: int):
        self.turtle_screen.screensize(width, height)

    def set_background_color(self, r: float, g: float, b: float):
        self.turtle_screen.bgcolor(r, g, b)

    def set_title(self, title: str):
        self.turtle_screen.title(title)

    def update(self):
        self.turtle_screen.update()


class Graphics:
    def __init__(self):
        self.turtle_object = Turtle()
        self.turtle_object.hideturtle()

    def draw_line(
        self,
        p1: tuple[float, float],
        p2: tuple[float, float],
        thickness: int,
        color: tuple[float, float, float],
    ):
        self.turtle_object.pensize(thickness)
        self.turtle_object.pencolor(*color)
        self.turtle_object.fillcolor(*color)
        self.turtle_object.penup()
        self.turtle_object.goto(*p1)
        self.turtle_object.pendown()
        self.turtle_object.goto(*p2)
        self.turtle_object.penup()

    def draw_text(
        self,
        position: tuple[float, float],
        color: tuple[float, float, float],
        text: str,
    ):
        self.turtle_object.pencolor(color)
        self.turtle_object.fillcolor(color)
        self.turtle_object.penup()
        self.turtle_object.goto(position)
        self.turtle_object.write(text, font=("Arial", 24, "normal"))

    def clear_screen(self):
        self.turtle_object.clear()


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

    def get_length(self) -> float:
        return math.sqrt(self.x**2.0 + self.y**2.0 + self.z**2.0)

    def set_magnitude(self, magnitude: float) -> Self:
        length = self.get_length()
        if length > 0:
            self.x = (self.x / length) * magnitude
            self.y = (self.y / length) * magnitude
            self.z = (self.z / length) * magnitude
        return Vector3D(self.x, self.y, self.z)


class Physics:
    def __init__(self, shape: list[tuple[float, float, float]]):
        self.shape = shape
        self.position = Vector3D()
        self.velocity = Vector3D()
        self.acceleration = Vector3D()
        self.spin_velocity = Vector3D()
        self.spin_acceleration = Vector3D()
        self.mass = 1.0
        self.scale = 1.0

    @staticmethod
    def _rotate_x(
        xyz_point: tuple[float, float, float], theta: float
    ) -> tuple[float, float, float]:
        cs = math.cos(theta)
        sn = math.sin(theta)
        x = xyz_point[0]
        y = (cs * xyz_point[1]) - (sn * xyz_point[2])
        z = (sn * xyz_point[1]) + (cs * xyz_point[2])
        return (x, y, z)

    @staticmethod
    def _rotate_y(
        xyz_point: tuple[float, float, float], theta
    ) -> tuple[float, float, float]:
        cs = math.cos(theta)
        sn = math.sin(theta)
        x = (cs * xyz_point[0]) + (sn * xyz_point[2])
        y = xyz_point[1]
        z = (-sn * xyz_point[0]) + (cs * xyz_point[2])
        return (x, y, z)

    @staticmethod
    def _rotate_z(
        xyz_point: tuple[float, float, float], theta: float
    ) -> tuple[float, float, float]:
        cs = math.cos(theta)
        sn = math.sin(theta)
        x = (cs * xyz_point[0]) - (sn * xyz_point[1])
        y = (sn * xyz_point[0]) + (cs * xyz_point[1])
        z = xyz_point[2]
        return (x, y, z)

    @staticmethod
    def _constrain(val: float, min_val: float, max_val: float) -> float:
        return min(max_val, max(min_val, val))

    def _calculate_position(self) -> None:
        self.position = self.position.add_vector(self.velocity)
        self.velocity = self.velocity.add_vector(self.acceleration)

    def _calculate_spin(self):
        self.spin_velocity = self.spin_velocity.add_vector(self.spin_acceleration)
        x_rotation = self.spin_velocity.x
        y_rotation = self.spin_velocity.y
        z_rotation = self.spin_velocity.z
        shape = []
        for point in self.shape:
            point = self._rotate_x(point, x_rotation)
            point = self._rotate_y(point, y_rotation)
            point = self._rotate_z(point, z_rotation)
            shape.append(point)
        self.shape = shape

    def set_position(self, x: float, y: float, z: float):
        self.position = Vector3D(x, y, z)

    def set_velocity(self, x: float, y: float, z: float):
        self.velocity = Vector3D(x, y, z)

    def set_spin_velocity(self, x: float, y: float, z: float):
        self.spin_velocity = Vector3D(x, y, z)

    def set_acceleration(self, x: float, y: float, z: float):
        self.acceleration = Vector3D(x, y, z)

    def set_mass(self, mass: float):
        self.mass = mass

    def set_scale(self, scale: float):
        self.scale = scale

    def apply_attraction(self, target: Self):
        force = target.position.subtract_vector(self.position)
        distance = force.get_length()
        g_const = 0.0001
        strength = g_const * ((self.mass * target.mass) / distance)
        force = force.set_magnitude(strength)
        force = force.divide(self.mass)
        self.acceleration = self.acceleration.add_vector(force)
        self.spin_acceleration = self.spin_acceleration.add_vector(force)

    def move_object(self):
        self._calculate_position()
        self._calculate_spin()
        self.acceleration = self.acceleration.multiply(0)
        self.spin_acceleration = self.spin_acceleration.multiply(0)


class Shape:
    def __init__(self, shape: list[tuple[float, float, float]]):
        self.physics = Physics(shape)
        self.color = (1.0, 1.0, 1.0)
        self.line_thickness = 3

    @staticmethod
    def _perspective_projection(
        xyz_point: tuple[float, float, float]
    ) -> tuple[float, float, float]:
        distance = 5
        zp = 1 / (distance - xyz_point[2])
        xp = xyz_point[0] * zp
        yp = xyz_point[1] * zp
        return (xp, yp, zp)

    def _draw_edge(
        self,
        a: tuple[float, float, float],
        b: tuple[float, float, float],
        color_shading: float,
        graphics: Graphics,
    ):
        scale = self.physics.scale
        z = self.physics.position.z
        relative_z = scale + z
        relative_z = min(float("inf"), max(0, relative_z))

        x1 = a[0] * relative_z + self.physics.position.x
        y1 = a[1] * relative_z + self.physics.position.y
        x2 = b[0] * relative_z + self.physics.position.x
        y2 = b[1] * relative_z + self.physics.position.y

        color = tuple((i * color_shading for i in self.color))
        graphics.draw_line((x1, y1), (x2, y2), self.line_thickness, color)

    def _draw_edge_perspective(
        self,
        a: tuple[float, float, float],
        b: tuple[float, float, float],
        color_shading: float,
        graphics: Graphics,
    ):
        a = self._perspective_projection(a)
        b = self._perspective_projection(b)
        self._draw_edge(a, b, color_shading, graphics)

    def set_color(self, color: tuple[float, float, float]):
        self.color = color

    def draw_shape(self, graphics: Graphics):
        for i in range(4):
            s1 = (i + 1) % 4
            s2 = i + 4
            s3 = s1 + 4
            shape_i = self.physics.shape[i]
            shape_s1 = self.physics.shape[s1]
            shape_s2 = self.physics.shape[s2]
            shape_s3 = self.physics.shape[s3]
            self._draw_edge(shape_i, shape_s1, 1.0, graphics)
            self._draw_edge(shape_i, shape_s2, 0.85, graphics)
            self._draw_edge(shape_s2, shape_s3, 0.75, graphics)


class Simulation:
    def __init__(self, graphics: Graphics) -> None:
        self.graphics = graphics
        self.fps_txp = (-300, 300)
        self.fps_txc = (0.8, 0.8, 0.8)
        self.objects: list[Shape] = []
        self.timestep = 0.1

    @staticmethod
    def get_shape():
        shape = [
            (-1, -1, -1),
            (1, -1, -1),
            (1, 1, -1),
            (-1, 1, -1),
            (-1, -1, 1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, 1, 1),
        ]
        return shape

    def add_center_object(self) -> None:
        mass = 10_000_000
        shape = self.get_shape()
        color = (0.8, 0.3, 0.3)
        scale = mass / 250_000

        p = Shape(shape)
        p.set_color(color)
        p.physics.set_mass(mass)
        p.physics.set_scale(scale)
        p.physics.set_spin_velocity(0, 0, 0)
        self.objects.append(p)

    def add_orbiting_object(self) -> None:
        x = random.uniform(-50, -40)
        y = random.uniform(-50, -40)
        z = 0

        mass = random.uniform(50, 100)
        shape = self.get_shape()
        scale = mass / 20

        p = Shape(shape)
        p.physics.set_position(x, y, z)
        p.physics.set_velocity(10, 30, 5)
        p.physics.set_mass(mass)
        p.physics.set_scale(scale)
        self.objects.append(p)

    def setup_objects(self) -> None:
        self.add_center_object()
        for _ in range(15):
            self.add_orbiting_object()

    def compute_all_objects(self) -> None:
        for pl1 in self.objects:
            for pl2 in self.objects:
                if pl1 == pl2:
                    continue
                pl1.physics.apply_attraction(pl2.physics)

            pl1.physics.move_object()
            pl1.draw_shape(self.graphics)

    def timestep_adjustment(self, frame_en: float) -> int:
        self.timestep = frame_en
        return 0

    def write_fps(self, frame_time: float):
        fps = f"{1 / frame_time:.2f} FPS"
        self.graphics.draw_text(self.fps_txp, self.fps_txc, fps)

    def start_simulation(self, graphics_screen: GraphicsScreen):
        while True:
            self.graphics.clear_screen()
            frame_st = time.perf_counter()
            self.compute_all_objects()

            # frame_en = time.perf_counter() - frame_st
            # frame_hold = self.timestep - frame_en

            # if frame_hold < 0 or frame_hold > 0.01:
            #     frame_hold = self.timestep_adjustment(frame_en)

            # time.sleep(frame_hold)
            frame_time = time.perf_counter() - frame_st
            self.write_fps(frame_time)
            graphics_screen.update()


def main():
    graphics = Graphics()
    graphics_screen = GraphicsScreen()

    graphics_screen.set_title("Physics System")
    graphics_screen.set_screensize(640, 640)
    graphics_screen.set_background_color(0.15, 0.15, 0.15)

    simulation = Simulation(graphics)
    simulation.setup_objects()
    simulation.start_simulation(graphics_screen)


if __name__ == "__main__":
    main()
