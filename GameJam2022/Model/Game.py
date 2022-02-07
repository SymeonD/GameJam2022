import pygame
import pygame_ai.steering.kinematic
import pytmx
import pyscroll

import NPC_Werewolf
import bouton
from GameJam2022.Model import Player1, CircleNPC


class Game:

    def __init__(self):

        self.screen = pygame.display.set_mode((1024, 768))
        pygame.display.set_caption("WereWolf")

        # Charger la carte du jeu
        tmx_data = pytmx.util_pygame.load_pygame("../Ressources/MapTest.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())

        #Spawn player
        player_position = tmx_data.get_object_by_name('player')
        #self.player = Player.Player(player_position.x, player_position.y, "Player1")
        self.player = Player1.Player()

        #Spawn Werewolfs
        werewolf_positions = []
        self.werewolfs = []
        for i in range(4):
            name = 'LG'+str(i)
            werewolf_position = tmx_data.get_object_by_name(name)
            werewolf_positions.append(werewolf_position)

        for werewolf_spawn in werewolf_positions:
            werewolf = NPC_Werewolf.NPC_Werewolf(werewolf_spawn.x, werewolf_spawn.y, 'Werewolf')
            self.werewolfs.append(werewolf)

        """
        #Add entities to the screen
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        self.group.add(self.player)

        for werewolf in self.werewolfs:
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
        elif pressed[pygame.K_p]:
            self.paused()
    """

    def handle_input(self, player_steering): #Version GameObject
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_steering.linear[1] -= self.player.max_accel
            self.player.change_animation('up')
        if keys[pygame.K_a]:
            player_steering.linear[0] -= self.player.max_accel
            self.player.change_animation('left')
        if keys[pygame.K_s]:
            player_steering.linear[1] += self.player.max_accel
            self.player.change_animation('down')
        if keys[pygame.K_d]:
            self.player.change_animation('right')
            player_steering.linear[0] += self.player.max_accel
        if keys[pygame.K_p]:
            self.paused()

    def run(self):
        clock = pygame.time.Clock()
        running = True

        #Create player steering
        player_steering = pygame_ai.steering.kinematic.SteeringOutput()

        #Game Objects
        player = Player1.Player(pos = (1024//2, 768//2))
        circle = CircleNPC.CircleNPC(pos = (1024//4, 768//4))

        circle.ai = pygame_ai.steering.kinematic.Arrive(circle, player)

        while running:
            tick = clock.tick(60) / 1000
            player_steering.reset()

            #self.handle_input()
            self.handle_input(player_steering) #Version GameObject
            #self.group.update()
            #self.group.center(self.player.rect)
            #self.group.draw(self.screen)
            pygame.display.flip()

            #create drag
            drag = pygame_ai.steering.kinematic.Drag(15)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            player.update(player_steering, tick)
            circle.update(tick)

            player.steer(drag.get_steering(player), tick)
            circle.steer(drag.get_steering(circle), tick)

            self.screen.blit(player.image, player.rect)
            self.screen.blit(circle.image, circle.rect)

        pygame.quit()

    def paused(self):
        run = True
        #chargement de l'image de fond
        background_img = pygame.image.load('../Ressources/bg.jpg').convert_alpha()

        #chargement des images pour boutons
        resume_img = pygame.image.load('../Ressources/start_btn.png').convert_alpha()
        leave_img = pygame.image.load('../Ressources/exit_btn.png').convert_alpha()

        #creer les boutons
        resume_button = bouton.Button(100, 200, resume_img, 0.5)
        leave_button = bouton.Button(600, 200, leave_img, 0.5)

        while run:

            self.screen.blit(background_img, (0, 0))

            if resume_button.draw(self.screen):
                self.run()
            if leave_button.draw(self.screen):
                run = False


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            pygame.display.update()
            
        pygame.quit()
