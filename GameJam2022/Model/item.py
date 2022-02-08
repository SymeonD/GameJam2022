import pygame

items = [pygame.Surface((50,50),pygame.SRCALPHA)]

class Item:
    def __init__(self,id):
        self.id = id
        self.surface = items[id]
    
    def resize(self,size):
        return pygame.transform.scale(self.surface,(size,size))