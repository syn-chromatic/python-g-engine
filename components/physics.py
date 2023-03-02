import math
from components.vector_3d import Vector3D

from typing_extensions import Self


class Physics:
    def __init__(self, shape: list[tuple[float, float, float]]):
        self.name = ""
        self.shape = shape
        self.position = Vector3D()
        self.velocity = Vector3D()
        self.acceleration = Vector3D()
        self.spin_velocity = Vector3D()
        self.spin_acceleration = Vector3D()
        self.mass = 1.0
        self.scale = 1.0
        self.collision = False
        self.collision_fc = 0

        self.center_of_mass = Vector3D(0, 0, 0).set_magnitude(self.mass)

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

    def apply_forces(self, target: Self, delta_t: float):

        force = target.position.subtract_vector(self.position)
        distance = force.get_length()

        if distance <= 0:
            return

        # self.apply_attraction(target, delta_t)
        self.apply_collision(target, delta_t)

    def apply_attraction(self, target: Self, delta_t: float):
        force = target.position.subtract_vector(self.position)
        length = force.get_length() * delta_t


        g_const = 0.0001

        # force = force.divide(length)
        strength = g_const * ((self.mass * target.mass) / length)
        force = force.multiply(strength)

        self.acceleration = self.acceleration.add_vector(force)
        self.spin_acceleration = self.spin_acceleration.add_vector(force)



    # def apply_attraction(self, target: Self, delta_t: float):
    #     force = target.position.subtract_vector(self.position)
    #     length_squared = force.get_length() * delta_t**2 # (xyz**2)

    #     if length_squared != 0:
    #         force = force.divide(math.sqrt(length_squared))
    #         g_const = 0.0001
    #         strength = g_const * ((self.mass * target.mass) / length_squared)
    #         force = force.multiply(strength)
    #     else:
    #         force = Vector3D(0, 0, 0)

    #     self.acceleration = self.acceleration.add_vector(force.divide(self.mass)).multiply(delta_t)
    #     self.spin_acceleration = self.spin_acceleration.add_vector(force.divide(self.mass)).multiply(delta_t)



    def apply_collision(self, target: Self, delta_t: float):
        self_radius = self.scale + self.position.get_length() * delta_t
        target_radius = target.scale + target.position.get_length() * delta_t

        total_radius = (self_radius + target_radius)
        self_centers_distnace = self.position.subtract_vector(target.position)
        # target_centers_distance = target.position.subtract_vector(self.position)

        # if self.collision or target.collision:
        #     self.collision = False
        #     return

        diff = self_centers_distnace.get_length() - total_radius

        if diff <= 0:
            collision_n = self_centers_distnace.normalize()
            # collision_n = (self.position.subtract_vector(target.position)).normalize()

            v1i = self.velocity.dot_product(collision_n)
            v2i = target.velocity.dot_product(collision_n)
            v1p = self.velocity.subtract_vector(collision_n.multiply(v1i))
            v2p = target.velocity.subtract_vector(collision_n.multiply(v2i))

            m1 = self.mass
            m2 = target.mass
            v1f = ((v1i * (m1 - m2)) + 2 * (m2 * v2i)) / (m1 + m2)
            v2f = ((v2i * (m2 - m1)) + 2 * (m1 * v1i)) / (m1 + m2)
            v1 = v1p.add_vector(collision_n.multiply(v1f))
            v2 = v2p.add_vector(collision_n.multiply(v2f))

            self.velocity = v1
            target.velocity = v2
            # test = Vector3D(1, 1, 1)
            # test = test.dot_product(self_centers_distnace)


            # self.position = self.position.add_vector(self_centers_distnace.divide(self_centers_distnace.get_length() - self_radius))
            # target.position = target.position.subtract_vector(self_centers_distnace.divide(self_centers_distnace.get_length() - target_radius))
            # self.collision = True
            # target.collision = True

            print("name", self.name)
            print("self_pos", self.position.__dict__)
            # print("targ_pos", target.position.__dict__)
            # print("centers_distance", self_centers_distnace.__dict__)
            print("diff", diff)

            # # print("cetners_distance_len2", self_centers_distnace.get_length_squared())
            # print("total_radius", total_radius)
            # print("collision_n", collision_n.__dict__)
            # print("v1i", v1i)
            # print("v2i", v2i)
            # print("v1p", v1p.__dict__)
            # print("v2p", v2p.__dict__)
            # print("m1", m1)
            # print("m2", m2)
            # print("v1f", v1f)
            # print("v2f", v2f)
            # print("v1", v1.__dict__)
            # print("v2", v2.__dict__)
            # print("v1_length", v1.get_length())
            # print("v2_length", v2.get_length())
            # # input()






    def move_object(self, delta_t: float):
        self._calculate_position(delta_t)
        self._calculate_spin(delta_t)
        self.acceleration = self.acceleration.multiply(0)
        self.spin_acceleration = self.spin_acceleration.multiply(0)
