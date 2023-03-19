from functools import partial

from components.graphics import Graphics
from components.simulation import Simulation
from components.camera import Camera
from components.color import RGBA


def main() -> None:
    width = 1200
    height = 800
    background_color = RGBA(0.15, 0.15, 0.15, 1.0)

    graphics = Graphics(width, height)
    graphics.update()
    camera = Camera(width, height)

    graphics.set_title("Physics System")
    graphics.set_background_color(background_color)

    simulation = Simulation(camera)
    simulation.setup_objects()
    GraphicsHandler(graphics, simulation)


class GraphicsHandler:
    def __init__(self, graphics: Graphics, simulation: Simulation):
        self.graphics = graphics
        self.simulation = simulation
        self.previous_pointer = graphics.get_pointer_xy()
        self.register_keys()
        self.draw_loop()

    def handle_events(self) -> None:
        self.on_mouse_move()
        self.on_mouse_wheel_scroll()
        self.on_window_resize()

    def register_keys(self) -> None:
        screen = self.graphics.screen
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
        move_up = partial(camera.increment_position_y, step_val)
        move_down = partial(camera.increment_position_y, -step_val)

        move_tar_forward = partial(camera.increment_target_z, step_val)
        move_tar_backward = partial(camera.increment_target_z, -step_val)
        move_tar_right = partial(camera.increment_target_x, step_val)
        move_tar_left = partial(camera.increment_target_x, -step_val)
        move_tar_up = partial(camera.increment_target_y, step_val)
        move_tar_down = partial(camera.increment_target_y, -step_val)

        reset = partial(camera.reset)

        screen.onkeypress(move_forward, "w")
        screen.onkeypress(move_backward, "s")
        screen.onkeypress(move_left, "a")
        screen.onkeypress(move_right, "d")
        screen.onkeypress(move_up, "f")
        screen.onkeypress(move_down, "g")

        screen.onkeypress(move_tar_forward, "Up")
        screen.onkeypress(move_tar_backward, "Down")
        screen.onkeypress(move_tar_right, "Left")
        screen.onkeypress(move_tar_left, "Right")
        screen.onkeypress(move_tar_up, "k")
        screen.onkeypress(move_tar_down, "l")

        screen.onkeypress(reset, "r")
        screen.onkeypress(increase_distance, "e")
        screen.onkeypress(decrease_distance, "q")
        screen.onkeypress(increase_timestep, ".")
        screen.onkeypress(decrease_timestep, ",")

    def on_window_resize(self):
        g_width = self.graphics.width
        g_height = self.graphics.height

        width = self.graphics.get_width()
        height = self.graphics.get_height()

        if g_width != width or g_height != height:
            self.graphics.setup_coordinates(width, height)

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
        self.simulation.simulate(self.graphics)
        self.graphics.update()

    def draw_loop(self) -> None:
        while True:
            self.handle_events()
            self.on_draw()


if __name__ == "__main__":
    main()
