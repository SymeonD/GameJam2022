import pygame

from Model.Game import Game
from Model.Menu import Menu


if __name__ == '__main__':
	pygame.init()
	game = Game()
	menu = Menu()
	menu.menu(game.screen, game)
	

	
