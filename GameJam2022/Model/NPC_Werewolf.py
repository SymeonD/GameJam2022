from Model.NPC import NPC as parent
import pygame
import math


class NPC_Werewolf(parent):

    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        self.updateImage('../Ressources/player.png', 32)
        self.moonCycle = 1
        self.type = 'speed'
        self.target = None

    def transform(self, cycleMoon):
        if cycleMoon >= self.moonCycle:
            self.updateImage('../Ressources/loup Garou.png', 80)

    def updateTarget(self, player1):
        if self.target:
            if math.hypot(self.position[0] - player1.position[0],
                          self.position[1] - player1.position[1]) < math.hypot(
                    self.position[0] - self.target.position[0], self.position[1] - self.target.position[1]):
                if self.target != player1:
                    self.target = player1
        else:
            self.target = player1
        self.targetDistance = math.hypot(self.position[0] - self.target.position[0],
                                         self.position[1] - self.target.position[1])

    def move_npc(self, player1):
        self.updateTarget(player1)
        rotation = 75
        if self.targetDistance < 200 :
            if self.position[1] > self.target.position[1]:
                self.position[1] -= self.speed
                self.change_animation("up")
            if self.position[1] < self.target.position[1]:
                self.position[1] += self.speed
                self.change_animation("down")
            if self.position[0] > self.target.position[0]:
                self.position[0] -= self.speed
                if self.position[1] - self.target.position[1] < rotation and self.position[1] - self.target.position[1] > -rotation:
                    self.change_animation("left")
            if self.position[0] < self.target.position[0]:
                self.position[0] += self.speed
                if self.position[1] - self.target.position[1] < rotation and self.position[1] - self.target.position[1] > -rotation:
                    self.change_animation("right")
        else:
            self.change_animation("down")
