import pygame
import sys

#ajout du repertoire modele au systempath

sys.path.insert(0, '../Model')

#importation de la classe bouton
import bouton
from GameJam2022.Model.Game import Game

pygame.init()

#dimension de la fenetre
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('WereWolf')

#chargement de l'image de fond
background_img = pygame.image.load('../Ressources/bg.jpg').convert_alpha()

#chargement des images pour boutons
start_img = pygame.image.load('../Ressources/start_btn.png').convert_alpha()
exit_img = pygame.image.load('../Ressources/exit_btn.png').convert_alpha()

#creer les boutons
start_button = bouton.Button(100, 200, start_img, 0.5)
exit_button = bouton.Button(600, 200, exit_img, 0.5)

def mainMenu():
	run = True
	while run:

		#affiche l'image de fond
		screen.blit(background_img, (0, 0))

		#dessine les boutons crees precedemment
		if start_button.draw(screen):
			print('Lance le jeu')
			gameMain()
		if exit_button.draw(screen):
			run = False

		#gestion des evenements
		for ev in pygame.event.get():
			#quitte le jeu
			if ev.type == pygame.QUIT:
				run = False

		pygame.display.update()

	pygame.quit()

def gameMain():
	run = True
	gameImport = Game()
	while run:

		screen.blit(background_img, (0, 0))
		gameImport.run()

		for ev in pygame.event.get():
			#quitte le jeu
			if ev.type == pygame.QUIT:
				run = False

		pygame.display.update()

	pygame.quit()

mainMenu()