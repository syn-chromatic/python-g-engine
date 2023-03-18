import math

from components.vectors import Vector3D
from components.utils import clamp_float
from copy import deepcopy


class Camera:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.fov = 100
        self.near_plane = 1
        self.far_plane = 1000.0
        self.yaw = 0.0
        self.pitch = 0.0
        self.camera_position = Vector3D(0.0, 0.0, 1000.0)
        self.camera_target = Vector3D(0.0, 0.0, 0.0)
        self.side_direction = Vector3D(1.0, 0.0, 0.0)
        self.up_direction = Vector3D(0.0, 1.0, 0.0)
        self.look_direction = Vector3D(0.0, 0.0, 1.0)

        self.previous_pointer = (width / 2.0, height / 2.0)
        self.save()

    def save(self):
        self.dict = deepcopy(self.__dict__)

    def apply_view_transform(self, position: Vector3D) -> Vector3D:
        look_dir = self.camera_target.subtract_vector(self.camera_position).normalize()
        side_dir = look_dir.cross_product(self.up_direction).normalize()
        up_dir = side_dir.cross_product(look_dir).normalize()

        translated_point = position.subtract_vector(self.camera_position)
        x = translated_point.dot_product(side_dir)
        y = translated_point.dot_product(up_dir)
        z = translated_point.dot_product(look_dir)

        translated_point = Vector3D(x, y, z)
        return translated_point

    def ndc_to_screen_coordinates(self, position: Vector3D) -> Vector3D:
        half_width = self.width / 2.0
        half_height = self.height / 2.0

        x = (position.x) * half_width
        y = (position.y) * half_height

        return Vector3D(x, y, position.z)

    def get_screen_coordinates(self, position: Vector3D):
        view = self.apply_view_transform(position)
        projection = self.calculate_perspective_projection(view)
        screen = self.ndc_to_screen_coordinates(projection)
        return screen

    def calculate_perspective_projection(self, position: Vector3D):
        width = self.width
        height = self.height
        fov_degrees = self.fov
        zn = self.near_plane
        zf = self.far_plane

        xi = position.x
        yi = position.y
        zi = position.z

        aspect_ratio = width / height
        fov_rad = math.tan(math.radians(fov_degrees / 2))

        xo = xi * (1 / (fov_rad * aspect_ratio))
        yo = yi * (1 / (fov_rad))
        zo = zi * ((-zf - zn) / (zn - zf)) + ((2 * zf * zn) / (zn - zf))

        if zi != 0.0:
            xo /= -zi
            yo /= -zi
            zo /= -zi

        vo = Vector3D(xo, yo, zo)
        return vo

    def handle_mouse_movement(self, x: float, y: float) -> None:
        sensitivityx = 0.3
        sensitivityy = 0.1

        dx = x - self.previous_pointer[0]
        dy = y - self.previous_pointer[1]
        self.previous_pointer = (x, y)

        self.yaw += dx * sensitivityx
        self.pitch += dy * sensitivityy

        if self.pitch > 89.0:
            self.pitch = 89.0
        elif self.pitch < -89.0:
            self.pitch = -89.0
        self.apply_mouse_movement()

    def apply_mouse_movement(self):
        yaw_rad = math.radians(self.yaw)
        pitch_rad = math.radians(self.pitch)

        direction_x = math.cos(yaw_rad) * math.cos(pitch_rad)
        direction_y = math.sin(pitch_rad)
        direction_z = math.sin(yaw_rad) * math.cos(pitch_rad)

        direction = Vector3D(direction_x, direction_y, direction_z)
        self.camera_target = self.camera_position.add_vector(direction)

        self.look_direction = self.camera_target.subtract_vector(self.camera_position)
        self.look_direction = self.look_direction.normalize()
        self.side_direction = self.look_direction.cross_product(self.up_direction)
        self.side_direction = self.side_direction.normalize()
        self.up_direction = self.side_direction.cross_product(self.look_direction)
        self.up_direction = self.up_direction.normalize()

    def increment_plane(self, increment: float):
        near_plane = self.near_plane
        far_plane = self.far_plane

        if (near_plane + increment) >= 0.1:
            near_plane += increment
            far_plane += increment
            self.near_plane = clamp_float(near_plane, 0.0, float("inf"))
            self.far_plane = clamp_float(far_plane, 0.0, float("inf"))

    def increment_position_x(self, increment: float):
        side_vector = self.side_direction.multiply(increment)
        self.camera_position = self.camera_position.add_vector(side_vector)
        self.camera_target = self.camera_position.add_vector(self.look_direction)

    def increment_position_y(self, increment: float):
        up_vector = self.up_direction.multiply(increment)
        self.camera_position = self.camera_position.add_vector(up_vector)
        self.camera_target = self.camera_position.add_vector(self.look_direction)

    def increment_position_z(self, increment: float):
        look_vector = self.look_direction.multiply(increment)
        self.camera_position = self.camera_position.add_vector(look_vector)
        self.camera_target = self.camera_position.add_vector(self.look_direction)

    def increment_target_x(self, increment: float):
        self.camera_target.x += increment

    def increment_target_y(self, increment: float):
        self.camera_target.y += increment

    def increment_target_z(self, increment: float):
        self.camera_target.z += increment

    def reset(self):
        class_dict = deepcopy(self.dict)

        for variable, value in class_dict.items():
            self.__setattr__(variable, value)
