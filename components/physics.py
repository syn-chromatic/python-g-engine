import math
from components.vector_3d import Vector3D

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

    def _calculate_position(self, delta_t: float) -> None:
        self.position = self.position.add_vector(self.velocity.multiply(delta_t))
        self.velocity = self.velocity.add_vector(self.acceleration.multiply(delta_t))

    def _calculate_spin(self, delta_t: float):
        self.spin_velocity = self.spin_velocity.add_vector(
            self.spin_acceleration.multiply(delta_t)
        )
        x_rotation = self.spin_velocity.x * delta_t
        y_rotation = self.spin_velocity.y * delta_t
        z_rotation = self.spin_velocity.z * delta_t
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

    def _debug_freeze_on_collision(self, target: Self):
        self.velocity = Vector3D()
        target.velocity = Vector3D()

    def _debug_show_position_shifts(
        self, self_shifted: Vector3D, target_shifted: Vector3D
    ):
        from components.graphics import Graphics
        from components.particle import Particle

        p1 = Particle([(0.0, 0.0, 0.0)])
        p1.set_color((0.4, 0.8, 0.4))
        p1.physics.set_scale(3)
        p1.physics.position = self_shifted
        p1.draw_shape(Graphics())

        p2 = Particle([(0.0, 0.0, 0.0)])
        p2.set_color((0.8, 0.4, 0.4))
        p2.physics.set_scale(3)
        p2.physics.position = target_shifted
        p2.draw_shape(Graphics())

    def correct_shift_collision(
        self, target: Self, timestep: float, edge_distance: float
    ):
        edge = edge_distance + timestep

        direction = self.position.subtract_vector(target.position).normalize()

        self_shifted = self.position.add_vector(direction.multiply(-edge))
        target_shifted = target.position.add_vector(direction.multiply(edge))

        self.position = self_shifted
        target.position = target_shifted

    def calculate_collision_velocities(self, target: Self, centers_distance: Vector3D):
        centers_distance_n = centers_distance.normalize()

        v1i = self.velocity.dot_product(centers_distance_n)
        v2i = target.velocity.dot_product(centers_distance_n)
        v1p = self.velocity.subtract_vector(centers_distance_n.multiply(v1i))
        v2p = target.velocity.subtract_vector(centers_distance_n.multiply(v2i))

        m1 = self.mass
        m2 = target.mass
        v1f = ((v1i * (m1 - m2)) + 2 * (m2 * v2i)) / (m1 + m2)
        v2f = ((v2i * (m2 - m1)) + 2 * (m1 * v1i)) / (m1 + m2)
        v1 = v1p.add_vector(centers_distance_n.multiply(v1f))
        v2 = v2p.add_vector(centers_distance_n.multiply(v2f))

        self.velocity = v1
        target.velocity = v2

    def apply_forces(self, target: Self, timestep: float):

        force = target.position.subtract_vector(self.position)
        distance = force.get_length()

        if distance <= 0:
            return

        self.apply_attraction(target)
        self.apply_collision(target, timestep)

    def apply_attraction(self, target: Self):
        force = target.position.subtract_vector(self.position)
        distance = force.get_length()
        g_const = 0.0001
        strength = g_const * ((self.mass * target.mass) / distance)
        force = force.set_magnitude(strength)
        force = force.divide(self.mass)
        self.acceleration = self.acceleration.add_vector(force)
        self.spin_acceleration = self.spin_acceleration.add_vector(force)

    def apply_collision(self, target: Self, timestep: float):
        self_radius = self.scale + self.position.get_length() * timestep
        target_radius = target.scale + target.position.get_length() * timestep

        total_radius = self_radius + target_radius
        centers_distance = self.position.subtract_vector(target.position)
        edge_distance = centers_distance.get_length() - total_radius

        if edge_distance <= 0:
            self.calculate_collision_velocities(target, centers_distance)
            self.correct_shift_collision(target, timestep, edge_distance)

    def move_object(self, delta_t: float):
        self._calculate_position(delta_t)
        self._calculate_spin(delta_t)
        self.acceleration = self.acceleration.multiply(0)
        self.spin_acceleration = self.spin_acceleration.multiply(0)
