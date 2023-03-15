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

    def interpolate_size(self, position: Vector3D, size: float) -> float:
        distance_from_camera = position.subtract_vector(self._position).get_length()
        if distance_from_camera == 0.0:
            return 0.0

        fov_radians = math.radians(self._fov)
        scale_factor = 1 / math.tan(fov_radians / 2)

        projected_circle_size = (size * scale_factor) / distance_from_camera
        return projected_circle_size

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


class Particle(Body):
    def __init__(self, shape: list[tuple[float, float, float]]) -> None:
        self.physics = Physics(shape)
        self.color = RGBA(1.0, 1.0, 1.0, 1.0)

    def set_color(self, color: RGBA) -> None:
        self.color = color

    def draw(self, graphics: Graphics, camera: Camera) -> None:
        self._draw_circle(graphics, camera)

    def _draw_circle(self, graphics: Graphics, camera: Camera) -> None:
        position = self._get_particle_position()
        size = self._get_particle_scale()

        projected = camera.get_perspective_projection(position)
        size = camera.interpolate_size(position, size)

        point = projected.x, projected.y
        graphics.draw_circle(point, size, self.color)

    def _get_scale_alpha(self, scale: float) -> float:
        max_scale = 300.0
        min_scale = max_scale / 2.0

        if scale < min_scale:
            return 1.0

        alpha_normalized = (scale - min_scale) / (max_scale - min_scale)
        alpha_clamped = clamp_float(alpha_normalized, 0.0, 1.0)
        alpha = 1.0 - alpha_clamped
        return alpha

    def _get_particle_position(self) -> Vector3D:
        return self.physics.position

    def _get_particle_scale(self) -> float:
        return self.physics.scale


class Vector3D:
    __slots__ = ("x", "y", "z")

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def multiply(self, num: float) -> Self:
        return Vector3D(self.x * num, self.y * num, self.z * num)

    def divide(self, num: float) -> Self:
        return Vector3D(self.x / num, self.y / num, self.z / num)

    def add_vector(self, vec: Self) -> Self:
        return Vector3D(self.x + vec.x, self.y + vec.y, self.z + vec.z)

    def subtract_vector(self, vec: Self) -> Self:
        return Vector3D(self.x - vec.x, self.y - vec.y, self.z - vec.z)

    def get_length_squared(self) -> float:
        return self.x**2.0 + self.y**2.0 + self.z**2.0

    def get_length(self) -> float:
        length_squared = self.get_length_squared()
        if length_squared == 0.0:
            return 0.0
        return math.sqrt(length_squared)

    def normalize(self) -> Self:
        length = self.get_length()
        if length == 0:
            return Vector3D(0.0, 0.0, 0.0)
        return Vector3D(self.x / length, self.y / length, self.z / length)

    def dot_product(self, vec: Self) -> float:
        return (self.x * vec.x) + (self.y * vec.y) + (self.z * vec.z)

    def cross_product(self, vec: Self) -> Self:
        x = self.y * vec.z - self.z * vec.y
        y = self.z * vec.x - self.x * vec.z
        z = self.x * vec.y - self.y * vec.x
        return Vector3D(x, y, z)

    def set_magnitude(self, magnitude: float) -> Self:
        length = self.get_length()
        x, y, z = self.x, self.y, self.z
        if length > 0:
            x = (self.x / length) * magnitude
            y = (self.y / length) * magnitude
            z = (self.z / length) * magnitude
        return Vector3D(x, y, z)
