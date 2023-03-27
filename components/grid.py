from components.body import Body
from components.vectors import Vector3D
from components.graphics_abc import GraphicsABC
from components.physics import Physics
from components.camera import Camera
from components.color import RGBA

from typing import Optional


class GridGround(Body):
    def __init__(self, rows: int, columns: int, cell_size: float, y_pos: float) -> None:
        self.rows = rows
        self.columns = columns
        self.cell_size = cell_size
        self.y_pos = y_pos
        self.physics = Physics([(1.0, 1.0, 1.0)])
        self.color = RGBA(1.0, 1.0, 1.0, 1.0)
        self.points: list[tuple[Vector3D, Vector3D]] = self.create_points()

    def set_color(self, color: RGBA) -> None:
        self.color = color

    def create_points(self) -> list[tuple[Vector3D, Vector3D]]:
        points = []
        for row in range(self.rows + 1):
            for column in range(self.columns):
                point1 = self._get_cell_position(row, column)
                point2 = self._get_cell_position(row, column + 1)
                grid_line = (point1, point2)
                points.append(grid_line)

        for column in range(self.columns + 1):
            for row in range(self.rows):
                point1 = self._get_cell_position(row, column)
                point2 = self._get_cell_position(row + 1, column)
                grid_line = (point1, point2)
                points.append(grid_line)

        return points

    def draw(self, graphics: GraphicsABC, camera: Camera) -> None:
        previous_line: list[tuple[float, float]] = []

        for point1, point2 in self.points:
            grid_line = self._get_projected_grid_line(camera, point1, point2)
            if grid_line:
                if not previous_line:
                    previous_line = grid_line
                    continue

                if previous_line[1] == grid_line[0]:
                    previous_line[1] = grid_line[1]
                else:
                    xy1, xy2 = previous_line
                    graphics.draw_line(xy1, xy2, 1, self.color)
                    previous_line = grid_line

        if previous_line:
            xy1, xy2 = previous_line
            graphics.draw_line(xy1, xy2, 1, self.color)

    def _get_projected_grid_line(
        self, camera: Camera, point1: Vector3D, point2: Vector3D
    ) -> Optional[list[tuple[float, float]]]:
        proj1 = camera.get_screen_coordinates(point1)
        proj2 = camera.get_screen_coordinates(point2)
        if proj1 and proj2:
            xy1 = proj1.x, proj1.y
            xy2 = proj2.x, proj2.y
            grid_line = [xy1, xy2]
            return grid_line

    def _get_cell_position(self, row: int, column: int) -> Vector3D:
        x = column * self.cell_size
        z = row * self.cell_size
        return Vector3D(x, self.y_pos, z)
