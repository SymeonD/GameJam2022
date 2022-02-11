import pygame
from Model import item

class Weapon(item.Item):

    def __init__(self, id, name, roll, image, effect, price, att_speed, att_range, att_power):
        super().__init__(id, name, roll, image, effect, 0, price)
        self.att_speed = att_speed
        self.att_range = att_range
        self.att_power = att_power


item.itemList.append(Weapon(2,"Wooden sword",5,(pygame.image.load('Ressources/item/tile081.png')), "weapon", 100, 1/60, 100, 20))
item.itemList.append(Weapon(8,"Knight's sword",5,(pygame.image.load('Ressources/item/tile082.png')), "weapon", 250, 1/45, 150, 35))
item.itemList.append(Weapon(9,"Corsair sword",5,(pygame.image.load('Ressources/item/tile085.png')), "weapon", 500, 1/30, 150, 50))
