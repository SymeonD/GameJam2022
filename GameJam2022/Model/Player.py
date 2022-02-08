import pygame_ai.gameobject
import pygame
import inventory


class Player(pygame_ai.gameobject.GameObject, pygame.sprite.Sprite):

    def __init__(self, pos=(0, 0)):
        self.sprite_sheet = pygame.image.load('../Ressources/player.png')
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = pos
        self.images = {
            'down': self.get_image(0, 0),
            'up': self.get_image(0, 96),
            'right': self.get_image(0, 64),
            'left': self.get_image(0, 32)
        }

        self.name = "player"
        self.health = 200
        self.skin = 1
        self.inventory = inventory.Inventory()

        # GameObject init
        super(Player, self).__init__(
            img_surf=self.image,
            pos=self.position,
            max_speed=15,
            max_accel=40,
            max_rotation=40,
            max_angular_accel=30
        )

    def update(self, steering, tick):
        self.steer(steering, tick)
        self.rect.move_ip(self.velocity)

    def change_animation(self, name):
        self.image.set_colorkey((0, 0, 0))
        self.image = self.images[name]

    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image
