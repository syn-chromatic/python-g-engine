import random

from components.shape import Shape
from components.color import RGBA

from components.vertices import Sphere, Cube, GridHorizontal, MeshConverter
from components.model import OBJModelFormat
from components.light import Light

from pathlib import Path


def get_center_cube(px, py, pz):
    mass = 100
    shape = Cube(50).get_polygons()

    shape = MeshConverter(shape).quads_to_triangles()

    color = RGBA(0.8, 0.3, 0.3, 1.0)

    body = Shape(shape)
    body.set_color(color)
    body.physics.set_mass(mass)
    body.physics.set_position(px, py, pz)
    body.physics.set_spin_velocity(50, 50, 0)
    return body


def get_sphere1():
    position = (400.0, 1100.0, 3100.0)
    mass = 50_000
    light = Light.get_light()
    sphere = Sphere(100, 10, 10)
    sphere.set_offset(*position)
    mesh = sphere.get_triangle_mesh()
    mesh.light = light
    body = Shape(mesh)
    body.physics.set_mass(mass)
    body.physics.set_position(*position)
    body.physics.set_velocity(-200, 0, 0)
    return body


def get_sphere2():
    position = (-400.0, 1100.0, 3100.0)
    mass = 50_000
    light = Light.get_light()
    sphere = Sphere(100, 10, 10)
    sphere.set_offset(*position)
    mesh = sphere.get_triangle_mesh()
    mesh.light = light
    body = Shape(mesh)
    body.physics.set_position(*position)
    body.physics.set_mass(mass)
    body.physics.set_velocity(200, 0, 0)
    return body


def get_cube_t1():
    px = random.uniform(-50, -40)
    py = random.uniform(-50, -40)
    pz = 0

    mass = random.uniform(50, 100)
    scale = mass / 20
    shape = Cube(scale).get_polygons()

    body = Shape(shape)
    # body.physics.set_position(px, py, pz)
    body.physics.set_velocity(10, 30, 5)
    body.physics.set_mass(mass)
    body.physics.set_scale(scale)
    return body


def get_grid():
    mass = 1_000
    grid = GridHorizontal(10, 10, 300)
    grid.set_offset(-1000, -100, -1000)
    polygons = grid.get_triangle_polygons()

    color = RGBA(0.8, 0.3, 0.3, 1.0)

    body = Shape(polygons)
    body.set_color(color)
    body.physics.set_mass(mass)

    return body


def get_obj():
    mass = 10_000_000
    file_path = Path("./cottage2.obj")
    obj = OBJModelFormat(file_path, 0.2)
    obj.set_offset(500, -100, 600)
    polygons = obj.get_polygons()
    color = RGBA(0.8, 0.3, 0.3, 1.0)

    body = Shape(polygons)
    body.set_color(color)
    body.physics.set_mass(mass)
    return body


def get_obj2():
    position = (-400.0, 1100.0, 3100.0)
    mass = 50_000

    file_path = Path("./cottage2.obj")
    obj = OBJModelFormat(file_path, 0.2)
    obj.set_offset(*position)
    mesh = obj.get_polygons()
    color = RGBA(0.8, 0.3, 0.3, 1.0)

    body = Shape(mesh)
    body.set_color(color)
    body.physics.set_position(*position)
    body.physics.set_mass(mass)
    body.physics.set_velocity(1000, 0, 0)
    return body
