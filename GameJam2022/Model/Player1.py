import pygame_ai.gameobject
import pygame

class Player(pygame_ai.gameobject.GameObject, pygame.sprite.Sprite):

    def __init__(self, pos = (0, 0)):
        self.sprite_sheet = pygame.image.load('../Ressources/player.png')
        self.img = self.get_image(0, 0)
        self.img.set_colorkey([0, 0, 0])
        self.images = {
            'down': self.get_image(0, 0),
            'up': self.get_image(0, 96),
            'right': self.get_image(0, 64),
            'left': self.get_image(0, 32)
        }

        #GameObject init
        super(Player, self).__init__(
            img_surf=self.img,
            pos=pos,
            max_speed=15,
            max_accel=40,
            max_rotation=40,
            max_angular_accel=30
        )

    def update(self, steering, tick):
        self.steer(steering, tick)
        self.rect.move_ip(self.velocity)

    def change_animation(self, name):
        self.image.set_colorkey((0,0,0))
        self.image = self.images[name]

    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image