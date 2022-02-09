from Model.NPC import NPC as parent
import pygame
import math
import os


class NPC_Werewolf(parent):

    def __init__(self, x, y, name, screen, moonCycle):
        super().__init__(x, y, name, screen)
        self.updateImage('Ressources/player.png', 32,  32)
        self.werewolf_skins = {
            '1': ['Ressources/WereWolfs.png', 48, 52, 0, 0],
            '2': ['Ressources/WereWolfs.png', 48, 52, 3*48, 0],
            '3': ['Ressources/WereWolfs.png', 48, 52, 9*48, 0],
            '4': ['Ressources/WereWolfs.png', 48, 52, 0, 4*52],
            '5': ['Ressources/WereWolfs.png', 48, 52, 6*48, 4*52],
        }
        self.moonCycle = moonCycle
        self.type = 'speed'
        self.target = None
        self.state = 'NPC'
        self.damage = self.moonCycle*10

    def transform(self, cycleMoon):
        if cycleMoon == 6:
            self.updateImage('Ressources/player.png', 32, 32)
            self.damage_image = (self.image.copy()).convert_alpha()
            self.damage_image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
            self.damage_image.fill((255, 0, 0, 0), None, pygame.BLEND_RGBA_ADD)
            self.rect = self.image.get_rect()
            self.state = 'NPC'
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
        if self.state == 'WW':
            self.updateTarget(player1)
            rotation = 75
            if self.targetDistance < 200:
                if self.position[1] > self.target.position[1]:
                    self.position[1] -= self.speed
                    self.change_animation("up")
                if self.position[1] < self.target.position[1]:
                    self.position[1] += self.speed
                    self.change_animation("down")
                if self.position[0] > self.target.position[0]:
                    self.position[0] -= self.speed
                    if self.position[1] - self.target.position[1] < rotation and self.position[1] - \
                            self.target.position[1] > -rotation:
                        self.change_animation("left")
                if self.position[0] < self.target.position[0]:
                    self.position[0] += self.speed
                    if self.position[1] - self.target.position[1] < rotation and self.position[1] - \
                            self.target.position[1] > -rotation:
                        self.change_animation("right")
            else:
                self.change_animation("down")
