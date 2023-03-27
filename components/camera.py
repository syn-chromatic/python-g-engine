import math

from components.vectors import Vector3D
from shared_dcs import Mesh, Triangle, Quad

from dataclasses import dataclass
from typing import Optional
from components.utils import clamp_float
from copy import deepcopy


@dataclass
class Plane:
    A: float
    B: float
    C: float
    D: float


@dataclass
class Frustum:
    planes: list[Plane]


class Camera:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.fov = 100
        self.near_plane = 0.1
        self.far_plane = 5000.0
        self.yaw = 0.0
        self.pitch = 0.0
        self.camera_position = Vector3D(-100.0, 25.0, 500.0)
        self.camera_target = Vector3D(0.0, 0.0, 0.0)
        self.side_direction = Vector3D(1.0, 0.0, 0.0)
        self.up_direction = Vector3D(0.0, 1.0, 0.0)
        self.look_direction = Vector3D(0.0, 0.0, 1.0)
        self.frustum = self.make_frustum()

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
        half_width = self.width / 2.0
        half_height = self.height / 2.0

        x = (position.x) * half_width
        y = (position.y) * half_height

        screen_coordinates = Vector3D(x, y, position.z)
        return screen_coordinates

    def calculate_perspective_projection(self, position: Vector3D) -> Vector3D:
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
        zo = zi * -((zf - zn) / (zn - zf)) + ((2 * zf * zn) / (zn - zf))

        if zi != 0.0:
            xo /= -zi
            yo /= -zi
            zo /= -zi

        vo = Vector3D(xo, yo, zo)
        return vo

    def get_screen_coordinates(self, world_position: Vector3D):
        view = self.apply_view_transform(world_position)
        ndc_projection = self.calculate_perspective_projection(view)
        screen = self.ndc_to_screen_coordinates(ndc_projection)
        return screen

    def apply_projection_polygons(self, mesh: Mesh) -> Optional[Mesh]:
        mesh = deepcopy(mesh)

        for polygon in mesh.polygons:
            vertices = list(polygon.vertices)
            for idx, vertex in enumerate(vertices):
                vertex = self.apply_view_transform(vertex)
                vertex = vertex.multiply(-1)
                vertices[idx] = vertex
            polygon.vertices = tuple(vertices)

        if self.enable_frustum_clipping:
            self.frustum_clip(mesh)

        for polygon in mesh.polygons:
            vertices = list(polygon.vertices)
            for idx, vertex in enumerate(vertices):
                vertex = self.calculate_perspective_projection(vertex)
                vertex = self.ndc_to_screen_coordinates(vertex)
                vertices[idx] = vertex
            polygon.vertices = tuple(vertices)
        return mesh

    def get_plane_intersection(self, a: Vector3D, b: Vector3D, p: Plane) -> float:
        ax, ay, az = a.x, a.y, a.z
        bx, by, bz = b.x, b.y, b.z

        numerator = -(ax * p.A + ay * p.B + az * p.C + p.D)
        denominator = p.A * (bx - ax) + p.B * (by - ay) + p.C * (bz - az)
        if denominator == 0:
            return 0
        return numerator / denominator

    def is_point_inside_frustum(self, point: Vector3D, plane: Plane) -> bool:
        x, y, z = point.x, point.y, point.z
        distance = plane.A * x + plane.B * y + plane.C * z + plane.D
        is_inside_frustum = distance < 0
        return is_inside_frustum

    def get_triangle_faces(
        self, output_polygon: list[int]
    ) -> list[tuple[int, int, int]]:
        faces = []
        for i in range(1, len(output_polygon) - 1):
            face = (output_polygon[0], output_polygon[i], output_polygon[i + 1])
            faces.append(face)
        return faces

    def clip_against_plane(self, mesh: Mesh, p: Plane):
        new_polygons = []

        for polygon in mesh.polygons:
            if isinstance(polygon, Quad):
                continue

            input_vertices = polygon.vertices
            output_vertices = []
            output_faces = []

            vertex_length = len(output_vertices)

            for i in range(3):
                a = input_vertices[i]
                b = input_vertices[(i + 1) % 3]

                t = self.get_plane_intersection(a, b, p)
                c = a.lerp_interpolation(b, t)

                ap_inside = self.is_point_inside_frustum(a, p)
                bp_inside = self.is_point_inside_frustum(b, p)

                if not bp_inside:
                    if ap_inside:
                        output_vertices.append(c)
                        output_faces.append(vertex_length)
                        vertex_length += 1

                    output_vertices.append(b)
                    output_faces.append(vertex_length)
                    vertex_length += 1

                elif not ap_inside:
                    output_vertices.append(c)
                    output_faces.append(vertex_length)
                    vertex_length += 1

            if len(output_faces) > 2:
                faces = self.get_triangle_faces(output_faces)
                for face in faces:
                    new_vertices = tuple(output_vertices[idx] for idx in face)
                    new_polygon = Triangle(new_vertices, face, polygon.shader)
                    new_polygons.append(new_polygon)

        mesh.polygons = new_polygons

    def frustum_clip(self, mesh: Mesh):
        for plane in self.frustum.planes:
            self.clip_against_plane(mesh, plane)

    def make_frustum(self) -> Frustum:
        fov = self.fov
        aspect = self.width / self.height
        near = -self.near_plane
        far = -self.far_plane
        fov_rad = math.tan(math.radians(fov / 2))

        y_top = abs(near) * fov_rad
        x_right = y_top * aspect

        # Near Plane
        p0_n = Vector3D(0.0, 0.0, near)
        n_n = Vector3D(0.0, 0.0, -1.0)
        near_plane = self.make_plane(p0_n, n_n)

        # Far Plane
        p0_f = Vector3D(0.0, 0.0, far)
        n_f = Vector3D(0.0, 0.0, 1.0)
        far_plane = self.make_plane(p0_f, n_f)

        # Top Plane
        p0_t = Vector3D(0.0, y_top, near)
        n_t = Vector3D(0.0, near / y_top, -1.0).normalize()
        top_plane = self.make_plane(p0_t, n_t)

        # Bottom Plane
        p0_b = Vector3D(0.0, -y_top, near)
        n_b = Vector3D(0.0, -near / y_top, -1.0).normalize()
        bottom_plane = self.make_plane(p0_b, n_b)

        # Left Plane
        p0_l = Vector3D(-x_right, 0.0, near)
        n_l = Vector3D(-near / x_right, 0.0, -1.0).normalize()
        left_plane = self.make_plane(p0_l, n_l)

        # Right Plane
        p0_r = Vector3D(x_right, 0.0, near)
        n_r = Vector3D(near / x_right, 0.0, -1.0).normalize()
        right_plane = self.make_plane(p0_r, n_r)

        planes = [
            near_plane,
            far_plane,
            top_plane,
            bottom_plane,
            left_plane,
            right_plane,
        ]
        frustum = Frustum(planes)
        return frustum

    def make_plane(self, p0: Vector3D, n: Vector3D) -> Plane:
        n = n.normalize()

        pA = n.x
        pB = n.y
        pC = n.z
        pD = -p0.dot_product(n)
        p = Plane(pA, pB, pC, pD)

        return p

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

    def get_plane_points(
        self,
    ) -> list[tuple[tuple[Vector3D, Vector3D, Vector3D], Vector3D]]:
        look_dir = self.camera_target.subtract_vector(self.camera_position).normalize()
        side_dir = look_dir.cross_product(self.up_direction).normalize()
        up_dir = side_dir.cross_product(look_dir).normalize()

        near_dir = look_dir.multiply(self.near_plane)
        near_center = self.camera_position.add_vector(near_dir)
        far_center = self.camera_position.add_vector(look_dir.multiply(self.far_plane))

        aspect_ratio = self.width / self.height
        fov_rad = math.tan(math.radians(self.fov / 2))

        near_height = 2 * self.near_plane * fov_rad
        near_width = near_height * aspect_ratio
        far_height = 2 * self.far_plane * fov_rad
        far_width = far_height * aspect_ratio

        near_up = up_dir.multiply(near_height / 2)
        near_right = side_dir.multiply(near_width / 2)
        far_up = up_dir.multiply(far_height / 2)
        far_right = side_dir.multiply(far_width / 2)

        points = [
            near_center.subtract_vector(near_right).subtract_vector(near_up),
            near_center.add_vector(near_right).subtract_vector(near_up),
            near_center.add_vector(near_right).add_vector(near_up),
            near_center.subtract_vector(near_right).add_vector(near_up),
            far_center.subtract_vector(far_right).subtract_vector(far_up),
            far_center.add_vector(far_right).subtract_vector(far_up),
            far_center.add_vector(far_right).add_vector(far_up),
            far_center.subtract_vector(far_right).add_vector(far_up),
        ]

        planes = [
            (points[0], points[3], points[2]),
            (points[4], points[5], points[6]),
            (points[0], points[1], points[5]),
            (points[2], points[3], points[7]),
            (points[0], points[4], points[7]),
            (points[1], points[2], points[6]),
        ]

        planes_normals = []
        for plane in planes:
            a, b, c = plane
            ab = b.subtract_vector(a)
            ac = c.subtract_vector(a)
            normal = ab.cross_product(ac).normalize()

            planes_normals.append((plane, normal))
        return planes_normals

    def is_point_in_frustum(self, position: Vector3D) -> bool:
        look_dir = self.camera_target.subtract_vector(self.camera_position).normalize()
        side_dir = look_dir.cross_product(self.up_direction).normalize()
        up_dir = side_dir.cross_product(look_dir).normalize()

        near_dir = look_dir.multiply(self.near_plane)
        near_center = self.camera_position.add_vector(near_dir)
        far_center = self.camera_position.add_vector(look_dir.multiply(self.far_plane))

        aspect_ratio = self.width / self.height
        fov_rad = math.tan(math.radians(self.fov / 2))

        near_height = 2 * self.near_plane * fov_rad
        near_width = near_height * aspect_ratio
        far_height = 2 * self.far_plane * fov_rad
        far_width = far_height * aspect_ratio

        near_up = up_dir.multiply(near_height / 2)
        near_right = side_dir.multiply(near_width / 2)
        far_up = up_dir.multiply(far_height / 2)
        far_right = side_dir.multiply(far_width / 2)

        points = [
            near_center.subtract_vector(near_right).subtract_vector(near_up),
            near_center.add_vector(near_right).subtract_vector(near_up),
            near_center.add_vector(near_right).add_vector(near_up),
            near_center.subtract_vector(near_right).add_vector(near_up),
            far_center.subtract_vector(far_right).subtract_vector(far_up),
            far_center.add_vector(far_right).subtract_vector(far_up),
            far_center.add_vector(far_right).add_vector(far_up),
            far_center.subtract_vector(far_right).add_vector(far_up),
        ]

        planes = [
            (points[0], points[3], points[2]),
            (points[4], points[5], points[6]),
            (points[0], points[1], points[5]),
            (points[2], points[3], points[7]),
            (points[0], points[4], points[7]),
            (points[1], points[2], points[6]),
        ]

        for plane in planes:
            a, b, c = plane
            ab = b.subtract_vector(a)
            ac = c.subtract_vector(a)
            normal = ab.cross_product(ac).normalize()
            ap = position.subtract_vector(a)

            if normal.dot_product(ap) < 0:
                return False

        return True

    def increment_plane(self, increment: float):
        near_plane = self.near_plane
        far_plane = self.far_plane

        if (near_plane + increment) > 0.1:
            near_plane += increment
            far_plane += increment
            self.near_plane = clamp_float(near_plane, 0.1, float("inf"))
            self.far_plane = clamp_float(far_plane, near_plane, float("inf"))

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

    # def clip_against_plane(self, polygons: list[Polygons], p: Plane):
    #     for polys in polygons:
    #         input_vertices = polys.type.vertices
    #         input_faces = polys.type.faces

    #         output_vertices = input_vertices.copy()
    #         output_faces = []

    #         for face in input_faces:
    #             output_polygon = []
    #             for i in range(len(face)):
    #                 a_idx = face[i]
    #                 b_idx = face[(i + 1) % len(face)]
    #                 a = input_vertices[a_idx]
    #                 b = input_vertices[b_idx]

    #                 t = self.get_plane_intersection(a, b, p)
    #                 c = self.lerp_interpolation(a, b, t)

    #                 if not self.is_point_behind_plane(b, p):
    #                     if self.is_point_behind_plane(a, p):
    #                         new_idx = len(output_vertices)
    #                         output_vertices.append(c)
    #                         output_polygon.append(new_idx)
    #                     output_polygon.append(b_idx)
    #                 elif not self.is_point_behind_plane(a, p):
    #                     new_idx = len(output_vertices)
    #                     output_vertices.append(c)
    #                     output_polygon.append(new_idx)

    #             n = len(output_polygon)
    #             if n == 3:
    #                 output_faces.append(tuple(output_polygon))
    #             elif n == 4:
    #                 output_faces.append((output_polygon[0], output_polygon[1], output_polygon[2]))
    #                 output_faces.append((output_polygon[0], output_polygon[2], output_polygon[3]))
    #             elif n == 5:  # One quad and one triangle
    #                 output_faces.append((output_polygon[0], output_polygon[1], output_polygon[2]))
    #                 output_faces.append((output_polygon[2], output_polygon[3], output_polygon[4]))

    #         polys.type.vertices = output_vertices
    #         polys.type.faces = output_faces
