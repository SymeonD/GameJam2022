import pygame

from Model.NPC import NPC as parent
from Model import item

class NPC_Trader(parent):

    def __init__(self, x, y, name, screen):
        super().__init__(x, y, name, screen)
        self.inventory = Inventory(x-336/2,y-10)
        self.inventory.add(item.itemList[0])
        self.trade = False

    def trade(self):
        self.trade = True

    def update(self):
        if trade:
            self.inventory.update()

