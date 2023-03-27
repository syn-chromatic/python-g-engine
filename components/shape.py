from abstracts.body_abc import Body
from components.physics import Physics
from abstracts.graphics_abc import GraphicsABC
from components.camera import Camera
from components.color import RGBA
from components.polygons import Mesh
from components.shaders import Shaders, Light


class Shape(Body):
    def __init__(self, mesh: Mesh):
        self.physics = Physics(mesh)
        self.color = RGBA(1.0, 1.0, 1.0, 1.0)
        self.light = Light.get_light()
        self.line_thickness = 3

    def set_color(self, color: RGBA):
        self.color = color

    def draw(self, graphics: GraphicsABC, camera: Camera):
        mesh = self.physics.mesh
        mesh = camera.apply_projection_polygons(mesh)
        if mesh:
            Shaders(mesh).apply_lighting(self.light, camera.camera_position)
            graphics.draw_polygons(mesh)
