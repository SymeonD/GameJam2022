import pygame
from Model.bouton import Button

pygame.init()
pygame.display.set_caption("Where's Wolf")
screen = pygame.display.set_mode((1024, 768))

class regles:

    def run():

        background_img = pygame.image.load('Ressources/menu/règlesbg.jpg').convert_alpha()

        exit_img = pygame.image.load('Ressources/item/tile037.png').convert_alpha()
        exit_button = Button(900, 650, exit_img, 3)

        running = True
        
        while running:
                #affiche l'image de fond
                screen.blit(background_img, (0, 0))

                #dessine les boutons crees precedemment
                if exit_button.draw(screen):
                        running = False

                #si on ferme la fenetre
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        running = False
                    
                #actualisation
                pygame.display.update()