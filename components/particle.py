from components.body import Body
from components.physics import Physics
from components.vectors import Vector3D
from components.graphics import Graphics
from components.camera import Camera
from components.color import RGBA
from components.utils import clamp_float


class Particle(Body):
    def __init__(self, shape: list[tuple[float, float, float]]) -> None:
        self.physics = Physics(shape)
        self.color = RGBA(1.0, 1.0, 1.0, 1.0)

    def set_color(self, color: RGBA) -> None:
        self.color = color

    def draw(self, graphics: Graphics, camera: Camera) -> None:
        self._draw_circle(graphics, camera)

    def _draw_circle(self, graphics: Graphics, camera: Camera) -> None:
        position = self._get_particle_position()
        scale = self._get_particle_scale()

        projected = camera.get_perspective_projection(position)
        intr_scale = camera.interpolate_scale(projected, scale)

        # intr_scale = scale
        # intr_scale = clamp_float(intr_scale, 0.5, float("inf"))

        alpha = self._get_scale_alpha(intr_scale)
        rgb = self.color.rgb_tuple
        color = RGBA(*rgb, alpha)

        point = projected.x, projected.y
        graphics.draw_circle(point, intr_scale, color)

    def _get_scale_alpha(self, scale: float) -> float:
        max_scale = 300.0
        min_scale = max_scale / 2.0

        if scale < min_scale:
            return 1.0

        alpha_normalized = (scale - min_scale) / (max_scale - min_scale)
        alpha_clamped = clamp_float(alpha_normalized, 0.0, 1.0)
        alpha = 1.0 - alpha_clamped
        return alpha

    def _get_particle_position(self) -> Vector3D:
        return self.physics.position

    def _get_particle_scale(self) -> float:
        return self.physics.scale
