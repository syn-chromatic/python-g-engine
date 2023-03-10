from functools import partial

from components.graphics import Graphics
from components.simulation import Simulation
from components.camera import Camera
from components.color import RGBA


def main():
    width = 640
    height = 640
    background_color = RGBA(0.15, 0.15, 0.15, 1.0)

    graphics = Graphics()
    camera = Camera(width, height)

    graphics.set_title("Physics System")
    graphics.set_screensize(width, height)
    graphics.set_background_color(background_color)

    simulation = Simulation(graphics, camera)
    simulation.setup_objects()
    GraphicsHandler(graphics, simulation)


class GraphicsHandler:
    def __init__(self, graphics: Graphics, simulation: Simulation):
        self.graphics = graphics
        self.simulation = simulation
        self.previous_pointer = graphics.get_pointer_xy()
        self.draw_loop()

    def handle_events(self) -> None:
        self.on_mouse_move()
        self.on_mouse_wheel_scroll()
        self.on_key_down()

    def on_mouse_wheel_scroll(self) -> None:
        pass

    def on_mouse_move(self) -> None:
        px, py = self.previous_pointer
        nx, ny = self.graphics.get_pointer_xy()

        if px != nx or py != ny:
            dx, dy = self.graphics.get_pointer_xy()
            camera = self.simulation.camera
            camera.handle_mouse_movement(dx, dy)

    def on_key_down(self) -> None:
        screen = self.graphics.turtle_screen
        camera = self.simulation.camera

        increase_distance = partial(camera.increment_distance, 1.0)
        decrease_distance = partial(camera.increment_distance, -1.0)

        screen.onkeypress(increase_distance, "w")
        screen.onkeypress(decrease_distance, "s")

    def on_draw(self) -> None:
        self.simulation.simulate(self.graphics)

    def draw_loop(self) -> None:
        while True:
            self.handle_events()
            self.on_draw()


if __name__ == "__main__":
    main()
