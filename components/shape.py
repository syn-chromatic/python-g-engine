from components.body import Body
from components.physics import Physics
from components.graphics_abc import GraphicsABC
from components.camera import Camera
from components.color import RGBA
from components.shared_dcs import Polygons
from components.shaders import Shaders, Light


class Shape(Body):
    def __init__(self, polygons: list[Polygons]):
        self.physics = Physics(polygons)
        self.color = RGBA(1.0, 1.0, 1.0, 1.0)
        self.light = Light.get_light()
        self.line_thickness = 3

    def set_color(self, color: RGBA):
        self.color = color

    def draw(self, graphics: GraphicsABC, camera: Camera):
        polygons = self.physics.polygons
        polygons = camera.apply_projection_polygons(polygons)
        if polygons:
            Shaders(polygons).apply_lighting(self.light, camera.camera_position)
            graphics.draw_polygons(polygons)
