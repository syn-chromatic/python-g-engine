import math
from components.shared_dcs import Polygons, Triangles, Quads
from components.vectors import Vector3D


class Sphere:
    def __init__(self, radius, num_latitude, num_longitude):
        self.radius = radius
        self.num_latitude = num_latitude
        self.num_longitude = num_longitude
        self.x_offset = 0.0
        self.y_offset = 0.0
        self.z_offset = 0.0

    def set_offset(self, x: float, y: float, z: float):
        self.x_offset = x
        self.y_offset = y
        self.z_offset = z

    def get_vertices(self) -> list[Vector3D]:
        vertices: list[Vector3D] = []

        for i in range(self.num_latitude + 1):
            theta = i * math.pi / self.num_latitude
            sin_theta = math.sin(theta)
            cos_theta = math.cos(theta)

            for j in range(self.num_longitude + 1):
                phi = j * 2 * math.pi / self.num_longitude
                sin_phi = math.sin(phi)
                cos_phi = math.cos(phi)

                x = (self.radius * sin_theta * cos_phi) + self.x_offset
                y = (self.radius * sin_theta * sin_phi) + self.y_offset
                z = (self.radius * cos_theta) + self.z_offset

                vertex = Vector3D(x, y, z)
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
        triangles = Triangles(vertices, faces, [])
        polygons = [Polygons(triangles)]
        return polygons

    def get_quad_polygons(self):
        vertices = self.get_vertices()
        faces = self.get_quad_faces()
        quads = Quads(vertices, faces, [])
        polygons = [Polygons(quads)]
        return polygons


class Cube:
    def __init__(self, size: float):
        self.size = size

    def get_quad_vertices(self) -> list[Vector3D]:
        half_size = self.size / 2
        vertices = [
            Vector3D(-half_size, -half_size, -half_size),
            Vector3D(half_size, -half_size, -half_size),
            Vector3D(half_size, half_size, -half_size),
            Vector3D(-half_size, half_size, -half_size),
            Vector3D(-half_size, -half_size, half_size),
            Vector3D(half_size, -half_size, half_size),
            Vector3D(half_size, half_size, half_size),
            Vector3D(-half_size, half_size, half_size),
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
        quads = Quads(vertices, faces, [])
        polygons = [Polygons(quads)]
        return polygons


class MeshConverter:
    def __init__(self, polygons: list[Polygons]):
        self.polygons = polygons

    def quads_to_triangles(self) -> list[Polygons]:
        polygons = self.polygons

        for idx, polys in enumerate(polygons):
            polys_type = polys.type

            if isinstance(polys_type, Quads):
                triangle_faces: list[tuple[int, int, int]] = []
                quad_faces = polys_type.faces
                for quad in quad_faces:
                    triangle1 = (quad[0], quad[1], quad[2])
                    triangle2 = (quad[0], quad[2], quad[3])

                    triangle_faces.extend([triangle1, triangle2])
                triangles = Triangles(polys_type.vertices, triangle_faces, [])
                polygons[idx].type = triangles

        return polygons


class GridHorizontal:
    def __init__(self, rows: int, cols: int, size: float = 20.0):
        self.rows = rows
        self.cols = cols
        self.size = size
        self.x_offset = 0.0
        self.y_offset = 0.0
        self.z_offset = 0.0

    def set_offset(self, x: float, y: float, z: float):
        self.x_offset = x
        self.y_offset = y
        self.z_offset = z

    def get_vertices(self) -> list[Vector3D]:
        vertices = []

        for row in range(self.rows):
            for col in range(self.cols):
                xv = (row * self.size) + self.x_offset
                yv = self.y_offset
                zv = (col * self.size) + self.z_offset
                vertex = Vector3D(xv, yv, zv)
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

        triangles = Triangles(vertices, faces, [])
        polygons = [Polygons(triangles)]
        return polygons

    def get_quad_polygons(self):
        vertices = self.get_vertices()
        faces = self.get_quad_faces()

        triangles = Quads(vertices, faces, [])
        polygons = [Polygons(triangles)]
        return polygons


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
