import turtle
import math


class ShapeProjectorBase:
    def __init__(self, shape: list[tuple[float, float, float]]):
        self._shape = shape
        self._turtle_screen = turtle.Screen()
        self._turtle_object = turtle.Turtle()
        self._setup_turtle()
        self._mouse_states = [[], []]

        self._x_angle = 0
        self._y_angle = 0
        self._z_angle = 0
        self._scale = 50
        self._center_x = 0
        self._center_y = 0

    def _setup_turtle(self):
        self._turtle_screen.bgcolor((0, 0, 0))
        self._turtle_object.pencolor("light blue")
        self._turtle_object.pensize(3)
        self._turtle_object.hideturtle()
        self._turtle_screen.tracer(0)

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

    def _draw_line(self, a: tuple[float, float, float], b: tuple[float, float, float]):
        x1 = a[0] * self._scale + self._center_x
        y1 = a[1] * self._scale + self._center_y
        x2 = b[0] * self._scale + self._center_x
        y2 = b[1] * self._scale + self._center_y
        self._turtle_object.penup()
        self._turtle_object.goto(x1, y1)
        self._turtle_object.pendown()
        self._turtle_object.goto(x2, y2)


class ShapeProjector(ShapeProjectorBase):
    def __init__(self, shape: list[tuple[float, float, float]]):
        super().__init__(shape)

    def set_color(self, color):
        self._turtle_object.pencolor(color)

    def draw_shape(self, x: float, y: float):
        self._center_x, self._center_y = x, y
        self._turtle_object.clear()
        for i in range(4):
            s1 = (i + 1) % 4
            s2 = i + 4
            s3 = s1 + 4
            shape_i = self._shape[i]
            shape_s1 = self._shape[s1]
            shape_s2 = self._shape[s2]
            shape_s3 = self._shape[s3]
            self._draw_line(shape_i, shape_s1)
            self._draw_line(shape_i, shape_s2)
            self._draw_line(shape_s2, shape_s3)
        self._turtle_screen.update()

    def add_x_angle_rotation(self, rotation: float):
        x_angle = self._x_angle + rotation
        self._shape = [self._rotate_x(p, x_angle) for p in self._shape]
        return self

    def add_y_angle_rotation(self, rotation: float):
        y_angle = self._y_angle + rotation
        self._shape = [self._rotate_y(p, y_angle) for p in self._shape]
        return self

    def add_z_angle_rotation(self, rotation: float):
        z_angle = self._z_angle + rotation
        self._shape = [self._rotate_z(p, z_angle) for p in self._shape]
        return self

    def add_total_angle_rotation(self, rotation: float):
        self.add_x_angle_rotation(rotation)
        self.add_y_angle_rotation(rotation)
        self.add_z_angle_rotation(rotation)
        return self


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


def get_circle_position(radius: float, step: float):
    point = ((radius * math.cos(step) + 2), (radius * math.sin(step) + 2))
    return point


projector = ShapeProjector(shape)

while True:
    projector.draw_shape(0, 0)
    projector.add_total_angle_rotation(0.001)
