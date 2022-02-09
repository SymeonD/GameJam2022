import random

import pygame
import pytmx
import pyscroll
import sys
import math
from pygame import mixer
from Model.Map import MapManager

from Model.bouton import Button
from Model.Player import Player
from Model.NPC_Werewolf import NPC_Werewolf
from Model.inventory import Inventory

class Game:

    def __init__(self):
        #creation de la fenetre du jeu
            #dimension de la fenetre
        SCREEN_WIDTH = 1024
        SCREEN_HEIGHT = 768
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            #titre de la fenetre
        pygame.display.set_caption('WereWolf')

        #map de base
        self.map = "town_day"

        #chargement du joueur
        self.player = Player(0, 0, self.screen)

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




    def run(self):
        running = True

        #mixer.music.play() #lecture de la musique

        while running:
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

            self.update()

            #event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()


                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    #Clique sur l'inventaire
                    #if self.player.inventory.In_grid(self.player.inventory.Get_pos()[0],
                    #                                 self.player.inventory.Get_pos()[1]):
                    #    print(self.player.inventory.Get_pos())

        pygame.quit

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            self.player.move_player('up')
        if keys[pygame.K_q]:
            self.player.move_player('left')
        if keys[pygame.K_s]:
            self.player.move_player('down')
        if keys[pygame.K_d]:
            self.player.move_player('right')
        if keys[pygame.K_p]:
            self.pause()


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
        Inventory.update(self.player.inventory, self.screen, self.player.inventory)

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
