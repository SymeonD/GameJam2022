import pygame
import pygame_ai as pai

class NPC(pai.gameobject.GameObject):

    def __init__(self, x, y, name):
        self.sprite_sheet = pygame.image.load('../Ressources/player.png')
        self.image = self.get_image(0,0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.images = {
            'down': self.get_image(0, 0),
            'up': self.get_image(0, 96),
            'right': self.get_image(0, 64),
            'left': self.get_image(0, 32)
        }
        self.speed = 3

        self.name = name
        self.health = 100
        self.skin = 1
        self.level = 1

        # GameObject
        super(NPC, self).__init__(
            img_surf=self.image,
            pos=self.position,
            max_speed=25,
            max_accel=40,
            max_rotation=40,
            max_angular_accel=30
        )

        self.ai = pai.steering.kinematic.NullSteering()

    def update(self, tick):
        steering = self.ai.get_steering()
        self.steer(steering, tick)
        self.rect.move_ip(self.velocity)

    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image