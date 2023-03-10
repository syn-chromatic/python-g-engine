from components.vector_3d import Vector3D
from components.particle import Particle
from components.graphics import Graphics
from components.camera import Camera


def debug_show_collision_shifts(
    graphics: Graphics, camera: Camera, self_shifted: Vector3D, target_shifted: Vector3D
):
    p1 = Particle([(0.0, 0.0, 0.0)])
    p1.set_color((0.4, 0.8, 0.4))
    p1.physics.set_scale(3)
    p1.physics.position = self_shifted
    p1.draw(graphics, camera)

    p2 = Particle([(0.0, 0.0, 0.0)])
    p2.set_color((0.8, 0.4, 0.4))
    p2.physics.set_scale(3)
    p2.physics.position = target_shifted
    p2.draw(graphics, camera)
