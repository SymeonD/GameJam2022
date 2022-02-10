import pygame
import os
from Model import item
import random
from pygame import mixer



class NPC(pygame.sprite.Sprite):

    def __init__(self, x, y, name, screen):
        super(NPC, self).__init__()
        self.image = None
        self.current_image = 0
        self.current_direction = 'down'
        self.animating = False
        self.updateImage('Ressources/perso/NPC1.png', 32, 32)
        self.original_image = self.image

        self.damage_image = (self.image.copy()).convert_alpha()
        self.damage_image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        self.damage_image.fill((255, 0, 0, 0), None, pygame.BLEND_RGBA_ADD)

        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.speed = 1
        self.screen = screen

        self.name = name
        self.health = 100
        self.max_health = 100
        self.skin = 1
        self.level = 1
        self.hit_countdown = 0

        #trader
        self.tradeState = False
        self.itemDesc = None
        self.descX = None
        self.descY = None
        self.showDesc = False
        self.itemShow = None

    def update(self):
        self.rect.topleft = self.position
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

        #if trader
        if self.tradeState:
            self.inventory.update(self.screen)
        elif self.showDesc == "desc":
            font = pygame.font.Font(pygame.font.match_font("calibri"), 22)
            obj = font.render(self.itemDesc, True, (0, 0, 0), (255, 255, 255))
            self.screen.blit(obj, (self.descX + 15, self.descY + 15))

        self.screen.blit(self.image, self.rect)

    def toggleDesc(self, state, itemDesc, posX, posY):
        if state == "desc":
            self.itemDesc = itemDesc
            self.descX = posX
            self.descY = posY
            self.showDesc = "desc"
            self.itemShow = None
        elif state == "item":
            self.itemDesc = None
            self.descX = posX
            self.descY = posY
            self.showDesc = "item"
            self.itemShow = itemDesc
        else:
            self.itemDesc = None
            self.descX = None
            self.descY = None
            self.showDesc = False
            self.itemShow = None

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
        self.image = self.get_image(0, 0)
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

    def take_damage(self, amount, xEnnemy, yEnnemy):
        self.health -= amount
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
            print(randomItem.name)
            randomItem.draw(self.screen, self.position[0], self.position[1]) #on affiche l'item au lieu de la mort du NPC
            print('test')
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
        self.draw_health_bar(surf, health_rect.topleft, health_rect.size, (0, 0, 0), (255, 0, 0), (0, 255, 0),
                        self.health / self.max_health)

    def heal(self, amount):
        if self.health + amount > self.max_health:
            self.health = self.max_health
        else:
            self.health += amount

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


