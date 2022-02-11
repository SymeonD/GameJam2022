import pygame
import math

class Item(pygame.sprite.Sprite):
    def __init__(self, id, name, roll, image, effect, effect_power, price):
        super(Item, self).__init__
        self.id = id #id de l'item dans la liste
        self.name = name #nom de l'item
        self.roll = roll #chance de drop
        self.image = image #image de l'item


        self.effect = effect
        self.effect_power = effect_power
        self.price = price

        self.rect = self.image.get_rect()

    def draw(self, screen, posx, posy):
        screen.blit(self.image, (posx, posy))

    def useItem(self, sprite, player):
        distance = math.hypot(sprite.position[0] - player.position[0],
                                       sprite.position[1] - player.position[1])
        if distance <= 200:
            if self.effect == "heal":
                sprite.heal(self.effect_power)
            if self.effect == "damage":
                sprite.take_damage(self.effect_power, 1024, 768)
            if sprite.type == "player":
                if self.effect == "protection":
                    sprite.protect(self.effect_power)
                if self.effect == "strength":
                    sprite.strengthen(self.effect_power)
                if self.effect == "speed":
                    sprite.increase_speed(self.effect_power)
                if self.effect == "weapon":
                    sprite.equip_weapon(self)
            return True
        else:
            return False

#créer la liste d'item
itemList = []

#pour ajouter un item à notre liste
itemList.append(Item(0,'Health potion',5, (pygame.image.load('Ressources/item/tile144.png')), 'heal', 20, 20))
itemList.append(Item(1,"Bread",5,(pygame.image.load('Ressources/item/tile238.png')), "heal", 5, 5))
itemList.append(Item(4,"Piece",5,(pygame.image.load('Ressources/item/tile199.png')), "damage", 10, 10)) # money
itemList.append(Item(5,"Round shield",5,(pygame.image.load('Ressources/item/tile096.png')), "protection", 10, 100))
itemList.append(Item(6,"Strong shield",5,(pygame.image.load('Ressources/item/tile097.png')), "protection", 25, 250))
itemList.append(Item(7,"Heater shield",5,(pygame.image.load('Ressources/item/tile098.png')), "protection", 50, 500))
itemList.append(Item(10,"Strength potion",5,(pygame.image.load('Ressources/item/tile147.png')), "strength", 10, 100))
itemList.append(Item(11,"Speed potion",5,(pygame.image.load('Ressources/item/tile145.png')), "speed", 10, 100))



