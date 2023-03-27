from components.polygons import Mesh, Triangle, Quad
from components.vertices import MeshConverter
from components.vectors import Vector3D
from pathlib import Path


class OBJModelFormat:
    def __init__(self, file_path: Path, scale: float = 1.0):
        self.file_path = file_path
        self.scale = scale
        self.x_offset = 0.0
        self.y_offset = 0.0
        self.z_offset = 0.0

    def set_offset(self, x: float, y: float, z: float):
        self.x_offset = x
        self.y_offset = y
        self.z_offset = z

    def get_model_triangles(self) -> Mesh:
        vertices, faces = [], []
        with open(self.file_path) as f:
            for line in f:
                tokens = line.split()
                if not tokens:
                    continue

                if tokens[0] == "v":
                    vertex_tuple = tuple(float(i) for i in tokens[1:4])
                    vertex = Vector3D(*vertex_tuple)
                    vertex = vertex.multiply(self.scale)

                    xv = vertex.x + self.x_offset
                    yv = vertex.y + self.y_offset
                    zv = vertex.z + self.z_offset
                    vertex = Vector3D(xv, yv, zv)

                    vertices.append(vertex)

                elif tokens[0] == "f":
                    face_indices = [int(tok.split("/")[0]) - 1 for tok in tokens[1:]]
                    if len(face_indices) == 3:
                        faces.append(tuple(face_indices))

        triangle_polygons = []
        for face in faces:
            triangle = Triangle(
                (vertices[face[0]], vertices[face[1]], vertices[face[2]]),
                face,
                (1.0, 1.0, 1.0),
            )
            triangle_polygons.append(triangle)
        return Mesh(triangle_polygons)

    def get_model_quads(self) -> Mesh:
        vertices, faces = [], []
        with open(self.file_path) as f:
            for line in f:
                tokens = line.split()
                if not tokens:
                    continue

                if tokens[0] == "v":
                    vertex_tuple = tuple(float(i) for i in tokens[1:4])
                    vertex = Vector3D(*vertex_tuple)
                    vertex = vertex.multiply(self.scale)

                    xv = vertex.x + self.x_offset
                    yv = vertex.y + self.y_offset
                    zv = vertex.z + self.z_offset
                    vertex = Vector3D(xv, yv, zv)
                    vertices.append(vertex)
                elif tokens[0] == "f":
                    face_indices = [int(tok.split("/")[0]) - 1 for tok in tokens[1:]]
                    if len(face_indices) == 4:
                        faces.append(tuple(face_indices))

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

    def get_polygons(self) -> Mesh:
        mesh1 = self.get_model_triangles()
        mesh2 = self.get_model_quads()
        mesh2 = MeshConverter(mesh2).quads_to_triangles()

        mesh = Mesh([*mesh1.polygons, *mesh2.polygons])
        return mesh
