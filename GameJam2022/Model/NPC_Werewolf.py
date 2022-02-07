import pygame
import pygame_ai as pai

from NPC import NPC as parent

class NPC_Werewolf(parent):

    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        self.moonCycle = 1;
        self.type = 'speed';

        self.ai = pai.steering.kinematic.NullSteering()

    def update(self):
        steering = self.ai.get_steering()