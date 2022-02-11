import pygame

from Model.NPC import NPC as parent
from Model.inventory import Inventory
from Model import item

class NPC_Trader(parent):

    def __init__(self, x, y, name, screen, player):
        super().__init__(x, y, name, screen, player)
        self.inventory = Inventory(16 + x - 336 / 2, y - 73 - 20)
        for new_item in item.itemList:
            if new_item.name != "Piece" and new_item.effect != "affichage":
                self.inventory.add(new_item)
        self.updateImage('Ressources/perso/trader.png', 32, 32)
        self.skin = ['Ressources/perso/trader.png', 32, 32]
        self.type = "trader"
        self.tradeState = False
        self.itemDesc = None
        self.descX = None
        self.descY = None
        self.showDesc = False
        self.itemShow = None

    def update(self):
        super().update()

        # if trader
        if self.showDesc == "desc":
            font = pygame.font.Font(pygame.font.match_font("calibri"), 22)
            obj = font.render(self.itemDesc, True, (0, 0, 0), (255, 255, 255))
            self.screen.blit(obj, (self.descX + 15, self.descY + 15))

    def updateInv(self):
        if self.tradeState:
            self.inventory.update(self.screen)

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

    def trade(self):
        self.tradeState = not self.tradeState

    def take_damage(self, amount, xEnnemy, yEnnemy):
        None



