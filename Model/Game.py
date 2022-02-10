import random

import pygame
import pytmx
#import pyscroll
import sys
import math
from pygame import mixer
from Model.Map import MapManager

from Model.bouton import Button
from Model.Player import Player
from Model.NPC_Werewolf import NPC_Werewolf
from Model.NPC_Trader import NPC_Trader
from Model.inventory import Inventory

class Game:

    def __init__(self):
        #creation de la fenetre du jeu
            #dimension de la fenetre
        SCREEN_WIDTH = 1024
        SCREEN_HEIGHT = 768
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            #titre de la fenetre
        pygame.display.set_caption("Where's Wolf")

        #map de base
        self.map = "town_day"

        #chargement du joueur
        self.player = Player(0, 0, self.screen)

        # Test du trade
        self.trader = NPC_Trader(500, 100, "Trader", self.screen)

        #Map manager
        self.map_manager = MapManager(self.screen, self.player)

        #définir le logo du jeu
        pygame.display.set_icon(self.player.get())

        #Création d'une clock pour les FPS
        self.clock = pygame.time.Clock()

        #Etat cycle jour/nuit
        self.cycleState = "jour"

        #Etat du cycle des lunes
        self.cycleMoon = 0

        #Définition du tick de départ de l'horloge
        self.start_ticks = pygame.time.get_ticks()

        # initialisation musique de fond (jour)
        mixer.pre_init(44100, 16, 2, 4096)
        mixer.init()
        mixer.music.load("Ressources/music/background_day.mp3")
        mixer.music.set_volume(1)

        #Variable de gestion du drag and drop
        self.itemSelected = None

        #Variable de la boucle du jeu
        self.running = True




    def run(self):

        #mixer.music.play() #lecture de la musique

        while self.running:

            #Limiter à 60 fps
            self.clock.tick(60)

            #gestion des cycles jour/nui
            self.switch_cycle()

            # Dessin de la map + centrage
            self.map_manager.draw()

            #sauvegarde localisation joueur
            self.player.save_location()

            #gestion des touches
            self.handle_input()

            #update game
            self.update()

            #update events
            self.handle_event(pygame.event.get())



        pygame.quit

    def handle_event(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                #clicked_sprites = [s for s in self.map_manager.get_group() if s.rect.collidepoint(pos)] + [s for s in self.werewolf_group if s.rect.collidepoint(pos)]
                if self.itemSelected:
                    #for sprite in clicked_sprites:
                    #    if self.itemSelected[0].name == "Potion de Vie":
                    #        sprite.heal(50)
                    if self.player.rect.collidepoint(pos):
                        self.itemSelected[0].useItem(self.player)
                        self.player.inventory.removeItem(self.itemSelected, 1)
                        for item in self.player.inventory.items:
                            print(item[0].name + str(item[1]))
                    self.itemSelected = None
                    self.player.inventory.toggleDesc("", self.screen, "", pos[0], pos[1])

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)
                # Clique sur l'inventaire
                if self.player.inventory.in_grid(pos[0], pos[1]):
                    self.itemSelected = self.player.inventory.getItem(pos[0], pos[1])
                    # self.player.inventory.removeItem(self.itemSelected[0], "all")
                else:
                    self.itemSelected = None
                    self.player.inventory.toggleDesc("", self.screen, "", pos[0], pos[1])

                #Test trader:
                if self.trader.rect.collidepoint(pos):
                    self.trader.trade()


            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()

                #passe sur un trader
                if self.trader.rect.collidepoint(pos):
                    self.trader.toggleDesc("desc", "Click to trade", pos[0], pos[1])
                else:
                    self.trader.toggleDesc("", "", pos[0], pos[1])

                # Passe sur l'inventaire
                if self.player.inventory.in_grid(pos[0], pos[1]):

                    # Item survolé
                    itemDesc = self.player.inventory.getItem(pos[0], pos[1])

                    # Si il y a un item séléctionné
                    if self.itemSelected:
                        self.player.inventory.toggleDesc("item", self.screen, self.itemSelected[0].image, pos[0], pos[1])

                    # Afficher la description
                    elif itemDesc:
                        self.player.inventory.toggleDesc("desc", self.screen, itemDesc[0].name, pos[0], pos[1])
                    else:
                        self.player.inventory.toggleDesc("", self.screen, "", pos[0], pos[1])
                elif self.itemSelected:
                    self.player.inventory.toggleDesc("item", self.screen, self.itemSelected[0].image, pos[0], pos[1])
                else:
                    self.player.inventory.toggleDesc("", self.screen, "", pos[0], pos[1])

    def handle_input(self):
        keys = pygame.key.get_pressed()
        keyD = False
        if keys[pygame.K_z]:
            self.player.move_player('up')
            keyD = True
        if keys[pygame.K_q]:
            self.player.move_player('left')
            keyD = True
        if keys[pygame.K_s]:
            self.player.move_player('down')
            keyD = True
        if keys[pygame.K_d]:
            self.player.move_player('right')
            keyD = True
        if keys[pygame.K_p]:
            self.pause()
            keyD = True
        if not keyD:
            self.player.move_player('stop')


    def switch_cycle(self):
        

        #Récupère les secondes
        seconds = (pygame.time.get_ticks()-self.start_ticks)//1000

        if seconds > 10:
            self.start_ticks = pygame.time.get_ticks()
            if self.cycleState == "jour":
                self.cycleState = "nuit"

                #Mooncycle update
                self.cycleMoon += 1
                if self.cycleMoon > 5:
                    self.cycleMoon = 1
                    #Add special effects (super werewolves...)



    def update(self):


        self.map_manager.update()

        # test trader
        self.trader.update()

        self.screen.blit(self.trader.image, self.trader.rect)

        pygame.display.update()




    def pause(self):
        runPause = True

        # chargement de l'image de fond
        background_img = pygame.image.load('Ressources/menu/bg.jpg').convert_alpha()

        # chargement des images pour boutons
        resume_img = pygame.image.load('Ressources/menu/start_btn.png').convert_alpha()
        leave_img = pygame.image.load('Ressources/menu/exit_btn.png').convert_alpha()

        # creer les boutons
        resume_button = Button(100, 200, resume_img, 0.5)
        leave_button = Button(600, 200, leave_img, 0.5)

        # musique en pause
        mixer.music.pause()

        while runPause:
            self.screen.blit(background_img, (0, 0))
            if resume_button.draw(self.screen):
                runPause = False
                mixer.music.unpause() #musique à nouveau active
            if leave_button.draw(self.screen):
                sys.exit(2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(2)

            pygame.display.update()
