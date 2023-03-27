from components.vectors import Vector3D
from components.shared_dcs import Polygons, Quads


class Light:
    def __init__(
        self,
        position: Vector3D,
        ambient: Vector3D,
        diffuse: Vector3D,
        specular: Vector3D,
    ) -> None:
        self.position = position
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular

    @staticmethod
    def get_light() -> "Light":
        light_position = Vector3D(300.0, 500.0, 400.0)
        ambient_color = Vector3D(0.6, 0.6, 0.6)
        diffuse_color = Vector3D(0.1, 0.1, 0.1)
        specular_color = Vector3D(1.0, 1.0, 1.0)

        light = Light(
            position=light_position,
            ambient=ambient_color,
            diffuse=diffuse_color,
            specular=specular_color,
        )
        return light


class Shaders:
    def __init__(self, polygons: list[Polygons]) -> None:
        self.polygons = polygons

    def apply_lighting(self, light: Light, viewer_position: Vector3D) -> None:

        for polygon in self.polygons:
            if isinstance(polygon.type, Quads):
                continue

            triangles = polygon.type
            vertices = triangles.vertices
            faces = triangles.faces
            shaders = []

            for face in faces:
                v0, v1, v2 = [vertices[i] for i in face]

                edge1 = v1.subtract_vector(v0)
                edge2 = v2.subtract_vector(v0)
                normal = edge1.cross_product(edge2)
                normal = normal.normalize()

                light_dir = light.position.subtract_vector(v0)
                light_dir = light_dir.normalize()
                light_normal = normal.dot_product(light_dir)

                viewer_dir = viewer_position.subtract_vector(v0)
                viewer_dir = viewer_dir.normalize()

                reflection = normal.multiply(2 * light_normal)
                reflection = reflection.subtract_vector(light_dir)
                reflection = reflection.normalize()

                ambient = light.ambient

                light_clamped = max(0, light_normal)
                diffuse = light.diffuse.multiply(light_clamped)
                shininess = 16

                reflection_perspective = reflection.dot_product(viewer_dir)
                specular_clamped = max(0, reflection_perspective) ** shininess
                specular = light.specular.multiply(specular_clamped)

                shading = ambient.add_vector(diffuse).add_vector(specular)
                shading = shading.clamp(0.0, 1.0)
                shaders.append(shading.to_tuple())
            triangles.shaders = shaders
