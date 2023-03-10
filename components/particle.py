from components.body import Body
from components.physics import Physics
from components.graphics import Graphics
from components.camera import Camera


class Particle(Body):
    def __init__(self, shape: list[tuple[float, float, float]]):
        self.physics = Physics(shape)
        self.color = (1.0, 1.0, 1.0)

    def get_scale_alpha(self):
        pass

    def get_rgb_values(self):
        pass

    def get_particle_position(self):
        return self.physics.position

    def get_particle_scale(self):
        return self.physics.scale

    def _draw_circle(self, graphics: Graphics, camera: Camera):
        position = self.get_particle_position()
        scale = self.get_particle_scale()

        projected = camera.get_perspective_projection(position)
        radius = camera.interpolate_radius(projected, scale)

        # rgb = self.get_rgb_values()
        # alpha = self.get_scale_alpha()

        p = projected.x, projected.y
        graphics.draw_circle(p, radius, self.color)

    def set_color(self, color: tuple[float, float, float]):
        self.color = color

    def draw(self, graphics: Graphics, camera: Camera):
        self._draw_circle(graphics, camera)
