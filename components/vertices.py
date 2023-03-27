import math
from components.polygons import Mesh, Triangle, Quad
from components.vectors import Vector3D


class Sphere:
    def __init__(self, radius: float, num_latitude: int, num_longitude: int):
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

    def get_triangle_polygons(self) -> Mesh:
        vertices = self.get_vertices()
        faces = self.get_triangle_faces()
        triangle_polygons = []
        for face in faces:
            triangle = Triangle(
                (vertices[face[0]], vertices[face[1]], vertices[face[2]]),
                face,
                (1.0, 1.0, 1.0),
            )
            triangle_polygons.append(triangle)
        return Mesh(triangle_polygons)

    def get_quad_polygons(self) -> Mesh:
        vertices = self.get_vertices()
        faces = self.get_quad_faces()
        quad_polygons = []
        for face in faces:
            quad = Quad(
                (
                    vertices[face[0]],
                    vertices[face[1]],
                    vertices[face[2]],
                    vertices[face[3]],
                ),
                face,
                (1.0, 1.0, 1.0),
            )
            quad_polygons.append(quad)
        return Mesh(quad_polygons)


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

    def get_polygons(self) -> Mesh:
        vertices = self.get_quad_vertices()
        faces = self.get_quad_faces()
        quad_polygons = []
        for face in faces:
            quad = Quad(
                (
                    vertices[face[0]],
                    vertices[face[1]],
                    vertices[face[2]],
                    vertices[face[3]],
                ),
                face,
                (1.0, 1.0, 1.0),
            )
            quad_polygons.append(quad)
        return Mesh(quad_polygons)


class MeshConverter:
    def __init__(self, mesh: Mesh):
        self.mesh = mesh

    def quads_to_triangles(self) -> Mesh:
        polygons = self.mesh.polygons
        new_polygons = []

        for poly in polygons:
            if isinstance(poly, Quad):
                vertices = poly.vertices
                face = poly.face
                shader = poly.shader
                color = poly.color

                triangle1 = Triangle(
                    (vertices[0], vertices[1], vertices[2]),
                    (face[0], face[1], face[2]),
                    shader,
                )
                triangle1.color = color

                triangle2 = Triangle(
                    (vertices[0], vertices[2], vertices[3]),
                    (face[0], face[2], face[3]),
                    shader,
                )
                triangle2.color = color

                new_polygons.extend([triangle1, triangle2])
            else:
                new_polygons.append(poly)

        return Mesh(new_polygons)


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

    def get_triangle_polygons(self) -> Mesh:
        vertices = self.get_vertices()
        faces = self.get_triangle_faces()
        triangle_polygons = []
        for face in faces:
            triangle = Triangle(
                (vertices[face[0]], vertices[face[1]], vertices[face[2]]),
                face,
                (1.0, 1.0, 1.0),
            )
            triangle_polygons.append(triangle)
        return Mesh(triangle_polygons)

    def get_quad_polygons(self) -> Mesh:
        vertices = self.get_vertices()
        faces = self.get_quad_faces()
        quad_polygons = []
        for face in faces:
            quad = Quad(
                (
                    vertices[face[0]],
                    vertices[face[1]],
                    vertices[face[2]],
                    vertices[face[3]],
                ),
                face,
                (1.0, 1.0, 1.0),
            )
            quad_polygons.append(quad)
        return Mesh(quad_polygons)


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
