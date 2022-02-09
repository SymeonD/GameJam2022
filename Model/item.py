import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self,id,name,roll,image):
        super(Item, self).__init__
        self.id = id #id de l'item dans la liste
        self.name = name #nom de l'item
        self.roll = roll #chance de drop
        self.image = image #image de l'item
        self.effect = None
        self.rect = self.image.get_rect()

    def draw(self, screen, posx, posy):
        screen.blit(self.image, (posx, posy))

#créer la liste d'item
itemList = []

#pour ajouter un item à notre liste
itemList.append(Item(0,'Potion de Vie',5, (pygame.image.load('Ressources/item/tile144.png'))))
itemList.append(Item(1,"Pain",5,(pygame.image.load('Ressources/item/tile238.png'))))
itemList.append(Item(2,"Piece",5,(pygame.image.load('Ressources/item/tile199.png'))))
