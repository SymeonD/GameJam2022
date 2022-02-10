from Model.NPC import NPC as parent
from pygame import mixer
import pygame
import math
import os


class NPC_Werewolf(parent):

    def __init__(self, x, y, name, screen, moonCycle, player):
        super().__init__(x, y, name, screen, player)
        self.updateImage('Ressources/perso/NPC1.png', 32,  32)
        self.werewolf_skins = {
            '1': ['Ressources/perso/WereWolfs.png', 48, 52, 0, 0],
            '2': ['Ressources/perso/WereWolfs.png', 48, 52, 3*48, 0],
            '3': ['Ressources/perso/WereWolfs.png', 48, 52, 9*48, 0],
            '4': ['Ressources/perso/WereWolfs.png', 48, 52, 0, 4*52],
            '5': ['Ressources/perso/WereWolfs.png', 48, 52, 6*48, 4*52]
        }
        self.moonCycle = moonCycle
        self.type = 'werewolf'
        self.target = None
        self.state = 'NPC'
        self.damage = self.moonCycle*10
        self.attack_speed = 1/(60*(6-self.moonCycle))
        self.attack_cooldown = 1
        self.old_position = self.position.copy()
        self.detect_range = self.moonCycle*50
        self.speed = self.moonCycle
        self.health = 100*moonCycle
        self.max_health = 100*moonCycle

    def transform(self, cycleMoon):
        if cycleMoon == 6:
            self.updateImage('Ressources/perso/NPC1.png', 32, 32, 0, 0)
            self.damage_image = (self.image.copy()).convert_alpha()
            self.damage_image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
            self.damage_image.fill((255, 0, 0, 0), None, pygame.BLEND_RGBA_ADD)
            self.rect = self.image.get_rect()
            self.state = 'NPC'
            self.animating = False
        elif cycleMoon >= self.moonCycle:
            self.updateImage(self.werewolf_skins[str(self.moonCycle)][0],
                             self.werewolf_skins[str(self.moonCycle)][1],
                             self.werewolf_skins[str(self.moonCycle)][2],
                             self.werewolf_skins[str(self.moonCycle)][3],
                             self.werewolf_skins[str(self.moonCycle)][4])
            self.damage_image = (self.image.copy()).convert_alpha()
            self.damage_image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
            self.damage_image.fill((255, 0, 0, 0), None, pygame.BLEND_RGBA_ADD)
            self.rect = self.image.get_rect()
            self.state = 'WW'
            transformSound = mixer.Sound('Ressources/sounds/transform.mp3')
            transformSound.play()

    def update(self):
        super().update()
        if self.state == "WW":
            self.updateTarget(self.player)
            self.move_npc(self.player)

        # update attack cooldown
        if self.attack_cooldown < 1:
            self.attack_cooldown += self.attack_speed

        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def updateTarget(self, player1):
        if self.target:
            if math.hypot(self.position[0] - player1.position[0],
                          self.position[1] - player1.position[1]) < math.hypot(self.position[0] -
                                                                               self.target.position[0],
                                                                               self.position[1] -
                                                                               self.target.position[1]):
                if self.target != player1:
                    self.target = player1
        else:
            self.target = player1
        self.targetDistance = math.hypot(self.position[0] - self.target.position[0],
                                         self.position[1] - self.target.position[1])

    def move_npc(self, player1):
        self.save_location()
        if self.state == 'WW':
            self.updateTarget(player1)
            rotation = 75
            if self.targetDistance < self.detect_range:
                if self.targetDistance < 50:
                    self.attack(player1)
                self.animating = True
                if self.position[1] > self.target.position[1]:
                    self.position[1] -= self.speed
                    self.change_animation("up")
                    self.current_direction = "up"
                if self.position[1] < self.target.position[1]:
                    self.position[1] += self.speed
                    self.change_animation("down")
                    self.current_direction = "down"
                if self.position[0] > self.target.position[0]:
                    self.position[0] -= self.speed
                    if self.position[1] - self.target.position[1] < rotation and self.position[1] - \
                            self.target.position[1] > -rotation:
                        self.change_animation("left")
                        self.current_direction = "left"
                if self.position[0] < self.target.position[0]:
                    self.position[0] += self.speed
                    if self.position[1] - self.target.position[1] < rotation and self.position[1] - \
                            self.target.position[1] > -rotation:
                        self.change_animation("right")
                        self.current_direction = "right"
            else:
                self.change_animation("down")
                self.animating = False

    def save_location(self):
        self.old_position = self.position.copy()

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_forth(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def attack(self, player):
        if self.attack_cooldown >= 1:
            player.take_damage(self.damage, self.position[0], self.position[1])
            self.attack_cooldown = 0
