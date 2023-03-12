import time

from components.graphics import Graphics
from components.body import Body
from components.camera import Camera
from components.color import RGBA

from components.body_configurations import (
    get_particle_t3,
    get_particle_t7,
)


class Simulation:
    def __init__(self, camera: Camera) -> None:
        self.camera = camera
        self.fps_txp = (-300, 300)
        self.fps_txc = RGBA(0.8, 0.8, 0.8, 1.0)
        self.objects: list[Body] = []
        self.timestep = 1 / 10_000

    def setup_objects(self) -> None:
        p3 = get_particle_t3()
        p7_list = get_particle_t7(0, 0)
        self.objects.append(p3)
        self.objects.extend(p7_list)

    def compute_all_objects(self, graphics: Graphics) -> None:
        for obj1 in self.objects:
            obj1_physics = obj1.physics
            for obj2 in self.objects:
                if obj1 == obj2:
                    continue
                obj2_physics = obj2.physics
                obj1_physics.apply_forces(obj2_physics, self.timestep)

            obj1_physics.update(self.timestep)
            obj1.draw(graphics, self.camera)

    def timestep_adjustment(self, frame_en: float) -> int:
        self.timestep = frame_en
        return 0

    def write_fps(self, graphics: Graphics, frame_time: float):
        fps = f"{1 / frame_time:.2f} FPS"
        graphics.draw_text(self.fps_txp, self.fps_txc, fps)

    def simulate(self, graphics: Graphics):
        graphics.clear_screen()
        frame_st = time.perf_counter()
        self.compute_all_objects(graphics)
        frame_time = time.perf_counter() - frame_st
        self.write_fps(graphics, frame_time)
