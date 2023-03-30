from components.vectors import Vector3D
from components.polygons import Triangle, Quad

from typing import Union


class BackfaceCulling:
    def get_normal(self, polygon: Union[Triangle, Quad]) -> Vector3D:
        v0, v1, v2 = polygon.vertices[:3]

        edge1 = v1.subtract_vector(v0)
        edge2 = v2.subtract_vector(v0)

        return edge1.cross_product(edge2).normalize()

    def get_centroid(self, polygon) -> Vector3D:

        vertices = polygon.vertices

        num_vertices = len(vertices)
        vertices_sum = Vector3D(0.0, 0.0, 0.0)

        for vertex in vertices:
            vertices_sum = vertices_sum.add_vector(vertex)

        return vertices_sum.divide(num_vertices)

    def cull_backfaces(
        self, camera_position: Vector3D, polygons: list[Union[Triangle, Quad]]
    ):
        culled_polygons = []

        for polygon in polygons:
            normal = self.get_normal(polygon)
            centroid = self.get_centroid(polygon)
            view_vector = centroid.subtract_vector(camera_position)

            dot_product = normal.dot_product(view_vector)

            if dot_product < 0.0:
                culled_polygons.append(polygon)

        return culled_polygons
