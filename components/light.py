from components.vectors import Vector3D


class Light:
    def __init__(
        self,
        position: Vector3D,
        target: Vector3D,
        ambient: Vector3D,
        diffuse: Vector3D,
        specular: Vector3D,
        lumens: float,
    ) -> None:
        self.position = position
        self.target = target
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.lumens = lumens

    @staticmethod
    def get_light() -> "Light":
        position = Vector3D(300.0, 1000.0, 3000.0)
        target = Vector3D(0.0, 0.0, 0.0)
        ambient_color = Vector3D(0.6, 0.6, 0.6)
        diffuse_color = Vector3D(0.4, 0.4, 0.4)
        specular_color = Vector3D(0.2, 0.2, 0.2)
        lumens = 4_000.0

        light = Light(
            position=position,
            target=target,
            ambient=ambient_color,
            diffuse=diffuse_color,
            specular=specular_color,
            lumens=lumens,
        )
        return light

    @staticmethod
    def get_light_from_position(position: Vector3D, target: Vector3D) -> "Light":
        ambient_color = Vector3D(0.8, 0.8, 0.8)
        diffuse_color = Vector3D(0.5, 0.5, 0.5)
        specular_color = Vector3D(0.2, 0.2, 0.2)
        lumens = 500.0

        light = Light(
            position=position,
            target=target,
            ambient=ambient_color,
            diffuse=diffuse_color,
            specular=specular_color,
            lumens=lumens,
        )
        return light
