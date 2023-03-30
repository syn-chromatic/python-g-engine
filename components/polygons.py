from components.vectors import Vector3D
from components.color import RGBA
from components.light import Light

from typing import Union, Optional


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
    def __init__(
        self, polygons: list[Union[Triangle, Quad]], light: Optional[Light] = None
    ) -> None:
        self.polygons = polygons
        self.light = light

    def get_axes(self) -> list[Vector3D]:
        axes = []
        for polygon in self.polygons:
            for i in range(len(polygon.vertices)):
                vertex1 = polygon.vertices[i]
                vertex2 = polygon.vertices[i - 1]
                edge = vertex1.subtract_vector(vertex2)
                normal = Vector3D(-edge.y, edge.x, edge.z)
                axes.append(normal.normalize())
        return axes

    def project_polygon(self, axis: Vector3D) -> tuple[float, float]:
        min_proj = max_proj = self.polygons[0].vertices[0].dot_product(axis)

        for polygon in self.polygons:
            for vertex in polygon.vertices:
                proj = vertex.dot_product(axis)
                min_proj = min(min_proj, proj)
                max_proj = max(max_proj, proj)

        return min_proj, max_proj

    def intersects(self, other: "Mesh") -> bool:
        axes1 = self.get_axes()
        axes2 = other.get_axes()

        for axis in axes1 + axes2:
            min_proj1, max_proj1 = self.project_polygon(axis)
            min_proj2, max_proj2 = other.project_polygon(axis)

            if max_proj1 < min_proj2 or max_proj2 < min_proj1:
                return False

        return True
