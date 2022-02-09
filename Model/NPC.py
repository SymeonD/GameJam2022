import pygame
import os



class NPC(pygame.sprite.Sprite):

    def __init__(self, x, y, name):
        super(NPC, self).__init__()
        self.updateImage('Ressources/player.png', 32)
        self.original_image = self.image

        self.damage_image = (self.image.copy()).convert_alpha()
        self.damage_image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        self.damage_image.fill((255, 0, 0), None, pygame.BLEND_RGBA_ADD)

        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.speed = 1

        self.name = name
        self.health = 100
        self.skin = 1
        self.level = 1
        self.hit_countdown = None

    def update(self):
        self.rect.topleft = self.position
        if self.hit_countdown:
            if self.hit_countdown % 2:
                self.image = self.damage_image  # (or other suitable pre-loaded image)
            else:
                self.image = self.original_image
            self.hit_countdown = max(0, self.hit_countdown - 1)

    def change_animation(self, name):
        self.image.set_colorkey((0, 0, 0))
        self.image = self.images[name]

    def get_image(self, x, y):
        image = pygame.Surface([self.sprite_size, self.sprite_size])
        image.blit(self.sprite_sheet, (0, 0), (x, y, self.sprite_size, self.sprite_size))
        return image

    def updateImage(self, ressource, sprite_size):
        self.sprite_size = sprite_size
        self.sprite_sheet = pygame.image.load(ressource)
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.images = {
            'down': self.get_image(0, 0),
            'up': self.get_image(0, 3 * self.sprite_size),
            'right': self.get_image(0, 2 * self.sprite_size),
            'left': self.get_image(0, self.sprite_size)
        }

    def take_damage(self, amount):
        self.health -= amount
        self.hit_countdown = 6
        print(self.health)

