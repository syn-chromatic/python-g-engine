import math

from vector_3d import Vector3D


class CameraBase:
    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height
        self._camera_position = Vector3D()
        self.near_plane = 60.0
        self.far_plane = 160.0
        self.yaw = 0.0
        self.pitch = 0.0
        self.prev_mouse_pos = (width / 2.0, height / 2.0)


class Camera(CameraBase):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)

    def hande_mouse_movement(self, x: float, y: float) -> None:
        px = self.prev_mouse_pos[0]
        py = self.prev_mouse_pos[1]

        dx = x - px
        dy = y - py

        sensitivity = 0.5
        self.yaw += dx * sensitivity
        self.pitch += dy * sensitivity
        self.prev_mouse_pos = (x, y)

    def interpolate_radius(self, position: Vector3D, radius: float) -> float:
        z = position.z
        interpolation_value = (z + self.near_plane) / (self.far_plane - self.near_plane)
        radius_scaled = radius * interpolation_value
        return radius_scaled

    def yaw_projection(self, position: Vector3D) -> Vector3D:
        yaw_radians = math.radians(self.yaw)
        yaw_cos = math.cos(yaw_radians)
        yaw_sin = math.sin(yaw_radians)

        yaw_x = position.x * yaw_cos - position.z * yaw_sin
        yaw_y = position.y
        yaw_z = position.x * yaw_sin + position.z * yaw_cos

        yaw_vector = Vector3D(yaw_x, yaw_y, yaw_z)
        return yaw_vector

    def pitch_projection(self, position: Vector3D) -> Vector3D:
        pitch_radians = math.radians(self.pitch)
        pitch_cos = math.cos(pitch_radians)
        pitch_sin = math.sin(pitch_radians)

        pitch_x = position.x
        pitch_y = (position.y * pitch_cos) - (position.z * pitch_sin)
        pitch_z = (position.y * pitch_sin) + (position.z * pitch_cos)

        pitch_vector = Vector3D(pitch_x, pitch_y, pitch_z)
        return pitch_vector

    def perspective_projection(self, position: Vector3D):
        position = self.yaw_projection(position)
        position = self.pitch_projection(position)

        x = (position.x * self.near_plane) / position.z
        y = (position.y * self.near_plane) / position.z

        z = (self.far_plane + self.near_plane) / (self.near_plane - self.far_plane)
        w = -position.z / (self.far_plane - self.near_plane)

        half_w = self._width / 2.0
        half_h = self._height / 2.0
        xp = (x * w) + half_w
        yp = (y * w) + half_h
        zp = z * w

        position = Vector3D(xp, yp, zp)
        return position

    @staticmethod
    def clamp(num, min_value, max_value):
        num = max(min(num, max_value), min_value)
        return num

    def increment_distance(self, increment: float):
        if (self.near_plane + increment) >= 0.0:
            self.near_plane += increment
            self.far_plane += increment
            self.near_plane = self.clamp(self.near_plane, 0.0, float("inf"))
            self.far_plane = self.clamp(self.far_plane, 0.0, float("inf"))
