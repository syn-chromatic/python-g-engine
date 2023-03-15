import time

from components.graphics import Graphics
from components.body import Body
from components.camera import Camera
from components.color import RGBA
from components.text_writer import TextWriter, FontConfiguration

from components.body_configurations import (
    get_particle_t3,
    get_particle_t7,
    get_particle_t4,
    get_particle_t5,
    get_center_particle,
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

    def setup_objects(self):
        # self.timestep_hz = 5
        p7_list = get_particle_t7(200, 0)
        self.objects.extend(p7_list)

        c1 = get_center_particle()
        self.objects.append(c1)

    # def setup_objects(self):
    #     self.timestep_hz = 1000
    #     p4 = get_particle_t4(-50, 0)
    #     p5 = get_particle_t5(50, 0)
    #     self.objects.append(p4)
    #     self.objects.append(p5)

    # def setup_objects(self) -> None:
    #     p3 = get_particle_t3()
    #     p7_list = get_particle_t7(0, 0)
    #     self.objects.append(p3)
    #     self.objects.extend(p7_list)

    def compute_all_objects(self, graphics: Graphics) -> float:
        frame_st = time.perf_counter()
        timestep = 1.0 / self.timestep_hz

        for idx1, obj1 in enumerate(self.objects):
            obj1_physics = obj1.physics
            for idx2, obj2 in enumerate(self.objects):
                if obj1 == obj2:
                    continue
                obj2_physics = obj2.physics
                p_props = obj1_physics.apply_forces(obj2_physics, timestep)
                p_props_collision = p_props.collision
                if p_props_collision:
                    if (
                        obj1_physics.temperature > obj1_physics.melting_point
                        and obj2_physics.temperature > obj2_physics.melting_point
                    ):
                        if obj1_physics.mass > obj2_physics.mass:
                            self.objects.pop(idx2)
                            obj1_physics.scale += obj2_physics.scale
                            obj1_physics.mass += obj2_physics.mass
                        else:
                            self.objects.pop(idx1)
                            obj2_physics.scale += obj1_physics.scale
                            obj2_physics.mass += obj1_physics.mass
                            continue

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

    def write_camera_information(self):
        camera = self.camera

        info_header = "Camera Information"
        fov = f"FOV: {camera._fov}"
        near_plane = f"Near Plane: {camera._near_plane}"
        far_plane = f"Far Plane: {camera._far_plane}"
        yaw = f"Yaw: {camera._yaw}"
        pitch = f"Pitch: {camera._pitch}"

        self.text_writer.add_text_top_left("")
        self.text_writer.add_text_top_left(info_header)
        self.text_writer.add_text_top_left(fov)
        self.text_writer.add_text_top_left(near_plane)
        self.text_writer.add_text_top_left(far_plane)
        self.text_writer.add_text_top_left(yaw)
        self.text_writer.add_text_top_left(pitch)

    def draw_text(self, graphics: Graphics):
        self.text_writer.draw(graphics)

    def simulate(self, graphics: Graphics):
        frame_time = self.compute_all_objects(graphics)

        self.write_fps_text(frame_time)
        self.write_timestep_text()
        self.write_object_count()
        self.write_camera_information()
        self.draw_text(graphics)
