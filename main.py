from components.graphics import Graphics, GraphicsScreen
from components.simulation import Simulation
# from components.vector_3d import Vector3D


def main():
    graphics = Graphics()
    graphics_screen = GraphicsScreen()

    while True:
        graphics_screen.set_title("Physics System")
        graphics_screen.set_screensize(640, 640)
        graphics_screen.set_background_color(0.15, 0.15, 0.15)

        simulation = Simulation(graphics)
        simulation.setup_objects()
        simulation.start_simulation(graphics_screen)

if __name__ == "__main__":
    main()
