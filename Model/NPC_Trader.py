import pygame

from Model.NPC import NPC as parent
from Model.inventory import Inventory
from Model import item

class NPC_Trader(parent):

    def __init__(self, x, y, name, screen):
        super().__init__(x, y, name, screen)
        print(x, y)
        self.inventory = Inventory(16+x-336/2,y-73-20)
        self.inventory.add(item.itemList[0])
        self.type = "trader"

    def trade(self):
        self.tradeState = not self.tradeState



