import itertools
import math


class SphereShape:
    def __init__(self, long_num: int, lat_num: int, points: int) -> None:
        self.long_num = long_num
        self.lat_num = lat_num
        self.points = points
        self.shape: list[tuple[float, float, float]] = []

    def create_long_points(self) -> None:
        range_long = range(self.long_num)
        range_lat = range(self.lat_num)
        for i, j in itertools.product(range_long, range_lat):
            theta = 2 * math.pi * i / self.long_num
            phi = math.pi * j / (self.lat_num - 1)
            x = 1 * math.sin(phi) * math.cos(theta)
            y = 1 * math.sin(phi) * math.sin(theta)
            z = 1 * math.cos(phi)
            self.shape.append((x, y, z))

    def create_lat_points(self) -> None:
        for i in range(self.points):
            theta = math.pi * i / (self.points)
            for j in range(self.points + 1):
                phi = 2 * math.pi * j / (self.points)
                x = 1 * math.sin(theta) * math.cos(phi)
                y = 1 * math.sin(theta) * math.sin(phi)
                z = 1 * math.cos(theta)
                self.shape.append((x, y, z))

    def get_shape(self) -> list[tuple[float, float, float]]:
        self.create_long_points()
        self.create_lat_points()
        return self.shape


class CubeShape:
    def __init__(self) -> None:
        self.shape: list[tuple[float, float, float]] = []

    def get_shape(self) -> list[tuple[float, float, float]]:
        shape = [
            (-1, -1, -1),
            (1, -1, -1),
            (-1, -1, -1),
            (-1, -1, 1),
            (-1, -1, 1),
            (1, -1, 1),
            (1, -1, -1),
            (1, 1, -1),
            (1, -1, -1),
            (1, -1, 1),
            (1, -1, 1),
            (1, 1, 1),
            (1, 1, -1),
            (-1, 1, -1),
            (1, 1, -1),
            (1, 1, 1),
            (1, 1, 1),
            (-1, 1, 1),
            (-1, 1, -1),
            (-1, -1, -1),
            (-1, 1, -1),
            (-1, 1, 1),
            (-1, 1, 1),
            (-1, -1, 1),
        ]
        return shape
