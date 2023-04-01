from abstracts.body_abc import Body
from abstracts.graphics_abc import GraphicsABC
from components.camera import Camera
from components.polygons import Mesh

from components.z_buffer import ZBufferSort2
from components.backface_culling import BackfaceCulling

from components.shaders import Shaders
from components.light import Light
from components.debug import console_overwrite
from copy import copy


class DrawCall:
    def __init__(self, graphics: GraphicsABC, camera: Camera):
        self.objects: list[Body] = []
        self.graphics = graphics
        self.camera = camera
        self.shaders = Shaders()
        self.z_buffer_sort = ZBufferSort2()
        self.backface_culling = BackfaceCulling()
        self.meshes = []

    def add_object(self, object: Body) -> None:
        self.objects.append(object)

    def get_camera_light(self):
        camera_position = self.camera.camera_position
        camera_target = self.camera.camera_target
        light_camera = Light.get_light_from_position(camera_position, camera_target)
        return light_camera

    def get_lights(self, meshes: list[Mesh]) -> list[Light]:
        lights = []
        for mesh in meshes:
            if mesh.light:
                lights.append(mesh.light)

        # camera_light = self.get_camera_light()
        # lights.append(camera_light)
        return lights

    def get_meshes(self) -> list[Mesh]:
        meshes = []
        for body in self.objects:
            mesh = body.physics.mesh
            mesh.polygons = copy(mesh.original_polygons)
            meshes.append(mesh)
        return meshes

    def cull_backfaces_meshes(self, meshes: list[Mesh]) -> list[Mesh]:
        camera_position = self.camera.camera_position

        for idx, mesh in enumerate(meshes):
            mesh = self.backface_culling.cull_backfaces_1(mesh, camera_position)
            meshes[idx] = mesh
        return meshes

    def apply_lighting_meshes(
        self, meshes: list[Mesh], lights: list[Light]
    ) -> list[Mesh]:
        camera_position = self.camera.camera_position

        for mesh in meshes:
            for light in lights:
                self.shaders.apply_pbr_lighting(mesh, light, camera_position)

        return meshes

    def cull_backfaces_mesh(self, mesh: Mesh) -> Mesh:
        camera_position = self.camera.camera_position
        mesh = self.backface_culling.cull_backfaces_1(mesh, camera_position)
        return mesh

    def apply_lighting_mesh(self, mesh: Mesh, lights: list[Light]) -> Mesh:
        camera_position = self.camera.camera_position
        for light in lights:
            self.shaders.apply_pbr_lighting(mesh, light, camera_position)
        return mesh

    def apply_projection(self, mesh: Mesh) -> Mesh:
        mesh = self.camera.apply_projection_polygons(mesh)
        return mesh

    def apply_z_buffer_sort(self, mesh: Mesh) -> Mesh:
        camera_position = self.camera.camera_position
        mesh = self.z_buffer_sort.sort_polygons(mesh, camera_position)
        return mesh

    def combine_meshes(self, meshes: list[Mesh]) -> Mesh:
        polygons = []
        for mesh in meshes:
            if mesh.polygons:
                polygons.extend(mesh.polygons)
        mesh = Mesh(polygons)
        return mesh

    def filter_polygons(self, meshes: list[Mesh]) -> list[Mesh]:
        for idx, mesh in enumerate(meshes):
            mesh = self.camera.filter_polygons_outside_frustum(mesh)
            meshes[idx] = mesh
        return meshes

    def filter_meshes(self, meshes: list[Mesh]) -> list[Mesh]:
        filtered_meshes = []
        for mesh in meshes:
            if mesh.polygons:
                filtered_meshes.append(mesh)

        return filtered_meshes

    def draw(self):
        meshes = self.get_meshes()
        lights = self.get_lights(meshes)

        meshes = self.filter_polygons(meshes)
        meshes = self.filter_meshes(meshes)
        if not meshes:
            return

        # mesh = self.combine_meshes(meshes)
        for mesh in meshes:
            mesh = self.apply_z_buffer_sort(mesh)
            mesh = self.cull_backfaces_mesh(mesh)
            mesh = self.apply_lighting_mesh(mesh, lights)
            mesh = self.apply_projection(mesh)

            # polygon_count = len(mesh.polygons)
            # console_overwrite(f"POLYGON COUNT: {polygon_count}")

            self.graphics.draw_polygons(mesh)
