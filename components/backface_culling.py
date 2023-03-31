from components.vectors import Vector3D
from components.polygons import Triangle, Quad, Mesh
from components.camera import Camera
from typing import Union


class BackfaceCulling:
    def __init__(self):
        pass

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

    def cull_backfaces_1(self, mesh: Mesh, camera_position: Vector3D) -> Mesh:
        polygons = mesh.polygons
        culled_polygons = []

        for polygon in polygons:
            normal = self.get_normal(polygon)
            centroid = self.get_centroid(polygon)
            view_vector = centroid.subtract_vector(camera_position)

            dot_product = normal.dot_product(view_vector)
            if dot_product < 0.0:
                culled_polygons.append(polygon)

        mesh.polygons = culled_polygons
        return mesh

    def cull_backfaces_2(
        self,
        mesh: Mesh,
        look_direction: Vector3D,
        up_direction: Vector3D,
    ) -> Mesh:
        polygons = mesh.polygons
        culled_polygons = []

        for polygon in polygons:
            normal = self.get_normal(polygon)
            dot_product = normal.dot_product(look_direction)
            if dot_product < 0.0:
                culled_polygons.append(polygon)
            else:
                normal_dot_up = normal.dot_product(up_direction)
                if abs(normal_dot_up) > 0.95:
                    culled_polygons.append(polygon)
        mesh.polygons = culled_polygons
        return mesh
