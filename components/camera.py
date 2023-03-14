import math
import numpy as np

from components.vectors import Vector3D
from components.utils import clamp_float


class CameraBase:
    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height
        self._camera_position = Vector3D(0.0, 0.0, 0.0)
        self._
        self._fov = 120
        self._near_plane = 0.1
        self._far_plane = 100.0
        self._yaw = 0.0
        self._pitch = 0.0
        self._previous_pointer = (width / 2.0, height / 2.0)


class Camera(CameraBase):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)

    def handle_mouse_movement(self, x: float, y: float) -> None:
        px = self._previous_pointer[0]
        py = self._previous_pointer[1]

        dx = x - px
        dy = y - py

        sensitivity = 0.5
        self._yaw += dx * sensitivity
        self._pitch += dy * sensitivity
        self._previous_pointer = (x, y)

    # def interpolate_scale(self, position: Vector3D, scale: float) -> float:
    #     pz = position.z
    #     near_plane = self._near_plane
    #     far_plane = self._far_plane

    #     if (pz + scale) < 0:
    #         return 0

    #     interpolation_value = (pz + near_plane) / (far_plane - near_plane)
    #     interpolated_scale = (pz + scale) * interpolation_value
    #     return interpolated_scale

    def interpolate_scale(self, position: Vector3D, scale: float) -> float:
        near_plane = self._near_plane
        far_plane = self._far_plane

        fov = self._fov
        fov_radians = math.tan(math.radians(fov))
        w = (-far_plane * near_plane) / (far_plane - near_plane)

        radius = (scale / w) * fov_radians

        # print(scale, fov_radians, w, position.get_length(), position.x, position.y, position.z)

        return radius





    def calculate_yaw_projection(self, position: Vector3D) -> Vector3D:
        yaw_radians = math.radians(self._yaw)
        yaw_cos = math.cos(yaw_radians)
        yaw_sin = math.sin(yaw_radians)

        px = position.x
        py = position.y
        pz = position.z

        yaw_x = (px * yaw_cos) - (pz * yaw_sin)
        yaw_y = py
        yaw_z = (px * yaw_sin) + (pz * yaw_cos)

        yaw_vector = Vector3D(yaw_x, yaw_y, yaw_z)
        return yaw_vector

    def calculate_pitch_projection(self, position: Vector3D) -> Vector3D:
        pitch_radians = math.radians(self._pitch)
        pitch_cos = math.cos(pitch_radians)
        pitch_sin = math.sin(pitch_radians)

        px = position.x
        py = position.y
        pz = position.z

        pitch_x = px
        pitch_y = (py * pitch_cos) - (pz * pitch_sin)
        pitch_z = (py * pitch_sin) + (pz * pitch_cos)

        pitch_vector = Vector3D(pitch_x, pitch_y, pitch_z)
        return pitch_vector

    # def calculate_homogeneous_projection(self, position: Vector3D):
    #     near_plane = self._near_plane
    #     far_plane = self._far_plane

    #     x = position.x
    #     y = position.y

    #     z = far_plane + near_plane
    #     w = near_plane - far_plane

    #     xprj = x * near_plane / w
    #     yprj = y * near_plane / w
    #     zprj = z / w

    #     projected_vector = Vector3D(xprj, yprj, zprj)
    #     return projected_vector

    def calculate_perspective_projection(self, position: Vector3D):
        width = self._width
        height = self._height
        fov = self._fov
        near_plane = self._near_plane
        far_plane = self._far_plane

        xi = position.x
        yi = position.y
        zi = position.z

        aspect_ratio = height / width
        fov_radians = math.tan(math.radians(fov))

        xo = xi * aspect_ratio * fov_radians
        yo = yi * fov_radians
        zo = zi * (far_plane / (far_plane - near_plane)) + 1
        w = (-far_plane * near_plane) / (far_plane - near_plane)

        if w != 0.0:
            xo /= w
            yo /= w
            zo /= w

        vo = Vector3D(xo, yo, zo)
        # test = vo.subtract_vector(position).get_length()
        # print(test * vo.get_length())
        return vo

    # def calculate_perspective_projection(self, position: Vector3D):
    #     near_plane = self._near_plane
    #     far_plane = self._far_plane

    #     px = position.x
    #     py = position.y
    #     pz = position.z

    #     x = (px * near_plane) / pz
    #     y = (py * near_plane) / pz

    #     z = (far_plane + near_plane) / (near_plane - far_plane)
    #     w = -pz / (far_plane - near_plane)

    #     xprj = x * w
    #     yprj = y * w
    #     zprj = z * w

    #     projected_vector = Vector3D(xprj, yprj, zprj)
    #     return projected_vector

    def calculate_projection(self, position: Vector3D):
        # if position.z == 0.0:
        #     return self.calculate_homogeneous_projection(position)
        return self.calculate_perspective_projection(position)

    def get_perspective_projection(self, position: Vector3D):
        position = self.calculate_projection(position)
        # position = self.calculate_yaw_projection(position)
        # position = self.calculate_pitch_projection(position)
        # position = self.calculate_projection(position)

        return position

    def increment_distance(self, increment: float):
        near_plane = self._near_plane
        far_plane = self._far_plane

        if (near_plane + increment) >= 0.0:
            near_plane += increment
            far_plane += increment
            self._near_plane = clamp_float(near_plane, 0.0, float("inf"))
            self._far_plane = clamp_float(far_plane, 0.0, float("inf"))
