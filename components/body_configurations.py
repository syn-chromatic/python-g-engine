import random

from components.shape import Shape
from components.color import RGBA

from components.vertices import Sphere, Cube, GridHorizontal
from components.model import OBJModelFormat


from pathlib import Path


def get_center_cube(px, py, pz):
    mass = 100
    shape = Cube(50).get_polygons()
    color = RGBA(0.8, 0.3, 0.3, 1.0)

    body = Shape(shape)
    body.set_color(color)
    body.physics.set_mass(mass)
    body.physics.set_position(px, py, pz)
    body.physics.set_spin_velocity(50, 50, 0)
    return body


def get_center_sphere():
    mass = 10_000_000
    polygons = Sphere(50, 10, 10).get_triangle_polygons()

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
    scale = mass / 20
    shape = Cube(scale).get_polygons()

    body = Shape(shape)
    body.physics.set_position(px, py, pz)
    body.physics.set_velocity(10, 30, 5)
    body.physics.set_mass(mass)
    body.physics.set_scale(scale)
    return body


def get_grid():
    mass = 10_000_000
    grid = GridHorizontal(15, 15, 100)
    grid.set_offset(-1000, -100, -1000)
    polygons = grid.get_triangle_polygons()
    color = RGBA(0.8, 0.3, 0.3, 1.0)

    body = Shape(polygons)
    body.set_color(color)
    body.physics.set_mass(mass)

    return body


def get_tank():
    file_path = Path("./tank_2.obj")
    polygons = OBJModelFormat(file_path).get_polygons()
    color = RGBA(0.8, 0.3, 0.3, 1.0)

    body = Shape(polygons)
    body.set_color(color)
    return body
