import pygame

#items = [pygame.Surface((50,50),pygame.SRCALPHA)]

class Item:
    def __init__(self,id,name,roll,image):
        self.id = id #id de l'item dans la liste
        self.name = name #nom de l'item
        self.roll = roll #chance de drop
        self.image = image #image de l'item
        #self.surface = items[id]
    
    def resize(self,size):
        return pygame.transform.scale(self.surface,(size,size))

#créer la liste d'item
itemList = []

#pour ajouter un item à notre liste
list.append(Item(0,'Potion de Vie',5, (pygame.image.load('Ressources/item/tile144.png'))))