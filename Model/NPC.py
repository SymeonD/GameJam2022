import pygame
import os
from Model import item
import random
from pygame import mixer



class NPC(pygame.sprite.Sprite):

    def __init__(self, x, y, name, screen, player):
        super(NPC, self).__init__()
        self.image = None
        self.current_image = 0
        self.current_direction = 'down'
        self.animating = False
        self.npc_skins = {
            '1': ['Ressources/perso/tabPNJ1.png', 32, 32, 0, 0],
            '2': ['Ressources/perso/tabPNJ1.png', 32, 32, 3 * 32, 0],
            '3': ['Ressources/perso/tabPNJ1.png', 32, 32, 6 * 32, 0],
            '4': ['Ressources/perso/tabPNJ1.png', 32, 32, 9 * 32, 0],
            '5': ['Ressources/perso/tabPNJ1.png', 32, 32, 0, 4 * 32],
            '6': ['Ressources/perso/tabPNJ1.png', 32, 32, 3 * 32, 4 * 32],
            '7': ['Ressources/perso/tabPNJ1.png', 32, 32, 6 * 32, 4 * 32],

            '8': ['Ressources/perso/tabPNJ2.png', 32, 32, 0, 0],
            '9': ['Ressources/perso/tabPNJ2.png', 32, 32, 3 * 32, 0],
            '10': ['Ressources/perso/tabPNJ2.png', 32, 32, 6 * 32, 0],
            '11': ['Ressources/perso/tabPNJ2.png', 32, 32, 9 * 32, 0],
            '12': ['Ressources/perso/tabPNJ4.png', 32, 32, 0, 4 * 32],
            '13': ['Ressources/perso/tabPNJ4.png', 32, 32, 3 * 32, 4 * 32],
            '14': ['Ressources/perso/tabPNJ4.png', 32, 32, 6 * 32, 4 * 32],

            '15': ['Ressources/perso/tabPNJ3.png', 32, 32, 0, 0],
            '16': ['Ressources/perso/tabPNJ3.png', 32, 32, 3 * 32, 0],
            '17': ['Ressources/perso/tabPNJ3.png', 32, 32, 6 * 32, 0],
            '18': ['Ressources/perso/tabPNJ3.png', 32, 32, 9 * 32, 0],
            '19': ['Ressources/perso/tabPNJ3.png', 32, 32, 0, 4 * 32],
            '20': ['Ressources/perso/tabPNJ3.png', 32, 32, 3 * 32, 4 * 32],
            '21': ['Ressources/perso/tabPNJ3.png', 32, 32, 6 * 32, 4 * 32]
        }
        nbr = random.randint(1, 21)
        self.skin_npc = self.npc_skins[str(nbr)]
        self.updateImage(self.skin_npc[0],
                         self.skin_npc[1],
                         self.skin_npc[2],
                         self.skin_npc[3],
                         self.skin_npc[4])
        self.original_image = self.image

        self.damage_image = (self.image.copy()).convert_alpha()
        self.damage_image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        self.damage_image.fill((255, 0, 0, 0), None, pygame.BLEND_RGBA_ADD)

        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.speed = 1
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.screen = screen

        self.name = name
        self.health = 100
        self.npc_health = self.health
        self.max_health = 100
        self.skin = 1
        self.level = 1
        self.hit_countdown = 0
        self.state = "NPC"

        self.type = "basic"
        self.player = player

    def update(self):
        if self.type != "werewolf" and self.type != "boss":
            self.rect.topleft = self.position
            self.feet.midbottom = self.rect.midbottom

        if self.state == "NPC":
            self.health = self.npc_health
        else:
            self.health = self.ww_health

        self.draw_health(self.screen)
        if self.hit_countdown:
            if self.hit_countdown % 2:
                self.image = self.damage_image  # (or other suitable pre-loaded image)
            else:
                self.image = self.original_image
            self.hit_countdown = max(0, self.hit_countdown - 1)
        elif self.hit_countdown == 0:
            self.image = self.original_image
            self.hit_countdown = None

        #animation
        if self.animating:
            self.current_image += 0.2
            if self.current_image >= len(self.images[self.current_direction]):
                self.current_image = 0
            self.image = self.images[self.current_direction][int(self.current_image)]
            self.image.set_colorkey([0, 0, 0])

        if self.health <= 0:
            self.kill()

        self.screen.blit(self.image, self.rect)

    def lose_health(self):
        self.npc_health -= 1 / 60

    def generate_money(self):
        return self.health/2

    def change_animation(self, name):
        self.image.set_colorkey((0, 0, 0))
        self.image = self.images[name][0]
        self.original_image = self.image

    def get_image(self, x, y):
        image = pygame.Surface([self.sprite_size_x, self.sprite_size_y])
        image.blit(self.sprite_sheet, (0, 0), (x, y, self.sprite_size_x, self.sprite_size_y))
        return image

    def updateImage(self, ressource, sprite_size_x, sprite_size_y, decal_x=0, decal_y=0):
        self.sprite_size_x = sprite_size_x
        self.sprite_size_y = sprite_size_y
        self.sprite_sheet = pygame.image.load(ressource)
        self.image = self.get_image(0+decal_x, 0+decal_y)
        self.image.set_colorkey([0, 0, 0])
        self.images = {
            'down': [self.get_image(0+decal_x, 0+decal_y),
                     self.get_image(sprite_size_x+decal_x, 0+decal_y),
                     self.get_image(sprite_size_x*2+decal_x, 0+decal_y)],
            'up': [self.get_image(0+decal_x, (3 * self.sprite_size_y)+decal_y),
                   self.get_image(sprite_size_x+decal_x, (3 * self.sprite_size_y)+decal_y),
                   self.get_image(sprite_size_x*2+decal_x, (3 * self.sprite_size_y)+decal_y)],
            'right': [self.get_image(0+decal_x, (2 * self.sprite_size_y)+decal_y),
                      self.get_image(sprite_size_x+decal_x, (2 * self.sprite_size_y)+decal_y),
                      self.get_image(sprite_size_x*2+decal_x, (2 * self.sprite_size_y)+decal_y)],
            'left': [self.get_image(0+decal_x, self.sprite_size_y+decal_y),
                     self.get_image(sprite_size_x+decal_x, self.sprite_size_y+decal_y),
                     self.get_image(sprite_size_x*2+decal_x, self.sprite_size_y+decal_y)]
        }
        self.original_image = self.image

    def take_damage(self, amount, xEnnemy, yEnnemy):
        if self.state == "NPC":
            self.npc_health -= amount
        else:
            self.ww_health -= amount

        self.original_image = self.image
        self.hit_countdown = 10
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
            randomItem = random.choice(item.itemList) #une fois le npc mort on choisi un item au hasard parmi ceux dans la liste
            randomItem.draw(self.screen, self.position[0], self.position[1]) #on affiche l'item au lieu de la mort du NPC
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
        if self.state == "NPC":
            self.draw_health_bar(surf, health_rect.topleft, health_rect.size, (0, 0, 0), (255, 0, 0), (0, 255, 0),
                        self.health / self.max_health)
        else:
            self.draw_health_bar(surf, health_rect.topleft, health_rect.size, (0, 0, 0), (255, 0, 0), (0, 255, 0),
                                 self.health / self.ww_max_health)

    def heal(self, amount):
        if self.npc_health + amount > self.max_health:
            self.npc_health = self.max_health
        else:
            self.npc_health += amount

    def startDialog(self):
        """
        dialog_circle = pygame.draw.circle(self.screen,  (255, 255, 255), (self.rect.centerx, self.rect.top), 7)
        dialog_circle.midbottom = self.rect.centerx, self.rect.top

        pygame.draw.rect(surface, color_background, (dialog_circle, dialog_circle.size))
        pygame.draw.rect(surface, color_border, (dialog_circle, dialog_circle.size), 1)
        innerPos = (position[0] + 1, position[1] + 1)
        innerSize = (int((size[0] - 2) * progress), size[1] - 2)
        pygame.draw.rect(surface, color_health, (*innerPos, *innerSize))
        """


