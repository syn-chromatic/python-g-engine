from abstracts.body_abc import Body
from components.physics import Physics
from abstracts.graphics_abc import GraphicsABC
from components.camera import Camera
from components.color import RGBA
from components.polygons import Mesh
from components.shaders import Shaders, Light

from components.z_buffer import ZBufferSort2
from components.backface_culling import BackfaceCulling

from copy import copy


class Shape(Body):
    def __init__(self, mesh: Mesh):
        self.physics = Physics(mesh)
        self.light = Light.get_light()
        self.z_buffers_test = []

    def set_color(self, color: RGBA):
        self.color = color

    def draw(self, graphics: GraphicsABC, camera: Camera):
        mesh = copy(self.physics.mesh)

        camera_position = camera.camera_position
        camera_target = camera.camera_target

        polygons = mesh.polygons
        backface_culling = BackfaceCulling()
        polygons = backface_culling.cull_backfaces(camera_position, polygons)
        mesh.polygons = polygons

        z_buffer_sort = ZBufferSort2(camera.camera_position)
        polygons = z_buffer_sort.get_sorted_polygons(mesh.polygons)
        mesh.polygons = polygons

        shaders = Shaders()
        shaders.apply_pbr_lighting(mesh, self.light, camera_position)

        # light_camera = Light.get_light_from_position(camera_position, camera_target)
        # shaders.apply_pbr_lighting(mesh, light_camera, camera_position)

        mesh = camera.apply_projection_polygons(mesh)
        if mesh:
            graphics.draw_polygons(mesh, False)
