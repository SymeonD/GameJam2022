import pygame

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, name):
        super().__init__()
        self.sprite_sheet = pygame.image.load('../Ressources/player.png')
        self.image = self.getImage(0,0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]

        self.name = name;
        self.health = 200;
        self.skin = 1;
        self.inventory = [];

    def update(self):
        self.rect.topleft = self.position

    def getImage(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image


