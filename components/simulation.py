import time

from components.graphics import Graphics
from components.body import Body
from components.camera import Camera
from components.color import RGBA
from components.text_writer import TextWriter, FontConfiguration

from components.body_configurations import (
    get_particle_t3,
    get_particle_t7,
)


class Simulation:
    def __init__(self, camera: Camera) -> None:
        self.camera = camera
        self.text_writer = self.create_text_writer()
        self.objects: list[Body] = []
        self.timestep_hz = 10_000

    @staticmethod
    def create_text_writer() -> TextWriter:
        font = FontConfiguration(
            font_type="Arial",
            font_size=11,
            font_style="normal",
            font_color=RGBA.from_rgb_tuple((0.8, 0.8, 0.8)),
            line_height=1.8,
            padding_percent=2,
        )

        text_writer = TextWriter(font)
        return text_writer

    def increment_timestep(self, increment: int):
        if (self.timestep_hz + increment) > 1:
            self.timestep_hz += increment

    def setup_objects(self) -> None:
        p3 = get_particle_t3()
        p7_list = get_particle_t7(0, 0)
        self.objects.append(p3)
        self.objects.extend(p7_list)

    def compute_all_objects(self, graphics: Graphics) -> float:
        frame_st = time.perf_counter()
        timestep = 1.0 / self.timestep_hz

        for obj1 in self.objects:
            obj1_physics = obj1.physics
            for obj2 in self.objects:
                if obj1 == obj2:
                    continue
                obj2_physics = obj2.physics
                obj1_physics.apply_forces(obj2_physics, timestep)

            obj1_physics.update(timestep)
            obj1.draw(graphics, self.camera)
        frame_time = time.perf_counter() - frame_st
        return frame_time

    def write_fps_text(self, frame_time: float):
        text = f"{1 / frame_time:.2f} FPS"
        self.text_writer.add_text_top_left(text)

    def write_timestep_text(self):
        khz = self.timestep_hz / 1000.0
        text = f"Timestep: {khz} khz"
        self.text_writer.add_text_top_left(text)

    def write_object_count(self):
        object_count = len(self.objects)
        text = f"Objects: {object_count}"
        self.text_writer.add_text_top_left(text)

    def draw_text(self, graphics: Graphics):
        self.text_writer.draw(graphics)

    def simulate(self, graphics: Graphics):
        frame_time = self.compute_all_objects(graphics)

        self.write_fps_text(frame_time)
        self.write_timestep_text()
        self.write_object_count()
        self.draw_text(graphics)
