from functools import partial

from components.graphics import Graphics
from components.simulation import Simulation
from components.camera import Camera
from components.color import RGBA


def main():
    width = 1200
    height = 800
    background_color = RGBA(0.15, 0.15, 0.15, 1.0)

    graphics = Graphics(width, height)
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

        increase_distance = partial(camera.increment_distance, 1.0)
        decrease_distance = partial(camera.increment_distance, -1.0)
        increase_timestep = partial(simulation.increment_timestep, 100)
        decrease_timestep = partial(simulation.increment_timestep, -100)

        screen.onkeypress(increase_distance, "w")
        screen.onkeypress(decrease_distance, "s")
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
