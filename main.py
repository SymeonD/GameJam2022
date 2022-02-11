import pygame


from Model.Menu import Menu


if __name__ == '__main__':
	pygame.init()

	# creation de la fenetre du jeu
	# dimension de la fenetre
	SCREEN_WIDTH = 1024
	SCREEN_HEIGHT = 768
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

	menu = Menu()
	menu.menu(screen)
	

	
