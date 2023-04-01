from components.vectors import Vector3D
from components.polygons import Mesh, Triangle, Quad
from components.color import RGBA
from components.light import Light
import math


class Shaders:
    def __init__(self):
        self.roughness = 0.2
        self.metallic = 0.8
        self.k_s = self.metallic
        self.k_d = 1.0 - self.k_s
        self.f0 = 0.04
        self.constant_attenuation = 1.0
        self.linear_attenuation = 0.09
        self.quadratic_attenuation = 0.032

    def get_attenuation(self, distance: float):
        attenuation_denom = (
            self.constant_attenuation
            + self.linear_attenuation * distance
            + self.quadratic_attenuation * (distance**2)
        )
        attenuation = 1.0 / attenuation_denom
        return attenuation

    def get_pbr_shader(
        self, light: Light, triangle: Triangle, viewer_position: Vector3D
    ) -> Vector3D:
        light_dir = light.target.subtract_vector(light.position)
        light_dir = light_dir.normalize()

        vertices = triangle.vertices
        v0 = vertices[0]
        v1 = vertices[1]
        v2 = vertices[2]

        centroid = v0.add_vector(v1).add_vector(v2).divide(3.0)

        edge1 = v1.subtract_vector(v0)
        edge2 = v2.subtract_vector(v0)
        normal = edge1.cross_product(edge2)
        normal = normal.normalize()

        distance_vector = centroid.subtract_vector(light.position)
        distance = distance_vector.get_length()
        distance_vector = distance_vector.normalize()

        light_intensity = light.lumens / (distance**2)
        light_dir = light_dir.multiply(distance_vector.dot_product(light_dir))
        light_dir = light_dir.multiply(-1.0)

        viewer_dir = viewer_position.subtract_vector(centroid)
        viewer_dir = viewer_dir.normalize()

        halfway = light_dir.add_vector(viewer_dir)
        halfway = halfway.normalize()

        diffuse_angle = normal.dot_product(light_dir)
        diffuse_angle = max(0.0, diffuse_angle)
        n_dot_v = max(0.0, normal.dot_product(viewer_dir))
        n_dot_l = max(0.0, normal.dot_product(light_dir))
        n_dot_h = max(0.0, normal.dot_product(halfway))

        roughness_sq = self.roughness**2
        n_dot_vsq = n_dot_v * n_dot_v
        n_dot_lsq = n_dot_l * n_dot_l
        n_dot_hsq = n_dot_h * n_dot_h

        g1_denom = n_dot_v + math.sqrt((1.0 - roughness_sq) * n_dot_vsq + roughness_sq)
        g2_denom = n_dot_l + math.sqrt((1.0 - roughness_sq) * n_dot_lsq + roughness_sq)

        g1 = 2.0 * n_dot_v / g1_denom
        g2 = 2.0 * n_dot_l / g2_denom

        attenuation = self.get_attenuation(distance)

        ambient = light.ambient.multiply(light.lumens).multiply(light_intensity)
        diffuse_mult = diffuse_angle * light.lumens * attenuation
        diffuse = light.diffuse.multiply(diffuse_mult).multiply(light_intensity)

        roughness_sq_intr = roughness_sq - 1.0

        d_denom = (n_dot_hsq * roughness_sq_intr + 1.0) ** 2

        f = self.f0 + (1.0 - self.f0) * (1.0 - n_dot_h) ** 5
        g = g1 * g2
        d = roughness_sq / d_denom

        specular_mult = f * g * d * light_intensity * attenuation
        specular_mult_denom = 4.0 * n_dot_l * n_dot_v + 0.000001

        specular = light.specular.multiply(specular_mult / specular_mult_denom)
        shader_vec = ambient.multiply(self.k_d)
        shader_vec = shader_vec.add_vector(diffuse.multiply(self.k_d))
        shader_vec = shader_vec.add_vector(specular.multiply(self.k_s))
        return shader_vec

    def apply_pbr_lighting(self, mesh: Mesh, light: Light, viewer_position: Vector3D):
        light_dir = light.target.subtract_vector(light.position)
        light_dir = light_dir.normalize()

        for polygon in mesh.polygons:
            if isinstance(polygon.shape, Quad):
                continue

            triangle = polygon.shape
            shader_vec = self.get_pbr_shader(light, triangle, viewer_position)
            shader = RGBA.from_vector(shader_vec)
            triangle.shader = triangle.shader.average(shader)

    @staticmethod
    def apply_lighting(mesh: Mesh, light: Light, viewer_position: Vector3D) -> None:
        for polygon in mesh.polygons:
            if isinstance(polygon.shape, Quad):
                continue

            triangle = polygon.shape
            vertices = triangle.vertices
            v0, v1, v2 = vertices

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
            shader = RGBA.from_vector(shading)
            triangle.shader = triangle.shader.average(shader)
