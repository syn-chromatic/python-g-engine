from components.body import Body
from components.physics import Physics
from components.graphics import Graphics


class Shape(Body):
    def __init__(self, shape: list[tuple[float, float, float]]):
        self.physics = Physics(shape)
        self.color = (1.0, 1.0, 1.0)
        self.line_thickness = 3

    @staticmethod
    def _perspective_projection(
        xyz_point: tuple[float, float, float]
    ) -> tuple[float, float, float]:
        distance = 5
        zp = 1 / (distance - xyz_point[2])
        xp = xyz_point[0] * zp
        yp = xyz_point[1] * zp
        return (xp, yp, zp)

    def _draw_edge(
        self,
        a: tuple[float, float, float],
        b: tuple[float, float, float],
        color: tuple[float, float, float],
        graphics: Graphics,

    ):
        scale = self.physics.scale
        z = self.physics.position.z
        relative_z = scale + z
        relative_z = min(float("inf"), max(0, relative_z))

        x1 = a[0] * relative_z + self.physics.position.x
        y1 = a[1] * relative_z + self.physics.position.y
        x2 = b[0] * relative_z + self.physics.position.x
        y2 = b[1] * relative_z + self.physics.position.y

        graphics.draw_line((x1, y1), (x2, y2), self.line_thickness, color)

    def _draw_edge_perspective(
        self,
        a: tuple[float, float, float],
        b: tuple[float, float, float],
        color: tuple[float, float, float],
        graphics: Graphics,
    ):
        a = self._perspective_projection(a)
        b = self._perspective_projection(b)
        self._draw_edge(a, b, color, graphics)

    def _get_static_shading_sequence(self, shape_length: int):
        shading = []
        for i in range(0, shape_length**2, shape_length):
            value = i / shape_length**2
            shading.append(value)
        return shading

    def set_color(self, color: tuple[float, float, float]):
        self.color = color

    def draw_shape(self, graphics: Graphics):
        shape = self.physics.shape
        shape_length = len(shape)
        shading = self._get_static_shading_sequence(shape_length)

        for idx in range(0, shape_length):
            nxt_idx = idx + 1
            color = tuple((i * shading[idx] for i in self.color))
            if nxt_idx < shape_length:
                p1 = shape[idx]
                p2 = shape[nxt_idx]

                self._draw_edge(p1, p2, color, graphics)
                continue

            p1 = shape[idx]
            p2 = shape[0]
            self._draw_edge(p1, p2, color, graphics)
