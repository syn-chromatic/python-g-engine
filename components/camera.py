import math
import numpy as np

from components.vectors import Vector3D
from components.utils import clamp_float


class CameraBase:
    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height
        self._fov = 120
        self._near_plane = 0.9
        self._far_plane = 100.0
        self._yaw = 0.0
        self._pitch = 0.0
        self._position = Vector3D(0.0, 0.0, 0.0)
        self._look_direction = Vector3D(0.0, 0.0, -1.0)
        self._up = Vector3D(0.0, 1.0, 0.0)
        self._right = Vector3D(1.0, 0.0, 0.0)
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
        self.update_vectors()

    def update_vectors(self):
        yaw_radians = math.radians(self._yaw)
        pitch_radians = math.radians(self._pitch)

        front = Vector3D(
            math.cos(pitch_radians) * math.cos(yaw_radians),
            math.sin(pitch_radians),
            math.cos(pitch_radians) * math.sin(yaw_radians),
        )

        self._look_direction = front.normalize()
        self._right = self._look_direction.cross_product(self._up).normalize()
        self._up = self._right.cross_product(self._look_direction).normalize()

    def interpolate_scale(self, position: Vector3D, scale: float) -> float:

        transformed_position = self.apply_view_transform(position)
        distance_to_camera = transformed_position.z

        # If the object is behind the camera, return 0 size
        if distance_to_camera < self._near_plane:
            return 0.0

        return scale + distance_to_camera

    def apply_view_transform(self, position: Vector3D) -> Vector3D:
        transformed_position = position.subtract_vector(self._position)
        transformed_position = Vector3D(
            transformed_position.dot_product(self._right),
            transformed_position.dot_product(self._up),
            transformed_position.dot_product(self._look_direction),
        )
        return transformed_position

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
        return vo

    def get_perspective_projection(self, position: Vector3D):
        position = self.apply_view_transform(position)
        position = self.calculate_perspective_projection(position)
        return position

    def increment_distance(self, increment: float):
        near_plane = self._near_plane
        far_plane = self._far_plane

        if (near_plane + increment) >= 0.0:
            near_plane += increment
            far_plane += increment
            self._near_plane = clamp_float(near_plane, 0.0, float("inf"))
            self._far_plane = clamp_float(far_plane, 0.0, float("inf"))


# class Camera(CameraBase):
#     def __init__(self, width: int, height: int) -> None:
#         super().__init__(width, height)

#     def handle_mouse_movement(self, x: float, y: float) -> None:
#         px = self._previous_pointer[0]
#         py = self._previous_pointer[1]

#         dx = x - px
#         dy = y - py

#         sensitivity = 0.5
#         self._yaw += dx * sensitivity
#         self._pitch += dy * sensitivity
#         self._previous_pointer = (x, y)

#     def interpolate_scale(self, position: Vector3D, scale: float) -> float:
#         distance_from_camera = position.get_length()
#         if distance_from_camera == 0.0:
#             return 0.0

#         fov_radians = math.radians(self._fov)
#         scale_factor = 1 / math.tan(fov_radians / 2)

#         projected_circle_size = (scale * scale_factor) / distance_from_camera
#         return projected_circle_size

#     def calculate_yaw_projection(self, position: Vector3D) -> Vector3D:
#         yaw_radians = math.radians(self._yaw)
#         yaw_cos = math.cos(yaw_radians)
#         yaw_sin = math.sin(yaw_radians)

#         px = position.x
#         py = position.y
#         pz = position.z

#         yaw_x = (px * yaw_cos) - (pz * yaw_sin)
#         yaw_y = py
#         yaw_z = (px * yaw_sin) + (pz * yaw_cos)

#         yaw_vector = Vector3D(yaw_x, yaw_y, yaw_z)
#         return yaw_vector

#     def calculate_pitch_projection(self, position: Vector3D) -> Vector3D:
#         pitch_radians = math.radians(self._pitch)
#         pitch_cos = math.cos(pitch_radians)
#         pitch_sin = math.sin(pitch_radians)

#         px = position.x
#         py = position.y
#         pz = position.z

#         pitch_x = px
#         pitch_y = (py * pitch_cos) - (pz * pitch_sin)
#         pitch_z = (py * pitch_sin) + (pz * pitch_cos)

#         pitch_vector = Vector3D(pitch_x, pitch_y, pitch_z)
#         return pitch_vector

#     def calculate_perspective_projection(self, position: Vector3D):
#         width = self._width
#         height = self._height
#         fov = self._fov
#         near_plane = self._near_plane
#         far_plane = self._far_plane

#         xi = position.x
#         yi = position.y
#         zi = position.z

#         aspect_ratio = height / width
#         fov_radians = math.tan(math.radians(fov))

#         xo = xi * aspect_ratio * fov_radians
#         yo = yi * fov_radians
#         zo = zi * (far_plane / (far_plane - near_plane)) + 1

#         w = (-far_plane * near_plane) / (far_plane - near_plane)

#         if w != 0.0:
#             xo /= w
#             yo /= w
#             zo /= w

#         vo = Vector3D(xo, yo, zo)
#         return vo

#     def apply_view_transform(self, position: Vector3D) -> Vector3D:
#         yaw_radians = math.radians(self._yaw)
#         pitch_radians = math.radians(self._pitch)

#         yaw_cos = math.cos(yaw_radians)
#         yaw_sin = math.sin(yaw_radians)
#         pitch_cos = math.cos(pitch_radians)
#         pitch_sin = math.sin(pitch_radians)

#         px, py, pz = position.x, position.y, position.z

#         rx = (px * yaw_cos) + (pz * yaw_sin)
#         ry = (py * pitch_cos) - (rx * pitch_sin)
#         rz = (py * pitch_sin) + (rx * pitch_cos)

#         transformed_position = Vector3D(rx, ry, rz)
#         return transformed_position

#     def get_perspective_projection(self, position: Vector3D):
#         position = self.apply_view_transform(position)
#         position = self.calculate_perspective_projection(position)

#         return position

#     def increment_distance(self, increment: float):
#         near_plane = self._near_plane
#         far_plane = self._far_plane

#         if (near_plane + increment) >= 0.0:
#             near_plane += increment
#             far_plane += increment
#             self._near_plane = clamp_float(near_plane, 0.0, float("inf"))
#             self._far_plane = clamp_float(far_plane, 0.0, float("inf"))
