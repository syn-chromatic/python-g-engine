import random

from components.shape import Shape
from components.grid import GridGround
from components.color import RGBA
from components.vertices import SphereShape, CubeShape, ParticleCircle
from components.vertices import Sphere, Cube, GridHorizontal
from components.shared_dcs import Circles, Quads, Triangles, Polygons
from components.model import OBJModelFormat


from pathlib import Path


def get_center_cube(px, py, pz):
    mass = 100
    shape = CubeShape().get_shape()
    color = RGBA(0.8, 0.3, 0.3, 1.0)
    scale = 50

    body = Shape(shape)
    body.set_color(color)
    body.physics.set_mass(mass)
    body.physics.set_scale(scale)
    body.physics.set_position(px, py, pz)
    body.physics.set_spin_velocity(50, 50, 0)
    return body


def quads_to_triangles(polygons: list[Polygons]) -> list[Polygons]:

    for idx, polys in enumerate(polygons):
        polys_type = polys.type

        if isinstance(polys_type, Quads):
            triangle_faces: list[tuple[int, int, int]] = []
            quad_faces = polys_type.faces
            for quad in quad_faces:
                triangle1 = (quad[0], quad[1], quad[2])
                triangle2 = (quad[0], quad[2], quad[3])

                triangle_faces.extend([triangle1, triangle2])
            triangles = Triangles(polys_type.vertices, triangle_faces)
            polygons[idx].type = triangles

    return polygons


def get_center_sphere():
    mass = 10_000_000
    polygons = Sphere(50, 10, 10).get_triangle_polygons()
    # polygons = quads_to_triangles(polygons)

    color = RGBA(0.8, 0.3, 0.3, 1.0)
    scale = mass / 250_000

    body = Shape(polygons)
    body.set_color(color)
    body.physics.set_mass(mass)
    body.physics.set_scale(scale)
    body.physics.set_spin_velocity(50, 50, 0)
    return body


def get_cube_t1():
    px = random.uniform(-50, -40)
    py = random.uniform(-50, -40)
    pz = 0

    mass = random.uniform(50, 100)
    shape = CubeShape().get_shape()
    scale = mass / 20

    body = Shape(shape)
    body.physics.set_position(px, py, pz)
    body.physics.set_velocity(10, 30, 5)
    body.physics.set_mass(mass)
    body.physics.set_scale(scale)
    return body


def get_grid():
    mass = 10_000_000
    polygons = GridHorizontal(10, 10, 20, -50).get_triangle_polygons()
    # polygons = quads_to_triangles(polygons)

    color = RGBA(0.8, 0.3, 0.3, 1.0)
    # scale = mass / 250_000

    body = Shape(polygons)
    body.set_color(color)
    body.physics.set_mass(mass)
    # body.physics.set_scale(scale)
    # body.physics.set_spin_velocity(50, 50, 0)
    return body


def get_tank():
    file_path = Path("./tank_2.obj")
    polygons = OBJModelFormat(file_path).get_polygons()
    color = RGBA(0.8, 0.3, 0.3, 1.0)

    body = Shape(polygons)
    body.set_color(color)
    return body
