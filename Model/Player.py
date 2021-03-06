import pygame
import os
import math

from Model.inventory import Inventory
from Model.Weapon import Weapon
from Model import item
from pygame import mixer

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, screen):
        super(Player, self).__init__()
        self.sprite_sheet = pygame.image.load('Ressources/perso/player.png')
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.original_image = self.image

        self.damage_image = (self.image.copy()).convert_alpha()
        self.damage_image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        self.damage_image.fill((255, 0, 0, 0), None, pygame.BLEND_RGBA_ADD)

        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.images = {
            'down': [self.get_image(0, 0), self.get_image(32, 0), self.get_image(64, 0)],
            'up': [self.get_image(0, 96), self.get_image(32, 96), self.get_image(64, 96)],
            'right': [self.get_image(0, 64), self.get_image(32, 64), self.get_image(64, 64)],
            'left': [self.get_image(0, 32), self.get_image(32, 32), self.get_image(64, 32)],
            'stop': [self.get_image(0, 0)]
        }
        self.current_image = 0
        self.current_direction = 'down'
        self.animating = False

        self.type = "player"

        self.old_position = self.position.copy()
        self.speed = 2
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)

        self.screen = screen
        self.hit_countdown = None

        self.name = "player"
        self.health = 200
        self.max_health = 200
        self.skin = 1
        self.inventory = Inventory(650, 650)
        self.inventory.add(item.itemList[0])
        self.inventory.add(item.itemList[0])
        self.inventory.add(item.itemList[1])
        self.inventory.add(item.itemList[1])
        self.inventory.add(item.itemList[1])
        self.inventory.add(item.itemList[1])
        self.inventory.add(item.itemList[1])

        self.weapon = "sword"
        self.weapon_power = 1
        self.weapon_speed = 1/15
        self.weapon_range = 50
        self.attack_cooldown = 1

        self.money = 0
        self.inventory_open = True
        self.strength = 10
        self.defense = 10

        self.is_dead = False
        self.cooldown_inventory = 0
        self.werewolf_killed = 0

        #potions
        self.speed_use = False
        self.strength_use = False
        self.protect_use = False

    def get(self):
        self.image = self.images["down"][0]
        self.image.set_colorkey([0, 0, 0])
        return self.image

    def save_location(self):
        self.old_position = self.position.copy()

    def move_player(self, type):
        self.image = self.images[type][0]
        self.image.set_colorkey([0, 0, 0])
        self.current_direction = type
        self.animating = True
        if type == "up":
            self.position[1] -= self.speed
        elif type == "down":
            self.position[1] += self.speed
        elif type == "right":
            self.position[0] += self.speed
        elif type == "left":
            self.position[0] -= self.speed
        elif type == "stop":
            self.animating = False
        self.original_image = self.image

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

        #animation
        if self.animating:
            self.current_image += 0.2
            if self.current_image >= len(self.images[self.current_direction]):
                self.current_image = 0
            self.image = self.images[self.current_direction][int(self.current_image)]
        self.image.set_colorkey([0, 0, 0])
        self.damage_image = (self.image.copy()).convert_alpha()
        self.damage_image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        self.damage_image.fill((255, 0, 0, 0), None, pygame.BLEND_RGBA_ADD)

        # blink if damaged
        if self.hit_countdown:
            if self.hit_countdown % 2:
                self.image = self.damage_image  # (or other suitable pre-loaded image)
            else:
                self.image = self.original_image
            self.hit_countdown = max(0, self.hit_countdown - 1)
        elif self.hit_countdown == 0:
            self.image = self.original_image
            self.hit_countdown = None

        #update attack cooldown
        if self.attack_cooldown < 1:
            self.attack_cooldown += self.weapon_speed

        #draw caracter image
        self.screen.blit(self.image, self.rect)

        # Update health bar
        self.draw_health(self.screen)

        #update cooldown inventory
        if self.cooldown_inventory > 0:
            self.cooldown_inventory -= 1/5

        self.update_preview()

    def update_preview(self):
        font = pygame.font.Font(pygame.font.match_font("calibri"), 22)

        # Update money
        text_money = ": " + str(self.money)
        obj = font.render(text_money, True, (0, 0, 0), (255, 255, 255, 100))
        self.screen.blit(item.itemList[2].image, (25, 640))
        self.screen.blit(obj, (70, 640,))

        # update strength
        text_strength = ": " + str(self.strength * self.weapon_power)
        obj = font.render(text_strength, True, (0, 0, 0), (255, 255, 255))
        self.screen.blit(item.itemList[8].image, (25, 670))
        self.screen.blit(obj, (70, 670,))

        # update speed
        text_speed = ": " + str(self.speed)
        obj = font.render(text_speed, True, (0, 0, 0), (255, 255, 255))
        self.screen.blit(item.itemList[9].image, (25, 700))
        self.screen.blit(obj, (70, 700,))

        # update speed
        text_defense = ": " + str(self.defense)
        obj = font.render(text_defense, True, (0, 0, 0), (255, 255, 255))
        self.screen.blit(item.itemList[10].image, (25, 730))
        self.screen.blit(obj, (70, 730,))

        # update inventory touch
        text_inventory = "E : open / close inventory"
        obj = font.render(text_inventory, True, (0, 0, 0), (255, 255, 255))
        self.screen.blit(obj, (655, 730,))

        # update pause touch
        text_pause = "P : Pause"
        obj = font.render(text_pause, True, (0, 0, 0), (255, 255, 255))
        self.screen.blit(obj, (900, 730,))

    def updateInv(self):
        if self.inventory_open:
            self.inventory.update(self.screen)

    def toggle_inventory(self):
        if self.cooldown_inventory <= 0:
            self.inventory_open = not self.inventory_open
            self.cooldown_inventory = 1

    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image

    def move_back(self):
        self.position = self.old_position
        self.update()

    def kill_werewolf(self):
        self.werewolf_killed += 1

    def take_damage(self, amount, xEnnemy, yEnnemy):
        self.health -= amount/(self.defense/20)
        self.original_image = self.image
        self.hit_countdown = 10

        playerHitSound = mixer.Sound('Ressources/sounds/player_hit.ogg')
        playerHitSound.play()

        # jump_back = 10

        '''
        if self.position[0] - xEnnemy < 0:
            self.position[0] -= self.speed * jump_back
        if self.position[0] - xEnnemy > 0:
            self.position[0] += self.speed * jump_back
        if self.position[1] - yEnnemy < 0:
            self.position[1] -= self.speed * jump_back
        if self.position[1] - yEnnemy > 0:
            self.position[1] += self.speed * jump_back
        '''

        if self.health <= 0:
            self.is_dead = True
            print("Game Over")
        self.update()

    def attack(self, werewolf):
        werewolf_distance = math.hypot(self.position[0] - werewolf.position[0],
                                       self.position[1] - werewolf.position[1])
        if werewolf_distance < self.weapon_range and self.attack_cooldown >= 1:
            werewolf.take_damage(self.weapon_power+self.strength, self.position[0], self.position[1])
            self.attack_cooldown = 0

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


    #Item effect functions
    def heal(self, amount):
        print(amount)
        if self.health + amount > self.max_health:
            self.health = self.max_health
        else:
            self.health += amount

    def protect(self, amount):
        if not self.protect_use:
            self.defense += amount
            self.protect_use = True
        else:
            self.defense += amount/10

    def strengthen(self, amount):
        if not self.strength_use:
            self.strength += amount
            self.strength_use = True
        else:
            self.strength += amount/10

    def increase_speed(self, amount):
        if not self.speed_use:
            self.speed += amount
            self.speed_use = True
        else:
            self.speed += amount/10


    def equip_weapon(self, weapon):
        self.weapon = weapon.name
        self.weapon_speed = weapon.att_speed
        self.weapon_power = weapon.att_power
        self.weapon_range = weapon.att_range

    def drop(self, amount):
        self.money += amount

    #trader function
    def buy(self, item_to_buy):
        if self.inventory.is_full():
            print("inventaire plein")
        else:
            if self.money >= item_to_buy[0].price:
                self.inventory.add(item_to_buy[0])
                self.money -= item_to_buy[0].price
                mixer.Sound('Ressources/sounds/coin_loose.mp3').play()
            else:
                print("Vous etes trop pauvre")

