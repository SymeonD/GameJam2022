import pygame
import os
import math

from Model.inventory import Inventory


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, screen):
        super(Player, self).__init__()
        self.sprite_sheet = pygame.image.load('Ressources/perso/player.png')
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.images = {
            'down': self.get_image(0, 0),
            'up': self.get_image(0, 96),
            'right': self.get_image(0, 64),
            'left': self.get_image(0, 32)
        }
        self.old_position = self.position.copy()
        self.speed = 3
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)

        self.screen = screen

        self.name = "player"
        self.health = 200
        self.skin = 1
        self.inventory = Inventory()
        self.weapon = "sword"
        self.weapon_damage = 20

    def get(self):
        self.image = self.images["down"]
        self.image.set_colorkey([0, 0, 0])
        return self.image

    def save_location(self):
        self.old_position = self.position.copy()

    def move_player(self, type):
        self.image = self.images[type]
        self.image.set_colorkey([0, 0, 0])
        if type == "up":
            self.position[1] -= self.speed
        elif type == "down":
            self.position[1] += self.speed
        elif type == "right":
            self.position[0] += self.speed
        elif type == "left":
            self.position[0] -= self.speed

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        # Update health bar
        pygame.draw.rect(self.screen, (255, 255, 255), (50, 698, 200, 20), 3)
        pygame.draw.rect(self.screen, (255, 0, 0), (50, 698, 200, 20))
        self.health_bar_green = pygame.draw.rect(self.screen, (0, 255, 0), (50, 698, self.health, 20))

    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image

    def move_back(self):
        self.position = self.old_position
        self.update()

    def damage(self, amount, xEnnemy, yEnnemy):
        self.health -= amount
        jump_back = 10
        if self.position[0] - xEnnemy < 0:
            self.position[0] -= self.speed * jump_back
        if self.position[0] - xEnnemy > 0:
            self.position[0] += self.speed * jump_back
        if self.position[1] - yEnnemy < 0:
            self.position[1] -= self.speed * jump_back
        if self.position[1] - yEnnemy > 0:
            self.position[1] += self.speed * jump_back
        if self.health <= 0:
            print("Game Over")
        self.update()

    def attack(self, werewolf):
        werewolf_distance = math.hypot(self.position[0] - werewolf.position[0],
                                       self.position[1] - werewolf.position[1])
        if werewolf_distance < 100:
            werewolf.take_damage(self.weapon_damage)
