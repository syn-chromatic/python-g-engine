import time
import random

from components.graphics import Graphics, GraphicsScreen
from components.body import Body
from components.shape import Shape
from components.particle import Particle
from components.vertices import CubeShape, SphereShape, ParticleCircle


class Simulation:
    def __init__(self, graphics: Graphics) -> None:
        self.graphics = graphics
        self.fps_txp = (-300, 300)
        self.fps_txc = (0.8, 0.8, 0.8)
        self.objects: list[Body] = []
        self.timestep = 1 / 5_000

    def add_center_cube(self) -> None:
        mass = 10_000_000
        shape = CubeShape().get_shape()
        color = (0.8, 0.3, 0.3)
        scale = mass / 250_000

        p = Shape(shape)
        p.set_color(color)
        p.physics.set_mass(mass)
        p.physics.set_scale(scale)
        p.physics.set_spin_velocity(50, 50, 0)
        self.objects.append(p)

    def add_center_sphere(self) -> None:
        mass = 10_000_000
        shape = SphereShape(10, 10, 10).get_shape()
        color = (0.8, 0.3, 0.3)
        scale = mass / 250_000

        p = Shape(shape)
        p.set_color(color)
        p.physics.set_mass(mass)
        p.physics.set_scale(scale)
        p.physics.set_spin_velocity(50, 50, 0)
        self.objects.append(p)

    def add_cube_t1(self) -> None:
        px = random.uniform(-50, -40)
        py = random.uniform(-50, -40)
        pz = 0

        mass = random.uniform(50, 100)
        shape = CubeShape().get_shape()
        scale = mass / 20

        p = Shape(shape)
        p.physics.set_position(px, py, pz)
        p.physics.set_velocity(10, 30, 5)
        p.physics.set_mass(mass)
        p.physics.set_scale(scale)
        self.objects.append(p)

    def add_particle_t1(self):
        px = 0
        py = 10
        pz = 0

        mass = 30
        shape = [(0.0, 0.0, 0.0)]
        scale = mass

        vx = 1000
        vy = 0

        p = Particle(shape)
        p.physics.set_position(px, py, pz)
        p.physics.set_velocity(vx, vy, 0)
        p.physics.set_mass(mass)
        p.physics.set_scale(scale)
        self.objects.append(p)

    def add_particle_t2(self):
        px = -300
        py = -20
        pz = 0

        mass = 30
        shape = [(0.0, 0.0, 0.0)]
        scale = mass

        vx = 1000
        vy = 0

        p = Particle(shape)
        p.physics.set_position(px, py, pz)
        p.physics.set_velocity(vx, vy, 0)
        p.physics.set_mass(mass)
        p.physics.set_scale(scale)
        self.objects.append(p)

    def add_particle_t3(self):
        px = 150
        py = 10
        pz = 0

        mass = 30
        shape = CubeShape().get_shape()
        scale = mass

        p = Particle(shape)
        p.physics.set_position(px, py, pz)
        p.physics.set_velocity(-10000, 0, 0)
        p.physics.set_mass(mass)
        p.physics.set_scale(scale)
        p.set_color((0.8, 0.2, 0.2))
        self.objects.append(p)

    def add_particle_t4(self, px, py):
        pz = 0

        mass = 30
        shape = [(0.0, 0.0, 0.0)]
        scale = mass

        vx = 500
        vy = 0

        p = Particle(shape)
        p.physics.set_position(px, py, pz)
        p.physics.set_velocity(vx, vy, 0)
        p.physics.set_mass(mass)
        p.physics.set_scale(scale)
        self.objects.append(p)

    def add_particle_t5(self, px, py):
        pz = 0

        mass = 30
        shape = [(0.0, 0.0, 0.0)]
        scale = mass

        vx = -20_000
        vy = 80_000

        p = Particle(shape)
        p.physics.set_position(px, py, pz)
        p.physics.set_velocity(vx, vy, 0)
        p.physics.set_mass(mass)
        p.physics.set_scale(scale)
        self.objects.append(p)

    def add_particle_t6(self) -> None:
        px = random.uniform(-200, -60)
        py = random.uniform(-50, -100)
        pz = 0

        mass = random.uniform(1, 5)
        shape = [(0.0, 0.0, 0.0)]
        scale = mass

        p = Particle(shape)
        p.physics.set_position(px, py, pz)
        p.physics.set_velocity(-10, -30, 0)
        p.physics.set_mass(mass)
        p.physics.set_scale(scale)
        self.objects.append(p)

    def add_particle_t7(self, px: float, py: float) -> None:
        particles = ParticleCircle(20).generate(px, py)

        for particle in particles:
            px = particle[0]
            py = particle[1]
            pz = 0

            mass = particle[2]
            shape = [(0.0, 0.0, 0.0)]
            scale = particle[2]

            p = Particle(shape)
            p.physics.set_position(px, py, pz)
            p.physics.set_velocity(0, 0, 0)
            p.physics.set_mass(mass)
            p.physics.set_scale(scale)
            self.objects.append(p)

    def setup_objects(self) -> None:
        self.add_particle_t3()
        self.add_particle_t7(0, 0)
        self.add_particle_t7(50, 50)

    def compute_all_objects(self) -> None:
        for pl1 in self.objects:
            for pl2 in self.objects:
                if pl1 == pl2:
                    continue
                pl1.physics.apply_forces(pl2.physics, self.timestep)

            pl1.physics.update(self.timestep)
            pl1.draw(self.graphics)

    def timestep_adjustment(self, frame_en: float) -> int:
        self.timestep = frame_en
        return 0

    def write_fps(self, frame_time: float):
        fps = f"{1 / frame_time:.2f} FPS"
        self.graphics.draw_text(self.fps_txp, self.fps_txc, fps)

    def start_simulation(self, graphics_screen: GraphicsScreen):
        while True:
            self.graphics.clear_screen()
            frame_st = time.perf_counter()
            self.compute_all_objects()
            frame_time = time.perf_counter() - frame_st
            self.write_fps(frame_time)
            graphics_screen.update()
