from components.vectors import Vector3D
from components.polygons import Triangle, Quad, Mesh
from components.camera import Camera
from typing import Union


class BackfaceCulling:
    def __init__(self):
        pass

    def cull_backfaces_1(self, mesh: Mesh, camera_position: Vector3D) -> Mesh:
        polygons = mesh.polygons
        culled_polygons = []

        for polygon in polygons:
            normal = polygon.get_normal()
            centroid = polygon.get_centroid()
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
            normal = polygon.get_normal()
            dot_product = normal.dot_product(look_direction)
            if dot_product < 0.0:
                culled_polygons.append(polygon)
            else:
                normal_dot_up = normal.dot_product(up_direction)
                if abs(normal_dot_up) > 0.95:
                    culled_polygons.append(polygon)
        mesh.polygons = culled_polygons
        return mesh
