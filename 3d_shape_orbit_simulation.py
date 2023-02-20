import turtle
import math

import random
import time

from typing_extensions import Self


class Vector3D:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0) -> None:
        self.x = x
        self.y = y
        self.z = z

    def get_tuple(self) -> tuple[float, float, float]:
        return self.x, self.y, self.z

    def multiply(self, num: float) -> Self:
        return Vector3D(self.x * num, self.y * num, self.z * num)

    def divide(self, num: float) -> Self:
        return Vector3D(self.x / num, self.y / num, self.z / num)

    def add_vector(self, vec: Self) -> Self:
        return Vector3D(self.x + vec.x, self.y + vec.y, self.z + vec.z)

    def subtract_vector(self, vec: Self) -> Self:
        return Vector3D(self.x - vec.x, self.y - vec.y, self.z - vec.z)

    def get_length(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def set_magnitude(self, magnitude: float) -> Self:
        length = self.get_length()
        if length != 0:
            self.x = (self.x / length) * magnitude
            self.y = (self.y / length) * magnitude
            self.z = (self.z / length) * magnitude
        return self


class ShapeProjectorBase:
    def __init__(
        self, shape: list[tuple[float, float, float]], x: float, y: float, z: float
    ):
        self._shape = shape
        self._turtle_screen = turtle.Screen()
        self._turtle_object = turtle.Turtle()
        self._setup_turtle()
        self._mouse_states = [[], []]
        self._color = (1.0, 1.0, 1.0)

        self._x_angle = 0
        self._y_angle = 0
        self._z_angle = 0
        self._scale = 1

        self.position = Vector3D(x, y, z)
        self.velocity = Vector3D(0, 0, 0)
        self.acceleration = Vector3D(0, 0, 0)
        self.mass = 1
        self.size = 1

    def _setup_turtle(self):
        self._turtle_object.pencolor("light blue")
        self._turtle_object.pensize(3)
        self._turtle_object.hideturtle()

    @staticmethod
    def _rotate_z(xyz_point, theta) -> tuple[float, float, float]:
        cs = math.cos(theta)
        sn = math.sin(theta)
        x = cs * xyz_point[0] - sn * xyz_point[1]
        y = sn * xyz_point[0] + cs * xyz_point[1]
        z = xyz_point[2]
        return (x, y, z)

    @staticmethod
    def _rotate_x(xyz_point, theta) -> tuple[float, float, float]:
        cs = math.cos(theta)
        sn = math.sin(theta)
        x = xyz_point[0]
        y = cs * xyz_point[1] - sn * xyz_point[2]
        z = sn * xyz_point[1] + cs * xyz_point[2]
        return (x, y, z)

    @staticmethod
    def _rotate_y(xyz_point, theta) -> tuple[float, float, float]:
        cs = math.cos(theta)
        sn = math.sin(theta)
        x = cs * xyz_point[0] + sn * xyz_point[2]
        y = xyz_point[1]
        z = -sn * xyz_point[0] + cs * xyz_point[2]
        return (x, y, z)

    @staticmethod
    def _perspective_projection(xyz_point) -> tuple[float, float, float]:
        distance = 5

        z = 1 / (distance - xyz_point[2])
        x = xyz_point[0] * z
        y = xyz_point[1] * z
        return (x, y, z)

    def _set_color(self, color: tuple[float, float, float]):
        self._turtle_object.pencolor(*color)
        self._turtle_object.fillcolor(*color)

    def _draw_line(
        self,
        a: tuple[float, float, float],
        b: tuple[float, float, float],
        scale: float,
        color_shading: float,
    ):
        x1 = a[0] * scale + self.position.x
        y1 = a[1] * scale + self.position.y
        x2 = b[0] * scale + self.position.x
        y2 = b[1] * scale + self.position.y

        color = tuple((i * color_shading for i in self._color))
        self._set_color(color)
        self._turtle_object.penup()
        self._turtle_object.goto(x1, y1)
        self._turtle_object.pendown()
        self._turtle_object.goto(x2, y2)
        self._set_color(color)


class ShapeProjector(ShapeProjectorBase):
    def __init__(
        self, shape: list[tuple[float, float, float]], x: float, y: float, z: float
    ):
        super().__init__(shape, x, y, z)

    def draw_shape(self, scale):
        self._turtle_object.clear()
        for i in range(4):
            s1 = (i + 1) % 4
            s2 = i + 4
            s3 = s1 + 4
            self._draw_line(self._shape[i], self._shape[s1], scale, 1.0)
            self._draw_line(self._shape[i], self._shape[s2], scale, 0.85)
            self._draw_line(self._shape[s2], self._shape[s3], scale, 0.75)

        self._turtle_screen.update()

    def add_x_angle_rotation(self, rotation: float):
        self._x_angle += rotation
        self._shape = [self._rotate_x(p, self._x_angle) for p in self._shape]
        return self

    def add_y_angle_rotation(self, rotation: float):
        self._y_angle += rotation
        self._shape = [self._rotate_y(p, self._y_angle) for p in self._shape]
        return self

    def add_z_angle_rotation(self, rotation: float):
        self._z_angle += rotation
        self._shape = [self._rotate_z(p, self._z_angle) for p in self._shape]
        return self

    def add_total_angle_rotation(self, rotation: float):
        self._x_angle += rotation
        self._y_angle += rotation
        self._z_angle += rotation

        self._shape = [self._rotate_x(p, self._x_angle) for p in self._shape]
        self._shape = [self._rotate_y(p, self._y_angle) for p in self._shape]
        self._shape = [self._rotate_z(p, self._z_angle) for p in self._shape]
        return self

    def set_mass(self, mass: float) -> Self:
        self.mass = mass
        return self

    def set_scale(self, scale: float):
        self._scale = scale

    def set_shapesize(self, shapesize: tuple[float, float]) -> None:
        self._turtle_object.shapesize(*shapesize)

    def set_color(self, color: tuple[float, float, float]) -> None:
        self._color = color
        self._set_color(color)

    def with_trail(self) -> Self:
        self._turtle_object.pendown()
        return self

    def random_velocity(self, min_range: float = 0, max_range: float = 1) -> Self:
        self.velocity.x = random.uniform(min_range, max_range)
        self.velocity.y = random.uniform(min_range, max_range)
        return self

    def set_velocity(self, x: float, y: float, z: float) -> Self:
        self.velocity.x = x
        self.velocity.y = y
        self.velocity.z = z
        return self

    def set_acceleration(self, x: float, y: float, z: float) -> Self:
        self.acceleration.x = x
        self.acceleration.y = y
        self.acceleration.z = z
        return self

    def move_object(self):
        x, y, z = self.position.get_tuple()
        # self._turtle_object.pensize(self.trail_thickness)

        # self._scale += z
        scale = self._scale + z
        scale = min(float("inf"), max(0, scale))
        # print(self._scale)
        self.draw_shape(scale)
        # self._turtle_object.goto(x, y)

    def update(self) -> Self:
        self.position = self.position.add_vector(self.velocity)
        self.velocity = self.velocity.add_vector(self.acceleration)
        self.acceleration = self.acceleration.multiply(0)
        self.move_object()
        return self

    @staticmethod
    def constrain(val: float, min_val: float, max_val: float) -> float:
        return min(max_val, max(min_val, val))

    def apply_force(self, force: Vector3D) -> None:
        force = force.divide(self.mass)
        self.acceleration = self.acceleration.add_vector(force)

    def apply_angular_force(self, force: Vector3D):
        xf, yf, zf = force.get_tuple()
        self.add_x_angle_rotation(xf / 10000000)
        self.add_y_angle_rotation(yf / 10000000)
        self.add_z_angle_rotation(zf / 10000000)

    def apply_attraction(self, target: Self) -> None:
        force = target.position.subtract_vector(self.position)
        distance = force.get_length()
        g_const = 0.0005
        strength = g_const * (self.mass * target.mass) / distance
        force = force.set_magnitude(strength)
        self.apply_force(force)
        self.apply_angular_force(force)


class Simulation:
    def __init__(self) -> None:
        self.objects: list[ShapeProjector] = []
        self.turtle_screen = turtle.Screen()
        self.turtle_screen.tracer(0)
        self.turtle_screen.bgcolor((0.1, 0.1, 0.1))
        self.turtle_screen.title("Orbital System")
        self.timestep = 0.01

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
        x, y = 0, 0
        z = 0
        shape = self.get_shape()
        mass = 500_000

        p = ShapeProjector(shape, x, y, z)
        p.set_velocity(0, 0, 0)
        p.set_color((0.8, 0.2, 0.2))
        p.set_mass(mass)
        p.set_scale(mass / 10000)
        p.update()
        self.objects.append(p)

    def add_orbiting_object(self) -> None:
        x, y = random.uniform(-400, -200), random.uniform(-400, -200)
        z = 0
        shape = self.get_shape()
        mass = random.uniform(50, 500)

        p = ShapeProjector(shape, x, y, z)
        p.set_velocity(5, -10, 0.1)
        p.set_mass(mass)
        p.set_scale(mass / 50)
        p.update()
        self.objects.append(p)

    def setup_objects(self) -> None:
        self.add_center_object()
        for _ in range(20):
            self.add_orbiting_object()
        self.turtle_screen.update()

    def compute_all_objects(self) -> None:
        for pl1 in self.objects:
            for pl2 in self.objects:
                if pl1 != pl2:
                    pl1.apply_attraction(pl2)

            pl1.update()

    def timestep_adjustment(self, frame_time: float) -> None:
        print(f"ADJUSTING TIMESTEP TO {frame_time}")
        self.timestep = frame_time
        self.turtle_screen.update()

    def start_simulation(self):
        while True:
            frame_st = time.process_time()
            self.compute_all_objects()
            frame_time = time.process_time() - frame_st
            frame_hold = self.timestep - frame_time

            if frame_hold < 0:
                self.timestep_adjustment(frame_time)
                continue
            self.turtle_screen.update()
            time.sleep(frame_time)


sim = Simulation()
sim.setup_objects()
sim.start_simulation()
