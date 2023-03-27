import math
from components.shared_dcs import Polygons, Triangles, Quads


class Sphere:
    def __init__(self, radius, num_latitude, num_longitude):
        self.radius = radius
        self.num_latitude = num_latitude
        self.num_longitude = num_longitude

    def get_vertices(self) -> list[tuple[float, float, float]]:
        vertices: list[tuple[float, float, float]] = []

        for i in range(self.num_latitude + 1):
            theta = i * math.pi / self.num_latitude
            sin_theta = math.sin(theta)
            cos_theta = math.cos(theta)

            for j in range(self.num_longitude + 1):
                phi = j * 2 * math.pi / self.num_longitude
                sin_phi = math.sin(phi)
                cos_phi = math.cos(phi)

                x = self.radius * sin_theta * cos_phi
                y = (self.radius * sin_theta * sin_phi) - 50
                z = self.radius * cos_theta

                vertex = (x, y, z)
                vertices.append(vertex)
        return vertices

    def get_triangle_faces(self) -> list[tuple[int, int, int]]:
        faces: list[tuple[int, int, int]] = []

        for i in range(self.num_latitude):
            for j in range(self.num_longitude):
                first = i * (self.num_longitude + 1) + j
                second = first + self.num_longitude + 1

                face1 = (first, second, first + 1)
                face2 = (second, second + 1, first + 1)

                faces.extend([face1, face2])
        return faces

    def get_quad_faces(self) -> list[tuple[int, int, int, int]]:
        faces: list[tuple[int, int, int, int]] = []

        for i in range(self.num_latitude):
            for j in range(self.num_longitude):
                first = i * (self.num_longitude + 1) + j
                second = first + self.num_longitude + 1

                # Create a quad face instead of two triangles
                face = (first, second, second + 1, first + 1)
                faces.append(face)
        return faces

    def get_triangle_polygons(self) -> list[Polygons]:
        vertices = self.get_vertices()
        faces = self.get_triangle_faces()
        triangles = Triangles(vertices, faces)
        polygons = [Polygons(triangles)]
        return polygons

    def get_quad_polygons(self):
        vertices = self.get_vertices()
        faces = self.get_quad_faces()
        quads = Quads(vertices, faces)
        polygons = [Polygons(quads)]
        return polygons


class Cube:
    def __init__(self, size: float):
        self.size = size

    def get_quad_vertices(self) -> list[tuple[float, float, float]]:
        half_size = self.size / 2
        vertices = [
            (-half_size, -half_size, -half_size),
            (half_size, -half_size, -half_size),
            (half_size, half_size, -half_size),
            (-half_size, half_size, -half_size),
            (-half_size, -half_size, half_size),
            (half_size, -half_size, half_size),
            (half_size, half_size, half_size),
            (-half_size, half_size, half_size),
        ]
        return vertices

    def get_quad_faces(self) -> list[tuple[int, int, int, int]]:
        faces = [
            (0, 1, 2, 3),
            (4, 5, 6, 7),
            (0, 1, 5, 4),
            (2, 3, 7, 6),
            (0, 4, 7, 3),
            (1, 5, 6, 2),
        ]
        return faces

    def get_polygons(self) -> list[Polygons]:
        vertices = self.get_quad_vertices()
        faces = self.get_quad_faces()
        quads = Quads(vertices, faces)
        polygons = [Polygons(quads)]
        return polygons


# class Grid:
#     def __init__(self, rows: int, cols: int, size=20):
#         self.rows = rows
#         self.cols = cols
#         self.size = size

#     def get_vertices(self) -> list[tuple[float, float, float]]:
#         vertices = []

#         for row in range(self.rows):
#             for col in range(self.cols):
#                 vertex = (row, col, 0)
#                 vertices.append(vertex)
#         return vertices

#     def get_triangle_faces(self) -> list[tuple[int, int, int]]:
#         faces = []

#         for row in range(self.rows - 1):
#             for col in range(self.cols - 1):
#                 face1 = (
#                     row * self.cols + col,
#                     row * self.cols + col + 1,
#                     (row + 1) * self.cols + col,
#                 )

#                 face2 = (
#                     row * self.cols + col + 1,
#                     (row + 1) * self.cols + col + 1,
#                     (row + 1) * self.cols + col,
#                 )

#                 faces.extend([face1, face2])
#         return faces

#     def get_triangle_polygons(self):
#         vertices = self.get_vertices()
#         faces = self.get_triangle_faces()

#         triangles = Triangles(vertices, faces)
#         polygons = [Polygons(triangles)]
#         return polygons


class GridHorizontal:
    def __init__(self, rows: int, cols: int, size: float = 20.0, y_offset: float = 0.0):
        self.rows = rows
        self.cols = cols
        self.size = size
        self.y_offset = y_offset

    def get_vertices(self) -> list[tuple[float, float, float]]:
        vertices = []

        for row in range(self.rows):
            for col in range(self.cols):
                vertex = (row * self.size, self.y_offset, col * self.size)
                vertices.append(vertex)
        return vertices

    def get_triangle_faces(self) -> list[tuple[int, int, int]]:
        faces = []

        for row in range(self.rows - 1):
            for col in range(self.cols - 1):
                face1 = (
                    row * self.cols + col,
                    row * self.cols + col + 1,
                    (row + 1) * self.cols + col,
                )

                face2 = (
                    row * self.cols + col + 1,
                    (row + 1) * self.cols + col + 1,
                    (row + 1) * self.cols + col,
                )

                faces.extend([face1, face2])
        return faces

    def get_quad_faces(self) -> list[tuple[int, int, int, int]]:
        faces = []

        for row in range(self.rows - 1):
            for col in range(self.cols - 1):
                face = (
                    row * self.cols + col,
                    row * self.cols + col + 1,
                    (row + 1) * self.cols + col + 1,
                    (row + 1) * self.cols + col,
                )
                faces.append(face)
        return faces

    def get_triangle_polygons(self):
        vertices = self.get_vertices()
        faces = self.get_triangle_faces()

        triangles = Triangles(vertices, faces)
        polygons = [Polygons(triangles)]
        return polygons

    def get_quad_polygons(self):
        vertices = self.get_vertices()
        faces = self.get_quad_faces()

        triangles = Quads(vertices, faces)
        polygons = [Polygons(triangles)]
        return polygons


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
