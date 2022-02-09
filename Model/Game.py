import random

import pygame
import pytmx
import pyscroll
import sys

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
        self.map = "town"

        #chargement de la map(tmx)
        tmx_data = pytmx.util_pygame.load_pygame("Ressources/MapTestFormat.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        #map_layer.zoom = 2

        #chargement du joueur
        player_position = tmx_data.get_object_by_name('player')
        self.player = Player(player_position.x, player_position.y, self.screen)

            #définir le logo du jeu
        pygame.display.set_icon(self.player.get())

        #chargement des PNJ
        self.werewolf_positions = []
        self.werewolfs = []

        for i in range(4):
            name = 'LG' + str(i)
            werewolf_position = tmx_data.get_object_by_name(name)
            self.werewolf_positions.append(werewolf_position)

        for werewolf_spawn in self.werewolf_positions:
            werewolf = NPC_Werewolf(werewolf_spawn.x, werewolf_spawn.y, 'Werewolf', self.screen, random.randint(1,5))
            self.werewolfs.append(werewolf)

        # Les collisions
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        #grouper les calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=2)
        self.group.add(self.player)
        self.werewolf_group = pygame.sprite.Group()
        self.werewolf_group.add(self.werewolfs)

        #Création d'une clock pour les FPS
        self.clock = pygame.time.Clock()

        #Etat cycle jour/nuit
        self.cycleState = "jour"

        #Etat du cycle des lunes
        self.cycleMoon = 0

        #Définition du tick de départ de l'horloge
        self.start_ticks = pygame.time.get_ticks()
        
    
    def run(self):
        running = True

        while running:
            #Limiter à 60 fps
            self.clock.tick(60)
            #gestion des cycles jour/nui
            self.switch_cycle()

            #centrer la caméra sur le joueur
            self.group.center(self.player.rect)
            #dessiner les calques
            self.group.draw(self.screen)
            #sauvegarde localisation joueur
            self.player.save_location()
            #gestion des touches
            self.handle_input()
            #maj des loups
            self.move_werewolfs()
            
            self.refresh()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # attack
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()

                    clicked_sprites = [s for s in self.werewolf_group if s.rect.collidepoint(pos)]
                    for werewolf in clicked_sprites:
                        self.player.attack(werewolf)

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

                # Change to werewolf
                for werewolf in self.werewolf_group:
                    werewolf.transform(self.cycleMoon)
            
            else:
                self.cycleState = "jour"

                for werewolf in self.werewolf_group:
                    werewolf.transform(6)

    def move_werewolfs(self):
        if self.cycleState == "nuit":
            for werewolf in self.werewolf_group:
                werewolf.move_npc(self.player)

    def refresh(self):
        #Update entities

        self.group.update()
        self.werewolf_group.update()

        #Blit entities
        self.screen.blit(self.player.image, self.player.rect)
        for werewolf in self.werewolf_group:
            self.screen.blit(werewolf.image, werewolf.rect)

        #afficher l'inventaire
        Inventory.open(self.screen, self.player.inventory)

        # Vérification des collisions
        for sprite in self.group.sprites():
            if sprite not in self.werewolfs:
                if sprite.feet.collidelist(self.walls) > -1:
                    sprite.move_back()

                #Degats sur le joueur
                for werewolf in self.werewolf_group:
                    if self.player.rect.colliderect(werewolf.rect) and werewolf.state == "WW":
                        self.player.take_damage(werewolf.damage, werewolf.position[0], werewolf.position[1])

        # actualisation
        # pygame.display.flip()
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

        while runPause:
            self.screen.blit(background_img, (0, 0))
            if resume_button.draw(self.screen):
                runPause = False
            if leave_button.draw(self.screen):
                sys.exit(2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(2)
            
            pygame.display.update()
