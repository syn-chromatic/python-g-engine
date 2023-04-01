import random

from abstracts.graphics_abc import GraphicsABC
from components.color import RGBA
from components.physics import Physics
from components.font import FontSettings, ArialFontNormal, ArialFontBold
from components.text_writer import TextWriter
from components.draw_call import DrawCall
from shared_dcs import FrameTime

from pathlib import Path

import configurations.body_configurations as body_configurations


class Simulation:
    def __init__(self, draw_call: DrawCall) -> None:
        self.draw_call = draw_call
        self.text_writer = self.create_text_writer()
        self.timestep_hz = 1

    @staticmethod
    def get_header_font():
        font_type = ArialFontBold()
        font_color = RGBA.from_rgb_tuple((0.8, 0.8, 0.8))

        font = FontSettings(
            font_type=font_type,
            font_size=10,
            font_color=font_color,
            line_height=1.8,
            padding_percent=1,
        )
        return font

    @staticmethod
    def get_standard_font():
        font_type = ArialFontNormal()
        font_color = RGBA.from_rgb_tuple((0.8, 0.8, 0.8))

        font = FontSettings(
            font_type=font_type,
            font_size=10,
            font_color=font_color,
            line_height=1.8,
            padding_percent=1,
        )
        return font

    def create_text_writer(self) -> TextWriter:
        font = self.get_standard_font()
        text_writer = TextWriter(font)
        return text_writer

    def increment_timestep(self, increment: int):
        if (self.timestep_hz + increment) > 1:
            self.timestep_hz += increment

    def setup_objects_cubes(self):
        for _ in range(10):
            x = random.uniform(0, 1000)
            y = 0
            z = random.uniform(0, 1000)

            cube = body_configurations.get_center_cube(x, y, z)
            self.draw_call.add_object(cube)

    def setup_objects(self) -> None:

        grid = body_configurations.get_grid()
        self.draw_call.add_object(grid)

        # self.setup_objects_cubes()
        # obj = body_configurations.get_obj_from_file(Path("./male.obj"))
        # self.draw_call.add_object(obj)

        obj = body_configurations.get_obj()
        self.draw_call.add_object(obj)

        sphere = body_configurations.get_sphere1()
        self.draw_call.add_object(sphere)

        # sphere = body_configurations.get_sphere2()
        # self.draw_call.add_object(sphere)

        # sphere = body_configurations.get_sphere3()
        # self.draw_call.add_object(sphere)

        # obj = body_configurations.get_obj2()
        # self.draw_call.add_object(obj)

    def handle_physics(
        self, obj1_physics: Physics, obj2_physics: Physics, idx1: int, idx2: int
    ):
        timestep = 1.0 / self.timestep_hz

        p_props = obj1_physics.apply_forces(obj2_physics, timestep)
        p_props_collision = p_props.collision
        # if p_props_collision:
        #     if (
        #         obj1_physics.temperature > obj1_physics.melting_point
        #         and obj2_physics.temperature > obj2_physics.melting_point
        #     ):
        #         if obj1_physics.mass > obj2_physics.mass:
        #             self.objects.pop(idx2)
        #             obj1_physics.scale += obj2_physics.scale
        #             obj1_physics.mass += obj2_physics.mass
        #         else:
        #             self.objects.pop(idx1)
        #             obj2_physics.scale += obj1_physics.scale
        #             obj2_physics.mass += obj1_physics.mass
        #             continue

    def compute_all_objects(self):
        # objects = self.draw_call.objects
        # timestep = 1.0 / self.timestep_hz

        # for obj1 in objects:
        #     obj1_physics = obj1.physics
        #     for obj2 in objects:
        #         if obj1 == obj2:
        #             continue
        #         obj2_physics = obj2.physics
        #         obj1_physics.apply_forces(obj2_physics, timestep)
        #     obj1_physics.update(timestep)

        self.draw_call.draw()

    def write_fps_text(self, frametime: FrameTime):
        header_font = self.get_header_font()
        header_text = "Simulation Information"
        text_average = f"Average: {frametime.average_fps:.2f} FPS"

        self.text_writer.add_text_top_left(header_text, header_font)
        self.text_writer.add_text_top_left(text_average)

    def write_timestep_text(self):
        khz = self.timestep_hz / 1000.0
        text = f"Timestep:  {khz} khz"
        self.text_writer.add_text_top_left(text)

    def write_object_count(self):
        object_count = len(self.draw_call.objects)
        text = f"Objects:  {object_count}"
        self.text_writer.add_text_top_left(text)

    def write_camera_information(self):
        camera = self.draw_call.camera
        cp = camera.camera_position
        clt = camera.camera_target
        cld = camera.look_direction
        clu = camera.up_direction
        cls = camera.side_direction

        header_font = self.get_header_font()

        info_header = "Camera Information"
        fov = f"FOV:  {camera.frustum.fov}"
        near_plane = f"Near Plane:  {camera.frustum.near_plane}"
        far_plane = f"Far Plane:  {camera.frustum.far_plane}"
        yaw = f"Yaw:  {camera.yaw:.2f}"
        pitch = f"Pitch:  {camera.pitch:.2f}"
        position = f"Position:  {cp.__str__()}"
        target = f"Target:  {clt.__str__()}"
        look_dir = f"Look (d):  {cld.__str__()}"
        up_dir = f"Up (d):  {clu.__str__()}"
        side_dir = f"Side (d):  {cls.__str__()}"

        self.text_writer.add_text_top_left("")
        self.text_writer.add_text_top_left(info_header, header_font)
        self.text_writer.add_text_top_left(fov)
        self.text_writer.add_text_top_left(near_plane)
        self.text_writer.add_text_top_left(far_plane)
        self.text_writer.add_text_top_left(yaw)
        self.text_writer.add_text_top_left(pitch)
        self.text_writer.add_text_top_left(position)
        self.text_writer.add_text_top_left(target)
        self.text_writer.add_text_top_left(look_dir)
        self.text_writer.add_text_top_left(up_dir)
        self.text_writer.add_text_top_left(side_dir)

    def draw_text(self, graphics: GraphicsABC):
        self.text_writer.draw(graphics)

    def simulate(self, graphics: GraphicsABC, frametime: FrameTime):
        self.compute_all_objects()

        self.write_fps_text(frametime)
        self.write_timestep_text()
        self.write_object_count()
        self.write_camera_information()
        self.draw_text(graphics)
