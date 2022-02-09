import pygame
import os



class NPC(pygame.sprite.Sprite):

    def __init__(self, x, y, name, screen):
        super(NPC, self).__init__()
        self.updateImage('Ressources/player.png', 32)
        self.original_image = self.image

        self.damage_image = (self.image.copy()).convert_alpha()
        self.damage_image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        self.damage_image.fill((255, 0, 0), None, pygame.BLEND_RGBA_ADD)

        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.speed = 1
        self.screen = screen

        self.name = name
        self.health = 100
        self.skin = 1
        self.level = 1
        self.hit_countdown = None

    def update(self):
        self.rect.topleft = self.position
        self.draw_health(self.screen)
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
        if self.health <= 0:
            self.kill()

    def draw_health_bar(self, surface, position, size, color_border, color_background, color_health, progress):
        pygame.draw.rect(surface, color_background, (*position, *size))
        pygame.draw.rect(surface, color_border, (*position, *size), 1)
        innerPos = (position[0] + 1, position[1] + 1)
        innerSize = (int((size[0] - 2) * progress), size[1] - 2)
        pygame.draw.rect(surface, color_health, (*innerPos, *innerSize))

    def draw_health(self, surf):
        health_rect = pygame.Rect(0, 0, self.original_image.get_width(), 7)
        health_rect.midbottom = self.rect.centerx, self.rect.top
        max_health = 100
        self.draw_health_bar(surf, health_rect.topleft, health_rect.size, (0, 0, 0), (255, 0, 0), (0, 255, 0),
                        self.health / max_health)


