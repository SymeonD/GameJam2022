from NPC import NPC as parent
import pygame


class NPC_Werewolf(parent):

    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        self.updateImage('../Ressources/player.png', 32)
        self.moonCycle = 1
        self.type = 'speed'

    def change_animation(self, name):
        self.image.set_colorkey((0,0,0))
        self.image = self.images[name]

    def get_image(self, x, y):
        image = pygame.Surface([self.sprite_size, self.sprite_size])
        image.blit(self.sprite_sheet, (0, 0), (x, y, self.sprite_size, self.sprite_size))
        return image

    def transform(self, cycleMoon):
        if cycleMoon >= self.moonCycle:
            self.updateImage('../Ressources/loup Garou.png', 80)
