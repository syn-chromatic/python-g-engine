from abstracts.body_abc import Body
from components.physics import Physics
from components.color import RGBA
from components.polygons import Mesh


class Shape(Body):
    def __init__(self, mesh: Mesh):
        self.physics = Physics(mesh)
        self.z_buffers_test = []

    def set_color(self, color: RGBA):
        self.color = color
