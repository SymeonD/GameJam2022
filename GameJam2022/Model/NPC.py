import pygame
import pygame_ai as pai

class NPC(pai.gameobject.GameObject):

    def __init__(self, x, y, name):
        self.updateImage('../Ressources/player.png', 32)
        self.speed = 3

        self.rect = self.image.get_rect()
        self.position = [x, y]

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

    def change_animation(self, name):
        self.image.set_colorkey((0,0,0))
        self.image = self.images[name]

    def get_image(self, x, y):
        image = pygame.Surface([self.sprite_size, self.sprite_size])
        image.blit(self.sprite_sheet, (0, 0), (x, y, self.sprite_size, self.sprite_size))
        return image

    def updateImage(self, ressource, sprite_size):
        self.sprite_sheet = pygame.image.load(ressource)
        self.sprite_size = sprite_size
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.images = {
            'down': self.get_image(0, 0),
            'up': self.get_image(0, 3 * self.sprite_size),
            'right': self.get_image(0, 2 * self.sprite_size),
            'left': self.get_image(0, self.sprite_size)
        }