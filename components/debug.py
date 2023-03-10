from components.vector_3d import Vector3D
from components.particle import Particle
from components.graphics import Graphics
from components.camera import Camera
from components.color import RGBA


def debug_show_collision_shifts(
    graphics: Graphics, camera: Camera, self_shifted: Vector3D, target_shifted: Vector3D
):

    p1_color = RGBA(0.4, 0.8, 0.4, 1.0)

    p1 = Particle([(0.0, 0.0, 0.0)])
    p1.set_color(p1_color)
    p1.physics.set_scale(3)
    p1.physics.position = self_shifted
    p1.draw(graphics, camera)

    p2_color = RGBA(0.8, 0.4, 0.4, 1.0)

    p2 = Particle([(0.0, 0.0, 0.0)])
    p2.set_color(p2_color)
    p2.physics.set_scale(3)
    p2.physics.position = target_shifted
    p2.draw(graphics, camera)
