import random

import pygame
import pytmx
import pyscroll

import sys

#ajout du repertoire modele au systempath

sys.path.insert(0, '../Model')

#importation de la classe bouton
import bouton
import Player
import NPC_Werewolf
import inventory

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

	# Etat du cycle jour nuit
	cycleState = "jour"

	# Etat du cycle des lunes
	cycleMoon = 0

	# Charger la carte du jeu
	tmx_data = pytmx.util_pygame.load_pygame("../Ressources/MapTest.tmx")
	map_data = pyscroll.data.TiledMapData(tmx_data)
	map_layer = pyscroll.orthographic.BufferedRenderer(map_data, screen.get_size())

	#create clock
	clock = pygame.time.Clock()

	# Get tick for 5 min cycles
	start_ticks=pygame.time.get_ticks()

	#Instatiate players
	player_position = tmx_data.get_object_by_name('player')
	player1 = Player.Player(player_position.x, player_position.y)
	player2 = Player.Player(player_position.x, player_position.y)

	#Instantiate werewolfs
	werewolf_positions = []
	werewolfs = []

	for i in range(4):
		name = 'LG' + str(i)
		werewolf_position = tmx_data.get_object_by_name(name)
		werewolf_positions.append(werewolf_position)

	for werewolf_spawn in werewolf_positions:
		werewolf = NPC_Werewolf.NPC_Werewolf(werewolf_spawn.x, werewolf_spawn.y, 'Werewolf')
		werewolfs.append(werewolf)

	#Create map group
	group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)

	"""
	#Add entity ai
	for werewolf in werewolfs:
		a=random.randint(1,2)
		if a == 1:
			werewolf.ai = pai.steering.kinematic.Arrive(werewolf, player1)
		else:
			werewolf.ai = pai.steering.kinematic.Arrive(werewolf, player2)
	"""

	# create inventory
	player_inventory = inventory.Inventory()

	while run:

		#Limit to 60 fps
		clock.tick(60)

		#Change daycycle state every 5 minute
		seconds = (pygame.time.get_ticks()-start_ticks)//1000
		if seconds > 300:
			print("Changement de cycle")
			start_ticks = pygame.time.get_ticks()
			if cycleState == "jour":
				cycleState = "nuit"

				#Mooncycle update
				cycleMoon += 1
				if cycleMoon > 5:
					cycleMoon = 1
					#Add special effects (super werewolves...)

				# Change to werewolf
				for werewolf in werewolfs:
					werewolf.transform(cycleMoon)
			else:
				cycleState = "jour"

		#Update map et centre
		group.update()
		group.center(player1.rect) #Attention centrage seulement sur le joueur 1
		group.draw(screen)

		#Quit
		for ev in pygame.event.get():
			#quitte le jeu
			if ev.type == pygame.QUIT:
				sys.exit(2)

		#Players control
		keys = pygame.key.get_pressed()
		if keys[pygame.K_w]:
			player1.move_player('up')
		if keys[pygame.K_a]:
			player1.move_player('left')
		if keys[pygame.K_s]:
			player1.move_player('down')
		if keys[pygame.K_d]:
			player1.move_player('right')

		if keys[pygame.K_UP]:
			player2.move_player('up')
		if keys[pygame.K_LEFT]:
			player2.move_player('left')
		if keys[pygame.K_DOWN]:
			player2.move_player('down')
		if keys[pygame.K_RIGHT]:
			player2.move_player('right')

		#Werewolf update
		for werewolf in werewolfs:
			werewolf.move_npc(player1, player2)

		#Menu pause
		if keys[pygame.K_p]:
			runPause = True
			# chargement de l'image de fond
			background_img = pygame.image.load('../Ressources/bg.jpg').convert_alpha()

			# chargement des images pour boutons
			resume_img = pygame.image.load('../Ressources/start_btn.png').convert_alpha()
			leave_img = pygame.image.load('../Ressources/exit_btn.png').convert_alpha()

			# creer les boutons
			resume_button = bouton.Button(100, 200, resume_img, 0.5)
			leave_button = bouton.Button(600, 200, leave_img, 0.5)

			while runPause:

				screen.blit(background_img, (0, 0))

				if resume_button.draw(screen):
					runPause = False
				if leave_button.draw(screen):
					sys.exit(2)

				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						sys.exit(2)

				pygame.display.update()

		#inventaire
		if keys[pygame.K_i]:
			runInventory = True

			screen.fill((0,0,0))
			player_inventory.draw(screen)
			
			mousex, mousey = inventory.pygame.mouse.get_pos()

			while runInventory:

				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						sys.exit(2)

				pygame.display.update()

		#Update entities
		player1.update()
		player2.update()
		for werewolf in werewolfs:
			werewolf.update()

		#Blit entities
		screen.blit(player1.image, player1.rect)
		screen.blit(player2.image, player2.rect)
		for werewolf in werewolfs:
			screen.blit(werewolf.image, werewolf.rect)

		#Update display
		pygame.display.update()

if __name__ == '__main__':
	pygame.init()
	mainMenu()
	pygame.quit()