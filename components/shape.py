from abstracts.body_abc import Body
from components.physics import Physics
from abstracts.graphics_abc import GraphicsABC
from components.camera import Camera
from components.color import RGBA
from components.polygons import Mesh
from components.shaders import Shaders
from components.light import Light

from components.z_buffer import ZBufferSort2
from components.backface_culling import BackfaceCulling

from copy import copy


lights = []


class Shape(Body):
    def __init__(self, mesh: Mesh):
        self.physics = Physics(mesh)
        self.z_buffers_test = []

    def set_color(self, color: RGBA):
        self.color = color

    def draw(self, graphics: GraphicsABC, camera: Camera):
        global lights
        mesh = copy(self.physics.mesh)
        if mesh.light and mesh.light not in lights:
            lights.append(mesh.light)

        camera_position = camera.camera_position
        camera_target = camera.camera_target

        polygons = mesh.polygons
        backface_culling = BackfaceCulling(camera)
        polygons = backface_culling.cull_backfaces_1(polygons)
        mesh.polygons = polygons

        z_buffer_sort = ZBufferSort2(camera.camera_position)
        polygons = z_buffer_sort.get_sorted_polygons(mesh.polygons)
        mesh.polygons = polygons

        for light in lights:
            shaders = Shaders()
            shaders.apply_pbr_lighting(mesh, light, camera_position)

        # light_camera = Light.get_light_from_position(camera_position, camera_target)
        # shaders.apply_pbr_lighting(mesh, light_camera, camera_position)

        mesh = camera.apply_projection_polygons(mesh)
        if mesh:
            graphics.draw_polygons(mesh, False)
