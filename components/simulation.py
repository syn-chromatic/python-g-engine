import time
import random

from components.graphics import Graphics, GraphicsScreen
from components.body import Body
from components.shape import Shape
from components.particle import Particle


class Simulation:
    def __init__(self, graphics: Graphics) -> None:
        self.graphics = graphics
        self.fps_txp = (-300, 300)
        self.fps_txc = (0.8, 0.8, 0.8)
        self.objects: list[Body] = []
        self.timestep = 1 / 1000

    @staticmethod
    def get_cube_shape():
        shape = [
            (-1.0, -1.0, -1.0),
            (1.0, -1.0, -1.0),
            (1.0, 1.0, -1.0),
            (-1.0, 1.0, -1.0),
            (-1.0, -1.0, 1.0),
            (1.0, -1.0, 1.0),
            (1.0, 1.0, 1.0),
            (-1.0, 1.0, 1.0),
        ]
        return shape

    def add_center_cube(self) -> None:
        mass = 10_000_000
        shape = self.get_cube_shape()
        color = (0.8, 0.3, 0.3)
        scale = mass / 250_000

        p = Shape(shape)
        p.set_color(color)
        p.physics.set_mass(mass)
        p.physics.set_scale(scale)
        p.physics.set_spin_velocity(0, 0, 0)
        self.objects.append(p)

    def add_orbiting_cube(self) -> None:
        x = random.uniform(-50, -40)
        y = random.uniform(-50, -40)
        z = 0

        mass = random.uniform(50, 100)
        shape = self.get_cube_shape()
        scale = mass / 20

        p = Shape(shape)
        p.physics.set_position(x, y, z)
        p.physics.set_velocity(10, 30, 5)
        p.physics.set_mass(mass)
        p.physics.set_scale(scale)
        self.objects.append(p)

    def add_orbiting_particle(self) -> None:
        x = random.uniform(-200, -60)
        y = random.uniform(-50, -100)
        z = 0

        mass = random.uniform(1, 5)
        shape = [(0.0, 0.0, 0.0)]
        scale = mass

        p = Particle(shape)
        p.physics.set_position(x, y, z)
        p.physics.set_velocity(-10, -30, 0)
        p.physics.set_mass(mass)
        p.physics.set_scale(scale)
        self.objects.append(p)

    def add_particle_right(self):
        x = 0
        y = 10
        z = 0

        mass = 30
        shape = [(0.0, 0.0, 0.0)]
        scale = mass

        vx = 1000
        vy = 0

        p = Particle(shape)
        p.physics.set_position(x, y, z)
        p.physics.set_velocity(vx, vy, 0)
        p.physics.set_mass(mass)
        p.physics.set_scale(scale)
        p.physics.name = "WHITE BALL"
        self.objects.append(p)

    def add_particle_right2(self):
        x = -300
        y = -20
        z = 0

        mass = 30
        shape = [(0.0, 0.0, 0.0)]
        scale = mass

        vx = 1000
        vy = 0

        p = Particle(shape)
        p.physics.set_position(x, y, z)
        p.physics.set_velocity(vx, vy, 0)
        p.physics.set_mass(mass)
        p.physics.set_scale(scale)
        p.physics.name = "WHITE BALL"
        self.objects.append(p)

    def add_particle_left(self):
        x = 300
        y = 10
        z = 0

        mass = 30
        # shape = [(0.0, 0.0, 0.0)}
        shape = self.get_cube_shape()
        scale = mass

        p = Particle(shape)
        p.physics.set_position(x, y, z)
        p.physics.set_velocity(-10000, 0, 0)
        # p.physics.set_spin_velocity(0, 1000, 0)
        p.physics.set_mass(mass)
        p.physics.set_scale(scale)
        p.set_color((0.8, 0.2, 0.2))
        p.physics.name = "RED BALL"
        self.objects.append(p)

    def add_ball(self, x, y):
        z = 0

        mass = 30
        shape = [(0.0, 0.0, 0.0)]
        scale = mass

        vx = 500
        vy = 0

        p = Particle(shape)
        p.physics.set_position(x, y, z)
        p.physics.set_velocity(vx, vy, 0)
        p.physics.set_mass(mass)
        p.physics.set_scale(scale)
        p.physics.name = "WHITE BALL"
        self.objects.append(p)

    def add_ball2(self, x, y):
        z = 0

        mass = 30
        shape = [(0.0, 0.0, 0.0)]
        scale = mass

        vx = -10_000
        vy = 40_000

        p = Particle(shape)
        p.physics.set_position(x, y, z)
        p.physics.set_velocity(vx, vy, 0)
        p.physics.set_mass(mass)
        p.physics.set_scale(scale)
        p.physics.name = "WHITE BALL"
        self.objects.append(p)

    def setup_objects(self) -> None:
        # self.add_center_cube()

        # for _ in range(15):
        self.add_particle_right()
        self.add_particle_right2()
        self.add_particle_left()
        self.add_ball(-200, 20)
        self.add_ball2(10, -500)

        # for _ in range(15):
        #     self.add_orbiting_cube()

        for _ in range(50):
            self.add_orbiting_particle()

    def compute_all_objects(self) -> None:
        for pl1 in self.objects:
            for pl2 in self.objects:
                if pl1 == pl2:
                    continue
                pl1.physics.apply_forces(pl2.physics, self.timestep, self.graphics)

            pl1.physics.move_object(self.timestep)
            pl1.draw_shape(self.graphics)

    def timestep_adjustment(self, frame_en: float) -> int:
        self.timestep = frame_en
        return 0

    def write_fps(self, frame_time: float):
        fps = f"{1 / frame_time:.2f} FPS"
        self.graphics.draw_text(self.fps_txp, self.fps_txc, fps)

    def start_simulation(self, graphics_screen: GraphicsScreen):
        counter = 0

        while counter < 100:

            self.graphics.clear_screen()
            frame_st = time.perf_counter()
            self.compute_all_objects()
            frame_time = time.perf_counter() - frame_st
            self.write_fps(frame_time)

            graphics_screen.update()
            time.sleep(0.05)
            counter += 1
            if counter == 1:
                input()
