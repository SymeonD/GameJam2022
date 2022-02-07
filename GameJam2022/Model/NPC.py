import pygame

class NPC(pygame.sprite.Sprite):

    def __init__(self, x, y, name):
        super().__init__()
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

    def update(self):
        self.rect.topleft = self.position

    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image