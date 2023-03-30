from components.vectors import Vector3D
from components.color import RGBA

from typing import Union


class Triangle:
    def __init__(
        self,
        vertices: tuple[Vector3D, Vector3D, Vector3D],
        face: tuple[int, int, int],
        shader: RGBA = RGBA(0.0, 0.0, 0.0, 0.0),
        color: RGBA = RGBA(1.0, 1.0, 1.0, 1.0),
    ):
        self.vertices = vertices
        self.face = face
        self.shader = shader
        self.color = color


class Quad:
    def __init__(
        self,
        vertices: tuple[Vector3D, Vector3D, Vector3D, Vector3D],
        face: tuple[int, int, int, int],
        shader: RGBA = RGBA(0.0, 0.0, 0.0, 0.0),
        color: RGBA = RGBA(1.0, 1.0, 1.0, 1.0),
    ) -> None:
        self.vertices = vertices
        self.face = face
        self.shader = shader
        self.color = color


class Polygon:
    def __init__(self, polygon: Union[Triangle, Quad]):
        self.polygon = polygon

    def get_normal(self) -> Vector3D:
        v0 = self.polygon.vertices[0]
        v1 = self.polygon.vertices[1]
        v2 = self.polygon.vertices[2]

        edge1 = v1.subtract_vector(v0)
        edge2 = v2.subtract_vector(v0)

        normal = edge1.cross_product(edge2).normalize()
        return normal

    def get_centroid(self) -> Vector3D:
        vertices = self.polygon.vertices
        vertices_sum = Vector3D(0.0, 0.0, 0.0)
        num_vertices = len(vertices)

        for vertex in vertices:
            vertices_sum = vertices_sum.add_vector(vertex)

        centroid = vertices_sum.divide(num_vertices)
        return centroid


class Mesh:
    def __init__(self, polygons: list[Union[Triangle, Quad]]) -> None:
        self.polygons = polygons
