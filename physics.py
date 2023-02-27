import math
from vector_3d import Vector3D

from typing_extensions import Self


class Physics:
    def __init__(self, shape: list[tuple[float, float, float]]):
        self.shape = shape
        self.position = Vector3D()
        self.velocity = Vector3D()
        self.acceleration = Vector3D()
        self.spin_velocity = Vector3D()
        self.spin_acceleration = Vector3D()
        self.mass = 1.0
        self.scale = 1.0

    @staticmethod
    def _rotate_x(
        xyz_point: tuple[float, float, float], theta: float
    ) -> tuple[float, float, float]:
        cs = math.cos(theta)
        sn = math.sin(theta)
        x = xyz_point[0]
        y = (cs * xyz_point[1]) - (sn * xyz_point[2])
        z = (sn * xyz_point[1]) + (cs * xyz_point[2])
        return (x, y, z)

    @staticmethod
    def _rotate_y(
        xyz_point: tuple[float, float, float], theta
    ) -> tuple[float, float, float]:
        cs = math.cos(theta)
        sn = math.sin(theta)
        x = (cs * xyz_point[0]) + (sn * xyz_point[2])
        y = xyz_point[1]
        z = (-sn * xyz_point[0]) + (cs * xyz_point[2])
        return (x, y, z)

    @staticmethod
    def _rotate_z(
        xyz_point: tuple[float, float, float], theta: float
    ) -> tuple[float, float, float]:
        cs = math.cos(theta)
        sn = math.sin(theta)
        x = (cs * xyz_point[0]) - (sn * xyz_point[1])
        y = (sn * xyz_point[0]) + (cs * xyz_point[1])
        z = xyz_point[2]
        return (x, y, z)

    @staticmethod
    def _constrain(val: float, min_val: float, max_val: float) -> float:
        return min(max_val, max(min_val, val))

    def _calculate_position(self) -> None:
        self.position = self.position.add_vector(self.velocity)
        self.velocity = self.velocity.add_vector(self.acceleration)

    def _calculate_spin(self):
        self.spin_velocity = self.spin_velocity.add_vector(self.spin_acceleration)
        x_rotation = self.spin_velocity.x
        y_rotation = self.spin_velocity.y
        z_rotation = self.spin_velocity.z
        shape = []
        for point in self.shape:
            point = self._rotate_x(point, x_rotation)
            point = self._rotate_y(point, y_rotation)
            point = self._rotate_z(point, z_rotation)
            shape.append(point)
        self.shape = shape

    def set_position(self, x: float, y: float, z: float):
        self.position = Vector3D(x, y, z)

    def set_velocity(self, x: float, y: float, z: float):
        self.velocity = Vector3D(x, y, z)

    def set_spin_velocity(self, x: float, y: float, z: float):
        self.spin_velocity = Vector3D(x, y, z)

    def set_acceleration(self, x: float, y: float, z: float):
        self.acceleration = Vector3D(x, y, z)

    def set_mass(self, mass: float):
        self.mass = mass

    def set_scale(self, scale: float):
        self.scale = scale

    def apply_attraction(self, target: Self):
        force = target.position.subtract_vector(self.position)
        distance = force.get_length()
        g_const = 0.0001
        strength = g_const * ((self.mass * target.mass) / distance)
        force = force.set_magnitude(strength)
        force = force.divide(self.mass)
        self.acceleration = self.acceleration.add_vector(force)
        self.spin_acceleration = self.spin_acceleration.add_vector(force)

    def move_object(self):
        self._calculate_position()
        self._calculate_spin()
        self.acceleration = self.acceleration.multiply(0)
        self.spin_acceleration = self.spin_acceleration.multiply(0)
