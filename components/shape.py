from components.body import Body
from components.physics import Physics
from components.vector_3d import Vector3D
from components.graphics import Graphics
from components.camera import Camera
from components.color import RGBA
from components.utils import clamp_float


class Shape(Body):
    def __init__(self, shape: list[tuple[float, float, float]]):
        self.physics = Physics(shape)
        self.color = RGBA(1.0, 1.0, 1.0, 1.0)
        self.line_thickness = 3

    def set_color(self, color: RGBA):
        self.color = color

    def draw(self, graphics: Graphics, camera: Camera):
        shape = self.physics.shape
        shape_length = len(shape)
        shading = self._get_static_shading_sequence(shape_length)
        rgb = self.color.rgb_tuple

        for idx in range(0, shape_length):
            nxt_idx = idx + 1
            rgb = tuple((i * shading[idx] for i in rgb))
            color = RGBA.from_rgb_tuple(rgb)
            if nxt_idx < shape_length:
                p1 = shape[idx]
                p2 = shape[nxt_idx]

                self._draw_edge(p1, p2, color, graphics, camera)
                continue

            p1 = shape[idx]
            p2 = shape[0]
            self._draw_edge(p1, p2, color, graphics, camera)

    def _draw_edge(
        self,
        a: tuple[float, float, float],
        b: tuple[float, float, float],
        color: RGBA,
        graphics: Graphics,
        camera: Camera,
    ):

        position = self._get_particle_position()
        scale = self._get_particle_scale()

        projected = camera.get_perspective_projection(position)
        intr_scale = camera.interpolate_scale(projected, scale)
        intr_scale = clamp_float(intr_scale, 0.5, float("inf"))

        x1 = a[0] * intr_scale + projected.x
        y1 = a[1] * intr_scale + projected.y
        x2 = b[0] * intr_scale + projected.x
        y2 = b[1] * intr_scale + projected.y

        alpha = self._get_scale_alpha(intr_scale)
        rgb = self.color.rgb_tuple
        color = RGBA(*rgb, alpha)

        point1 = (x1, y1)
        point2 = (x2, y2)
        thickness = self.line_thickness
        graphics.draw_line(point1, point2, thickness, color)

    def _get_static_shading_sequence(self, shape_length: int):
        shading = []
        for i in range(0, shape_length**2, shape_length):
            value = i / shape_length**2
            shading.append(value)
        return shading

    def _get_scale_alpha(self, scale: float) -> float:
        max_scale = 300.0
        min_scale = max_scale / 2.0

        if scale < min_scale:
            return 1.0

        alpha_normalized = (scale - min_scale) / (max_scale - min_scale)
        alpha_clamped = clamp_float(alpha_normalized, 0.0, 1.0)
        alpha = 1.0 - alpha_clamped
        return alpha

    def get_shaded_rgb(
        self, rgb: tuple[float, float, float], shade_value: float
    ) -> tuple[float, float, float]:
        rgb = tuple(ch * shade_value for ch in rgb)
        return rgb

    def _get_particle_position(self) -> Vector3D:
        return self.physics.position

    def _get_particle_scale(self) -> float:
        return self.physics.scale
