from abstracts.body_abc import Body
from components.physics import Physics
from abstracts.graphics_abc import GraphicsABC
from components.camera import Camera
from components.color import RGBA
from components.polygons import Mesh
from components.shaders import Shaders, Light

from components.polygons import Triangle, Quad
from components.vectors import Vector3D
from typing import Union


class ZBufferSort:
    def __init__(self, camera_position: Vector3D):
        self.camera_position = camera_position

    def get_centroid(self, polygon: Union[Triangle, Quad]):
        vertices_sum = Vector3D(0, 0, 0)
        num_vertices = len(polygon.vertices)

        for vertex in polygon.vertices:
            vertices_sum = vertices_sum.add_vector(vertex)

        return vertices_sum.divide(num_vertices)

    def get_sorted_polygons(
        self, polygons: list[Union[Triangle, Quad]]
    ) -> list[Union[Triangle, Quad]]:
        camera_position = self.camera_position
        return sorted(
            polygons,
            key=lambda p: camera_position.get_distance(self.get_centroid(p)),
            reverse=True,
        )


class Shape(Body):
    def __init__(self, mesh: Mesh):
        self.physics = Physics(mesh)
        self.light = Light.get_light()
        self.z_buffers_test = []

    def set_color(self, color: RGBA):
        self.color = color

    def draw(self, graphics: GraphicsABC, camera: Camera):
        mesh = self.physics.mesh
        camera_position = camera.camera_position
        camera_target = camera.camera_target

        Shaders.apply_pbr_lighting(mesh, self.light, camera_position)

        light_camera = Light.get_light_from_position(camera_position, camera_target)
        Shaders.apply_pbr_lighting(mesh, light_camera, camera_position)

        z_buffer_sort = ZBufferSort(camera.camera_position)
        sorted_polygons = z_buffer_sort.get_sorted_polygons(mesh.polygons)

        mesh.polygons = sorted_polygons
        mesh = camera.apply_projection_polygons(mesh)

        if mesh:
            graphics.draw_polygons(mesh, False)
