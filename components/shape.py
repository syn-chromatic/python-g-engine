from components.body import Body
from components.physics import Physics
from components.vectors import Vector3D
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
        position = self._get_shape_position()
        scale = self._get_shape_scale()

        point_a = (
            (a[0] * scale) + position.x,
            (a[1] * scale) + position.y,
            (a[2] * scale) + position.z,
        )
        point_b = (
            (b[0] * scale) + position.x,
            (b[1] * scale) + position.y,
            (b[2] * scale) + position.z,
        )
        point_av = Vector3D(*point_a)
        point_bv = Vector3D(*point_b)

        point_av = camera.get_screen_coordinates(point_av)
        point_bv = camera.get_screen_coordinates(point_bv)

        if point_av is None or point_bv is None:
            return

        p_scale = point_av.subtract_vector(point_bv).get_length() / 2.0
        alpha = self._get_scale_alpha(p_scale)
        rgb = self.color.rgb_tuple
        color = RGBA(*rgb, alpha)

        point_a_2d = (point_av.x, point_av.y)
        point_b_2d = (point_bv.x, point_bv.y)

        graphics.draw_line(point_a_2d, point_b_2d, self.line_thickness, color)

    def _get_static_shading_sequence(self, shape_length: int):
        shading = []
        for i in range(0, shape_length**2, shape_length):
            value = i / shape_length**2
            shading.append(value)
        return shading

    def _get_scale_alpha(self, scale: float) -> float:
        max_scale = 500.0
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

    def _get_shape_position(self) -> Vector3D:
        return self.physics.position

    def _get_shape_scale(self) -> float:
        return self.physics.scale
