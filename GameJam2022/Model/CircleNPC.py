import pygame
import pygame_ai.gameobject
import pygame_ai.steering.kinematic


class CircleNPC(pygame_ai.gameobject.GameObject):

    def __init__(self, pos = (0, 0)):
        #circle image with transparency
        img = pygame.Surface((10, 10)).convert_alpha()
        img.fill((255,255,255,0))

        #draw the circle
        pygame.draw.circle(img, (255,0,250), (5,5),5)

        #GameObject
        super(CircleNPC, self).__init__(
            img_surf=img,
            pos=pos,
            max_speed=25,
            max_accel=40,
            max_rotation=40,
            max_angular_accel=30
        )

        self.ai = pygame_ai.steering.kinematic.NullSteering()

    def update(self, tick):
       steering = self.ai.get_steering()
       self.steer(steering, tick)
       self.rect.move_ip(self.velocity)

