import random

import pygame
import pytmx
#import pyscroll
import sys

from Model.bouton import Button
from Model.Player import Player
from Model.NPC_Werewolf import NPC_Werewolf
from Model.inventory import Inventory
from Model.credits import Credits
from Model.regles import regles
from Model.histoire import histoire

class Menu:

    def __init__(self):
        #chargement de l'image de fond
        self.background_img = pygame.image.load('Ressources/menu/finalbg.jpg').convert_alpha()

        #chargement des images pour boutons
        self.start_img = pygame.image.load('Ressources/menu/start_btn.png').convert_alpha()
        self.exit_img = pygame.image.load('Ressources/menu/exit_btn.png').convert_alpha()
        self.credits_img = pygame.image.load('Ressources/item/tile216.png').convert_alpha()
        self.story_img = pygame.image.load('Ressources/item/tile212.png').convert_alpha()
        self.rules_img = pygame.image.load('Ressources/item/tile219.png').convert_alpha()

        #creer les boutons
        self.start_button = Button(200, 300, self.start_img, 0.5)
        self.exit_button = Button(700, 300, self.exit_img, 0.5)
        self.credits_button = Button(432, 600, self.credits_img, 5)
        self.story_button = Button(132, 600, self.story_img, 5)
        self.rules_button = Button(732, 600, self.rules_img, 5)

        font = pygame.font.SysFont(None, 24)
        self.text_story = font.render('Histoire', True, (255, 255, 255))
        self.text_credits = font.render('Credits', True, (255, 255, 255))
        self.text_rules = font.render('Règles', True, (255, 255, 255))


    def menu(self, screen, game):
        running = True
        while running:
            #affiche l'image de fond
            screen.blit(self.background_img, (0, 0))

            #affiche les noms pour les 3 icones
            screen.blit(self.text_credits, (482, 590))
            screen.blit(self.text_rules, (182, 590))
            screen.blit(self.text_story, (782, 590))

            #dessine les boutons crees precedemment
            if self.start_button.draw(screen):
                game.run()
            if self.exit_button.draw(screen):
                running = False
            if self.credits_button.draw(screen):
                Credits.credits()
            if self.story_button.draw(screen):
                regles.run()
            if self.rules_button.draw(screen):
                histoire.run()

            #si on ferme la fenetre
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    running = False
            
            #actualisation
            pygame.display.update()

        pygame.quit()