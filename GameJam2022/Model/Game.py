import pygame
import pytmx
import pyscroll

import Player
import NPC_Werewolf
import NPC


class Game:

    def __init__(self):

        self.screen = pygame.display.set_mode((1024, 768));
        pygame.display.set_caption("WereWolf");

        # Charger la carte du jeu
        tmx_data = pytmx.util_pygame.load_pygame("../Ressources/MapTest.tmx");
        map_data = pyscroll.data.TiledMapData(tmx_data);
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size());

        #Spawn player
        player_position = tmx_data.get_object_by_name('player')
        self.player = Player.Player(player_position.x, player_position.y, "Player1")

        #Spawn Werewolfs
        werewolf_positions = []
        self.werewolfs = []
        for i in range(4):
            name = 'LG'+str(i)
            werewolf_position = tmx_data.get_object_by_name(name)
            werewolf_positions.append(werewolf_position)

        for werewolf_spawn in werewolf_positions:
            npc = NPC.NPC(werewolf_spawn.x, werewolf_spawn.y, 'Werewolf')
            #werewolf = NPC_Werewolf.NPC_Werewolf(npc)
            self.werewolfs.append(npc)

        #Add entities to the screen
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        self.group.add(self.player)

        for werewolf in self.werewolfs:
            print(werewolf.name)
            self.group.add(werewolf)

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation('up')
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation('down')
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')

    def run(self):
        clock = pygame.time.Clock()
        running = True;

        while running:
            self.handle_input()
            self.group.update()
            self.group.center(self.player.rect)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False;

            clock.tick(60)

        pygame.quit()
