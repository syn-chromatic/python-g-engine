import math

from components.frustum import Frustum
from components.vectors import Vector3D
from shared_dcs import Mesh

from typing import Optional
from components.utils import clamp_float
from copy import deepcopy


class Camera:
    def __init__(self, width: int, height: int) -> None:
        self.frustum = Frustum(width, height)
        self.yaw = 0.0
        self.pitch = 0.0
        self.camera_position = Vector3D(-100.0, 25.0, 500.0)
        self.camera_target = Vector3D(0.0, 0.0, 0.0)
        self.side_direction = Vector3D(1.0, 0.0, 0.0)
        self.up_direction = Vector3D(0.0, 1.0, 0.0)
        self.look_direction = Vector3D(0.0, 0.0, 1.0)

        self.previous_pointer = (width / 2.0, height / 2.0)
        self.enable_frustum_clipping = True

        self.save()

    def save(self):
        self.dict = deepcopy(self.__dict__)

    def toggle_frustum_clipping(self):
        self.enable_frustum_clipping = not self.enable_frustum_clipping
        print("FRUSTUM CLIPPING:", self.enable_frustum_clipping)

    def apply_view_transform(self, position: Vector3D) -> Vector3D:
        self.apply_direction_adjustment()

        look_dir = self.look_direction
        side_dir = self.side_direction
        up_dir = self.up_direction

        point = position.subtract_vector(self.camera_position)
        x = point.dot_product(side_dir)
        y = point.dot_product(up_dir)
        z = point.dot_product(look_dir)

        translated_point = Vector3D(x, y, z)
        return translated_point

    def ndc_to_screen_coordinates(self, position: Vector3D) -> Vector3D:
        half_width = self.frustum.width / 2.0
        half_height = self.frustum.height / 2.0

        x = (position.x) * half_width
        y = (position.y) * half_height

        screen_coordinates = Vector3D(x, y, position.z)
        return screen_coordinates

    def calculate_perspective_projection(self, position: Vector3D) -> Vector3D:
        width = self.frustum.width
        height = self.frustum.height
        fov_degrees = self.frustum.fov
        zn = self.frustum.near_plane
        zf = self.frustum.far_plane

        xi = position.x
        yi = position.y
        zi = position.z

        aspect_ratio = width / height
        fov_rad = math.tan(math.radians(fov_degrees / 2))

        xo = xi * (1 / (fov_rad * aspect_ratio))
        yo = yi * (1 / (fov_rad))
        zo = zi * -((zf - zn) / (zn - zf)) + ((2 * zf * zn) / (zn - zf))

        if zi != 0.0:
            xo /= -zi
            yo /= -zi
            zo /= -zi

        vo = Vector3D(xo, yo, zo)
        return vo

    def apply_projection_polygons(self, mesh: Mesh) -> Optional[Mesh]:
        mesh = deepcopy(mesh)

        for polygon in mesh.polygons:
            vertices = list(polygon.vertices)
            for idx, vertex in enumerate(vertices):
                vertex = self.apply_view_transform(vertex)
                in_frustum = self.frustum.is_point_in_frustum(vertex)

                if not in_frustum:
                    polygon.color = (20, 255, 20)
                else:
                    polygon.color = (255, 255, 255)

                vertices[idx] = vertex
            polygon.vertices = tuple(vertices)

        if self.enable_frustum_clipping:
            self.frustum.frustum_clip(mesh)

        for polygon in mesh.polygons:
            vertices = list(polygon.vertices)
            for idx, vertex in enumerate(vertices):
                vertex = self.calculate_perspective_projection(vertex)
                vertex = self.ndc_to_screen_coordinates(vertex)
                vertices[idx] = vertex
            polygon.vertices = tuple(vertices)
        return mesh

    def handle_mouse_movement(self, x: float, y: float) -> None:
        sens_x = 0.3
        sens_y = 0.1

        dx = x - self.previous_pointer[0]
        dy = y - self.previous_pointer[1]
        self.previous_pointer = (x, y)

        self.yaw += dx * sens_x
        self.pitch += dy * -sens_y

        if self.pitch > 90.0:
            self.pitch = 90.0
        elif self.pitch < -90.0:
            self.pitch = -90.0
        self.apply_mouse_movement()

    def apply_direction_adjustment(self):
        self.look_direction = self.camera_target.subtract_vector(self.camera_position)
        self.look_direction = self.look_direction.normalize()
        self.side_direction = self.look_direction.cross_product(self.up_direction)
        self.side_direction = self.side_direction.normalize()

        yaw_rad = math.radians(self.yaw)
        pitch_rad = math.radians(self.pitch - 90.0)
        up_x = math.cos(yaw_rad) * math.cos(pitch_rad)
        up_y = math.sin(pitch_rad)
        up_z = math.sin(yaw_rad) * math.cos(pitch_rad)
        self.up_direction = Vector3D(up_x, up_y, up_z).normalize()

    def apply_mouse_movement(self):
        yaw_rad = math.radians(self.yaw)
        pitch_rad = math.radians(self.pitch)

        direction_x = math.cos(yaw_rad) * math.cos(pitch_rad)
        direction_y = math.sin(pitch_rad)
        direction_z = math.sin(yaw_rad) * math.cos(pitch_rad)

        direction = Vector3D(direction_x, direction_y, direction_z)
        self.camera_target = self.camera_position.add_vector(direction)
        self.apply_direction_adjustment()

    def increment_position_x(self, increment: float):
        side_vector = self.side_direction.multiply(-increment)
        side_vector.y = 0
        self.camera_position = self.camera_position.add_vector(side_vector)
        self.camera_target = self.camera_position.add_vector(self.look_direction)

    def increment_position_y(self, increment: float):
        up_vector = self.up_direction.multiply(increment)
        self.camera_position = self.camera_position.add_vector(up_vector)
        self.camera_target = self.camera_position.add_vector(self.look_direction)

    def increment_position_z(self, increment: float):
        look_vector = self.look_direction.multiply(increment)
        look_vector.y = 0
        self.camera_position = self.camera_position.add_vector(look_vector)
        self.camera_target = self.camera_position.add_vector(self.look_direction)

    def increment_plane(self, increment: float):
        near_plane = self.frustum.near_plane
        far_plane = self.frustum.far_plane

        if (near_plane + increment) > 0.1:
            near_plane += increment
            far_plane += increment
            self.frustum.near_plane = clamp_float(near_plane, 0.1, float("inf"))
            self.frustum.far_plane = clamp_float(far_plane, near_plane, float("inf"))

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
