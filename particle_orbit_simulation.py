import turtle
import math

import random
import time

from typing_extensions import Self, NoReturn


class Vector:
    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x = x
        self.y = y

    def get_tuple(self) -> tuple[float, float]:
        return self.x, self.y

    def multiply(self, num: float) -> Self:
        return Vector(self.x * num, self.y * num)

    def divide(self, num: float) -> Self:
        return Vector(self.x / num, self.y / num)

    def add_vector(self, vec: Self) -> Self:
        return Vector(self.x + vec.x, self.y + vec.y)

    def subtract_vector(self, vec: Self) -> Self:
        return Vector(self.x - vec.x, self.y - vec.y)

    def get_length(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def set_magnitude(self, magnitude: float) -> Self:
        length = self.get_length()
        if length != 0:
            self.x = (self.x / length) * magnitude
            self.y = (self.y / length) * magnitude
        return self


class Particle:
    def __init__(self, x: float, y: float) -> None:
        self.position = Vector(x, y)
        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, 0)
        self.mass = 1
        self.size = 1
        self.turtle = turtle.Turtle()
        self.turtle.penup()
        self.turtle.shape("circle")
        self.turtle.shapesize(self.size, self.size)
        self.turtle.color((0.6, 0.6, 0.6))
        self.turtle.goto(self.position.get_tuple())

    def set_mass(self, mass: float) -> Self:
        self.mass = mass
        return self

    def set_shapesize(self, shapesize: tuple[float, float]) -> None:
        self.turtle.shapesize(*shapesize)

    def set_color(self, color: tuple[float, float, float]) -> None:
        self.turtle.pencolor(color)
        self.turtle.fillcolor(color)

    def with_trail(self) -> Self:
        self.turtle.pendown()
        return self

    def random_velocity(self, min_range: float = 0, max_range: float = 1) -> Self:
        self.velocity.x = random.uniform(min_range, max_range)
        self.velocity.y = random.uniform(min_range, max_range)
        return self

    def set_velocity(self, x: float, y: float) -> Self:
        self.velocity.x = x
        self.velocity.y = y
        return self

    def set_acceleration(self, x: float, y: float) -> Self:
        self.acceleration.x = x
        self.acceleration.y = y
        return self

    def update(self) -> Self:
        self.position = self.position.add_vector(self.velocity)
        self.velocity = self.velocity.add_vector(self.acceleration)
        self.acceleration = self.acceleration.multiply(0)
        self.turtle.goto(self.position.get_tuple())
        return self

    @staticmethod
    def constrain(val: float, min_val: float, max_val: float) -> float:
        return min(max_val, max(min_val, val))

    def apply_force(self, force: Vector) -> None:
        force = force.divide(self.mass)
        self.acceleration = self.acceleration.add_vector(force)

    def attraction(self, target: Self) -> None:
        force = target.position.subtract_vector(self.position)
        distance = force.get_length()
        # g_const = 6.67430
        # g_const = 50
        g_const = 0.0005
        strength = g_const * (self.mass * target.mass) / distance
        force = force.set_magnitude(strength)
        self.apply_force(force)


class Simulation:
    def __init__(self) -> None:
        self.particles: list[Particle] = []
        self.turtle_screen = turtle.Screen()
        self.turtle_screen.tracer(0)
        self.turtle_screen.bgcolor((0.1, 0.1, 0.1))
        self.turtle_screen.title("Particle System")
        self.timestep = 0.00001

    def add_center_particle(self) -> None:
        x, y = 0, 0
        p = Particle(x, y)
        p.set_color((0.5, 0.2, 0.2))
        p.set_mass(1_000_000)
        p.set_shapesize((10, 10))
        self.particles.append(p)

    def add_orbiting_particle(self) -> None:
        x, y = random.uniform(-400, -200), random.uniform(-400, -200)
        p = Particle(x, y)
        p.set_shapesize((0.5, 0.5))
        p.set_velocity(5, -10)
        mass = random.uniform(1, 1000)
        p.set_mass(mass)
        p.set_shapesize((mass*0.001, mass*0.001))

        p.with_trail()
        self.particles.append(p)

    def setup_particles(self) -> None:
        self.add_center_particle()
        for _ in range(20):
            self.add_orbiting_particle()
        self.turtle_screen.update()

    def calculate_particle_forces(self) -> None:
        for pl1 in self.particles:
            for pl2 in self.particles:
                if pl1 != pl2:
                    pl1.attraction(pl2)
            pl1.update()

    def timestep_adjustment(self, time_taken: float) -> None:
        self.timestep = time_taken
        print(f"ADJUSTING TIMESTEP TO {self.timestep}")
        self.turtle_screen.update()

    def start_simulation(self) -> NoReturn:
        input("ENTER")
        while True:
            start_time = time.process_time()
            self.calculate_particle_forces()
            time_taken = time.process_time() - start_time
            wait_time = self.timestep - time_taken
            if wait_time < 0:
                self.timestep_adjustment(time_taken)
                continue
            time.sleep(wait_time)
            self.turtle_screen.update()


sim = Simulation()
sim.setup_particles()
sim.start_simulation()
