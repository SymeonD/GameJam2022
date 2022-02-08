import pygame


class NPC(pygame.sprite.Sprite):

    def __init__(self, x, y, name):
        super(NPC, self).__init__()
        self.updateImage('../Ressources/player.png', 32)

        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.speed = 1

        self.name = name
        self.health = 100
        self.skin = 1
        self.level = 1

    def update(self):
        self.rect.topleft = self.position

        """
        steering = self.ai.get_steering()
        if steering.linear[1] < 0 :
            self.change_animation('up')
        else :
            self.change_animation('down')
        if steering.linear[0] < 0 and (steering.linear[1] < 20 and steering.linear[1] > -20):
            self.change_animation('left')
        elif steering.linear[0] > 0 and (steering.linear[1] < 20 and steering.linear[1] > -20):
            self.change_animation('right')
        if steering.linear[0] == 0 or steering.linear[0] == 0:
            self.change_animation('down')
        self.steer(steering, tick)
        self.rect.move_ip(self.velocity)
        """

    def change_animation(self, name):
        self.image.set_colorkey((0,0,0))
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

