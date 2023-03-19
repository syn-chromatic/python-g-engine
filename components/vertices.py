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
        for i in range_long:
            for j in range_lat:
                theta = 2.0 * math.pi * i / self.long_num
                phi = math.pi * j / (self.lat_num - 1)
                x = 1.0 * math.sin(phi) * math.cos(theta)
                y = 1.0 * math.sin(phi) * math.sin(theta)
                z = 1.0 * math.cos(phi)
                self.shape.append((x, y, z))

    def create_lat_points(self) -> None:
        for i in range(self.points):
            theta = math.pi * i / (self.points)
            for j in range(self.points + 1):
                phi = 2.0 * math.pi * j / (self.points)
                x = 1.0 * math.sin(theta) * math.cos(phi)
                y = 1.0 * math.sin(theta) * math.sin(phi)
                z = 1.0 * math.cos(theta)
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
            (-1.0, -1.0, -1.0),
            (1.0, -1.0, -1.0),
            (-1.0, -1.0, -1.0),
            (-1.0, -1.0, 1.0),
            (-1.0, -1.0, 1.0),
            (1.0, -1.0, 1.0),
            (1.0, -1.0, -1.0),
            (1.0, 1.0, -1.0),
            (1.0, -1.0, -1.0),
            (1.0, -1.0, 1.0),
            (1.0, -1.0, 1.0),
            (1.0, 1.0, 1.0),
            (1.0, 1.0, -1.0),
            (-1.0, 1.0, -1.0),
            (1.0, 1.0, -1.0),
            (1.0, 1.0, 1.0),
            (1.0, 1.0, 1.0),
            (-1.0, 1.0, 1.0),
            (-1.0, 1.0, -1.0),
            (-1.0, -1.0, -1.0),
            (-1.0, 1.0, -1.0),
            (-1.0, 1.0, 1.0),
            (-1.0, 1.0, 1.0),
            (-1.0, -1.0, 1.0),
        ]
        return shape


class ParticleCircle:
    def __init__(self, circle_radius: int):
        self.circle_radius = circle_radius

    def generate(self, px: float, py: float) -> list[list[float]]:
        "Returns a list of particles in the form of list[list[x, y, size]]."
        particles = []
        max_particle_size = 0.0

        circle_radius = self.circle_radius
        while circle_radius > 1:
            size = 1.0
            angle_increment = 2.0 * math.pi / circle_radius

            for i in range(circle_radius):
                angle = i * angle_increment
                x = px + circle_radius * math.cos(angle)
                y = py + circle_radius * math.sin(angle)

                if size > max_particle_size:
                    max_particle_size = size

                particle = [x, y, size]
                particles.append(particle)
            circle_radius -= int(max_particle_size * math.pi)
            max_particle_size = 0.0
        return particles
