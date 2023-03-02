from components.body import Body
from components.physics import Physics
from components.graphics import Graphics


class Particle(Body):
    def __init__(self, shape: list[tuple[float, float, float]]):
        self.physics = Physics(shape)
        self.color = (1.0, 1.0, 1.0)

    def _draw_circle(
        self,
        graphics: Graphics,
    ):

        x = self.physics.position.x
        y = self.physics.position.y
        z = self.physics.position.z
        scale = self.physics.scale
        relative_z = scale + z

        # relative_z = min(float("inf"), max(0.5, relative_z))
        graphics.draw_circle((x, y), self.physics.scale, self.color)
        # graphics.draw_text((x, y), (1, 1, 1), f"VX: {self.physics.velocity.x}\nVY: {self.physics.velocity.y}")

    def set_color(self, color: tuple[float, float, float]):
        self.color = color

    def draw_shape(self, graphics: Graphics):
        self._draw_circle(graphics)
