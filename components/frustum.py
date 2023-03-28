import math

from components.vectors import Vector3D
from components.polygons import Mesh, Triangle, Quad

from dataclasses import dataclass


@dataclass
class Plane:
    A: float
    B: float
    C: float
    D: float


class Frustum:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.fov = 100
        self.near_plane = 0.1
        self.far_plane = 5000.0
        self.planes = self.make_frustum()

    def make_frustum(self) -> list[Plane]:
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
        return planes

    def make_plane(self, p0: Vector3D, n: Vector3D) -> Plane:
        n = n.normalize()

        pA = -n.x
        pB = -n.y
        pC = -n.z
        pD = -p0.dot_product(n)
        p = Plane(pA, pB, pC, pD)

        return p

    def get_plane_distance(self, point: Vector3D, plane: Plane):
        x, y, z = point.x, point.y, point.z
        distance = plane.A * x + plane.B * y + plane.C * z + plane.D
        return distance

    def get_plane_intersection(self, a: Vector3D, b: Vector3D, plane: Plane) -> float:
        ax, ay, az = a.x, a.y, a.z
        bx, by, bz = b.x, b.y, b.z

        distance = -self.get_plane_distance(a, plane)
        interpolation = plane.A * (bx - ax) + plane.B * (by - ay) + plane.C * (bz - az)
        if interpolation == 0:
            return 0
        return distance / interpolation

    def is_point_behind_plane(self, point: Vector3D, plane: Plane) -> bool:
        x, y, z = point.x, point.y, point.z
        distance = plane.A * x + plane.B * y + plane.C * z + plane.D
        is_inside_frustum = distance < 0
        return is_inside_frustum

    def is_point_in_frustum(self, point: Vector3D) -> bool:
        for plane in self.planes:
            is_behind_plane = self.is_point_behind_plane(point, plane)
            if is_behind_plane:
                return False
        return True

    def get_triangle_faces(
        self, output_polygon: list[int]
    ) -> list[tuple[int, int, int]]:
        faces = []
        for i in range(1, len(output_polygon) - 1):
            face = (output_polygon[0], output_polygon[i], output_polygon[i + 1])
            faces.append(face)
        return faces

    def clip_against_plane(self, mesh: Mesh, plane: Plane) -> None:
        output_polygons = []

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

                t = self.get_plane_intersection(a, b, plane)
                c = a.lerp_interpolation(b, t)

                ap_inside = self.is_point_behind_plane(a, plane)
                bp_inside = self.is_point_behind_plane(b, plane)

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
                    print(face)
                    new_vertices = tuple(output_vertices[idx] for idx in face)
                    new_polygon = Triangle(
                        vertices=new_vertices,
                        face=face,
                        shader=polygon.shader,
                        color=polygon.color,
                    )
                    output_polygons.append(new_polygon)

        mesh.polygons = output_polygons

    def frustum_clip(self, mesh: Mesh):
        for plane in self.planes:
            self.clip_against_plane(mesh, plane)
