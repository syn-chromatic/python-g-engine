from functools import partial

from components.graphics_abc import GraphicsABC
from components.graphics import TurtleGraphics, PygGraphics
from components.simulation import Simulation
from components.camera import Camera
from components.color import RGBA
from components.vertices import Cube, Sphere


def main() -> None:
    width = 1760
    height = 960
    background_color = RGBA(0.15, 0.15, 0.15, 1.0)

    graphics = PygGraphics(width, height)
    camera = Camera(width, height)

    graphics.set_title("Physics System")
    graphics.set_background_color(background_color)

    simulation = Simulation(camera)
    simulation.setup_objects()
    GraphicsHandler(graphics, simulation, camera)


class GraphicsHandler:
    def __init__(self, graphics: GraphicsABC, simulation: Simulation, camera: Camera):
        self.graphics = graphics
        self.simulation = simulation
        self.camera = camera
        self.previous_pointer = graphics.get_pointer_xy()
        self.register_keys()
        self.draw_loop()

    def handle_events(self) -> None:
        self.on_mouse_move()
        self.on_mouse_wheel_scroll()
        self.on_window_resize()

    def register_keys(self) -> None:
        camera = self.simulation.camera
        simulation = self.simulation

        step_val = 10.0

        increase_distance = partial(camera.increment_plane, step_val)
        decrease_distance = partial(camera.increment_plane, -step_val)
        increase_timestep = partial(simulation.increment_timestep, 100)
        decrease_timestep = partial(simulation.increment_timestep, -100)

        move_forward = partial(camera.increment_position_z, step_val)
        move_backward = partial(camera.increment_position_z, -step_val)
        move_right = partial(camera.increment_position_x, step_val)
        move_left = partial(camera.increment_position_x, -step_val)
        move_up = partial(camera.increment_position_y, -step_val)
        move_down = partial(camera.increment_position_y, step_val)

        move_tar_forward = partial(camera.increment_target_z, step_val)
        move_tar_backward = partial(camera.increment_target_z, -step_val)
        move_tar_right = partial(camera.increment_target_x, step_val)
        move_tar_left = partial(camera.increment_target_x, -step_val)
        move_tar_up = partial(camera.increment_target_y, step_val)
        move_tar_down = partial(camera.increment_target_y, -step_val)

        toggle_frustum = partial(camera.toggle_frustum_clipping)

        reset = partial(camera.reset)

        self.graphics.register_onkeypress(move_forward, "w")
        self.graphics.register_onkeypress(move_backward, "s")
        self.graphics.register_onkeypress(move_left, "a")
        self.graphics.register_onkeypress(move_right, "d")


        self.graphics.register_onkeypress(move_up, "Up")
        self.graphics.register_onkeypress(move_down, "Down")
        self.graphics.register_onkeypress(move_tar_right, "Left")
        self.graphics.register_onkeypress(move_tar_left, "Right")
        self.graphics.register_onkeypress(move_tar_up, "k")
        self.graphics.register_onkeypress(move_tar_down, "l")
        self.graphics.register_onkeypress(toggle_frustum, "o", False)

        self.graphics.register_onkeypress(reset, "r", False)
        self.graphics.register_onkeypress(increase_distance, "e")
        self.graphics.register_onkeypress(decrease_distance, "q")
        self.graphics.register_onkeypress(increase_timestep, ".")
        self.graphics.register_onkeypress(decrease_timestep, ",")

    def on_window_resize(self):
        g_width = self.graphics.width
        g_height = self.graphics.height

        width = self.graphics.get_width()
        height = self.graphics.get_height()

        # if g_width != width or g_height != height:
        #     self.graphics.setup_coordinates(width, height)

    def on_mouse_wheel_scroll(self) -> None:
        pass

    def on_mouse_move(self) -> None:
        px, py = self.previous_pointer
        nx, ny = self.graphics.get_pointer_xy()

        if px != nx or py != ny:
            dx, dy = self.graphics.get_pointer_xy()
            camera = self.simulation.camera
            camera.handle_mouse_movement(dx, dy)

    def on_draw(self) -> None:
        self.graphics.clear_screen()
        # sphere_poly = Sphere(50, 10, 10).get_polygons()
        # sphere_poly = self.camera.apply_projection_polygons(sphere_poly)
        # self.graphics.draw_polygons(sphere_poly)

        # cube_poly = Cube(10).get_polygons()
        # cube_poly = self.camera.apply_projection_polygons(cube_poly)
        # self.graphics.draw_polygons(cube_poly)
        self.simulation.simulate(self.graphics)
        self.graphics.update()

    def draw_loop(self) -> None:
        while True:
            self.handle_events()
            self.on_draw()


if __name__ == "__main__":
    main()
