import math
import random
from components.vector_3d import Vector3D
from components.shared_dcs import PhysicsProperties, CollisionProperties


from typing import Optional
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
        self.g_const = 0.0001

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

    def _calculate_position(self, timestep: float) -> None:
        timestep_velocity = self.velocity.multiply(timestep)
        timestep_acceleration = self.acceleration.multiply(timestep)
        self.position = self.position.add_vector(timestep_velocity)
        self.velocity = self.velocity.add_vector(timestep_acceleration)

    def _calculate_spin(self, timestep: float):
        timestep_spin_acc = self.spin_acceleration.multiply(timestep)
        self.spin_velocity = self.spin_velocity.add_vector(timestep_spin_acc)
        x_rotation = self.spin_velocity.x * timestep
        y_rotation = self.spin_velocity.y * timestep
        z_rotation = self.spin_velocity.z * timestep
        shape = []
        for point in self.shape:
            point = self._rotate_x(point, x_rotation)
            point = self._rotate_y(point, y_rotation)
            point = self._rotate_z(point, z_rotation)
            shape.append(point)
        self.shape = shape

    def get_random_direction(self):
        x_rnd = random.uniform(-1.0, 1.0)
        y_rnd = random.uniform(-1.0, 1.0)
        direction = Vector3D(x_rnd, y_rnd, 0.0)
        return direction

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

    def create_physics_properties(
        self, collision_properties: Optional[CollisionProperties]
    ) -> PhysicsProperties:
        physics_properties = PhysicsProperties(collision_properties)
        return physics_properties

    def create_collision_properties(
        self,
        target: Self,
        self_shifted: Vector3D,
        target_shifted: Vector3D,
        direction: Vector3D,
    ) -> CollisionProperties:
        self_position = self.position
        target_position = target.position
        collision_properties = CollisionProperties(
            self_position=self_position,
            target_position=target_position,
            self_shifted=self_shifted,
            target_shifted=target_shifted,
            direction=direction,
        )
        return collision_properties

    def correct_shift_collision(
        self,
        target: Self,
        timestep: float,
        direction: Vector3D,
        edge_distance: float,
    ) -> tuple[Vector3D, Vector3D]:
        edge = edge_distance + timestep
        if direction.get_length_squared() == 0.0:
            direction = self.get_random_direction()

        self_edge_vec = direction.multiply(-edge)
        target_edge_vec = direction.multiply(edge)

        self_shifted = self.position.add_vector(self_edge_vec)
        target_shifted = target.position.add_vector(target_edge_vec)

        self.position = self_shifted
        target.position = target_shifted
        return self_shifted, target_shifted

    def calculate_collision_velocities(self, target: Self, direction: Vector3D):
        v1i = self.velocity.dot_product(direction)
        v2i = target.velocity.dot_product(direction)

        v1i_vec = direction.multiply(v1i)
        v2i_vec = direction.multiply(v2i)

        v1p = self.velocity.subtract_vector(v1i_vec)
        v2p = target.velocity.subtract_vector(v2i_vec)

        m1 = self.mass
        m2 = target.mass
        v1f = ((v1i * (m1 - m2)) + 2 * (m2 * v2i)) / (m1 + m2)
        v2f = ((v2i * (m2 - m1)) + 2 * (m1 * v1i)) / (m1 + m2)

        v1f_vec = direction.multiply(v1f)
        v2f_vec = direction.multiply(v2f)

        v1 = v1p.add_vector(v1f_vec)
        v2 = v2p.add_vector(v2f_vec)

        self.velocity = v1
        target.velocity = v2

    def apply_forces(self, target: Self, timestep: float) -> PhysicsProperties:
        # Target-To-Self Distance
        tts_distance = target.position.subtract_vector(self.position)

        self.apply_attraction(target, tts_distance)
        collision_properties = self.apply_collision(target, tts_distance, timestep)
        physics_properties = self.create_physics_properties(collision_properties)

        return physics_properties

    def apply_attraction(self, target: Self, tts_distance: Vector3D):
        distance = tts_distance.get_length()

        if distance > 0.0:
            strength = self.g_const * ((self.mass * target.mass) / distance)
            force = tts_distance.set_magnitude(strength)
            force = force.divide(self.mass)
            self.acceleration = self.acceleration.add_vector(force)
            self.spin_acceleration = self.spin_acceleration.add_vector(force)

    def apply_collision(
        self, target: Self, tts_distance: Vector3D, timestep: float
    ) -> Optional[CollisionProperties]:
        self_radius = self.scale + self.position.get_length() * timestep
        target_radius = target.scale + target.position.get_length() * timestep

        total_radius = self_radius + target_radius
        edge_distance = tts_distance.get_length() - total_radius

        if edge_distance <= 0:
            # Self-To-Target Distance
            stt_distance = tts_distance.multiply(-1)
            stt_direction = stt_distance.normalize()
            self.calculate_collision_velocities(target, stt_direction)

            shift_args = (target, timestep, stt_direction, edge_distance)
            self_shifted, target_shifted = self.correct_shift_collision(*shift_args)

            properties_args = (target, self_shifted, target_shifted, stt_direction)
            collision_properties = self.create_collision_properties(*properties_args)
            return collision_properties

    def update(self, timestep: float):
        self._calculate_position(timestep)
        self._calculate_spin(timestep)
        self.acceleration = self.acceleration.multiply(0)
        self.spin_acceleration = self.spin_acceleration.multiply(0)
