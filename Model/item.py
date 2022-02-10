import pygame

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

    def useItem(self, sprite):
        if self.effect == "heal":
            sprite.heal(self.effect_power)
        if self.effect == "damage":
            sprite.take_damage(self.effect_power, 1024, 768)
        if self.effect == "sleep":
            print("sleep")
            #sprite.sleep(self.effect_power)

#créer la liste d'item
itemList = []

#pour ajouter un item à notre liste
itemList.append(Item(0,'Potion de Vie',5, (pygame.image.load('Ressources/item/tile144.png')), 'heal', 20, 20))
itemList.append(Item(1,"Pain",5,(pygame.image.load('Ressources/item/tile238.png')), "heal", 5, 5))
itemList.append(Item(2,"Epee en bois",5,(pygame.image.load('Ressources/item/tile081.png')), "weapon", 10, 50))
itemList.append(Item(4,"Piece",5,(pygame.image.load('Ressources/item/tile199.png')), "damage", 10, 10)) # money
itemList.append(Item(5,"Bouclier rond",5,(pygame.image.load('Ressources/item/tile096.png')), "protection", 10, 100))
itemList.append(Item(6,"Bouclier puissant",5,(pygame.image.load('Ressources/item/tile097.png')), "damage", 25, 250))
itemList.append(Item(7,"Bouclier croisé",5,(pygame.image.load('Ressources/item/tile098.png')), "damage", 50, 500))
itemList.append(Item(8,"Epee de chevalier",5,(pygame.image.load('Ressources/item/tile082.png')), "weapon", 25, 250))
itemList.append(Item(9,"Epee de corsaire",5,(pygame.image.load('Ressources/item/tile085.png')), "weapon", 50, 500))
itemList.append(Item(10,"Potion de force",5,(pygame.image.load('Ressources/item/tile147.png')), "strength", 10, 100))
itemList.append(Item(11,"Potion de vitesse",5,(pygame.image.load('Ressources/item/tile145.png')), "speed", 10, 100))



