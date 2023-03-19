from components.body import Body
from components.vectors import Vector3D
from components.graphics import Graphics
from components.physics import Physics
from components.camera import Camera
from components.color import RGBA


class GridGround(Body):
    def __init__(self, rows: int, columns: int, cell_size: float) -> None:
        self.rows = rows
        self.columns = columns
        self.cell_size = cell_size
        self.physics = Physics([(1.0, 1.0, 1.0)])
        self.color = RGBA(1.0, 1.0, 1.0, 1.0)

    def set_color(self, color: RGBA) -> None:
        self.color = color

    def draw(self, graphics: Graphics, camera: Camera) -> None:
        for row in range(self.rows + 1):
            for column in range(self.columns + 1):
                self._draw_grid_line(graphics, camera, row, column)

    def _draw_grid_line(
        self, graphics: Graphics, camera: Camera, row: int, column: int
    ) -> None:
        position1 = self._get_cell_position(row, column)
        position2 = (
            self._get_cell_position(row + 1, column) if row < self.rows else None
        )
        position3 = (
            self._get_cell_position(row, column + 1) if column < self.columns else None
        )

        if position2:
            proj1 = camera.get_screen_coordinates(position1)
            proj2 = camera.get_screen_coordinates(position2)
            if proj1 and proj2:
                xy1 = proj1.x, proj1.y
                xy2 = proj2.x, proj2.y
                graphics.draw_line(xy1, xy2, 1, self.color)

        if position3:
            proj1 = camera.get_screen_coordinates(position1)
            proj3 = camera.get_screen_coordinates(position3)
            if proj1 and proj3:
                xy1 = proj1.x, proj1.y
                xy3 = proj3.x, proj3.y

                graphics.draw_line(xy1, xy3, 1, self.color)

    def _get_cell_position(self, row: int, column: int) -> Vector3D:
        x = column * self.cell_size
        z = row * self.cell_size
        return Vector3D(x, 0, z)
