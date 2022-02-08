from NPC import NPC as parent
import pygame


class NPC_Werewolf(parent):

    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        self.sprite_sheet = pygame.image.load('../Ressources/loup Garou.png')
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.images = {
            'down': self.get_image(0, 0),
            'up': self.get_image(0, 240),
            'right': self.get_image(0, 160),
            'left': self.get_image(0, 80)
        }
        self.moonCycle = 1
        self.type = 'speed'

    def change_animation(self, name):
        self.image.set_colorkey((0,0,0))
        self.image = self.images[name]

    def get_image(self, x, y):
        image = pygame.Surface([80, 80])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 80, 80))
        return image
