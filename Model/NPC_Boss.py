import pygame
import math
from Model.NPC import NPC as parent

class NPC_Boss(parent):

    def __init__(self, x, y, name, screen, player):
        super().__init__(x, y, name, screen, player)

        # init pnj boss image
        self.form = "npc"
        self.updateImageBoss('Ressources/perso/boss.png', 32, 32)
        self.damage_image = (self.image.copy()).convert_alpha()
        self.damage_image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        self.damage_image.fill((255, 0, 0, 0), None, pygame.BLEND_RGBA_ADD)
        self.rect = self.image.get_rect()

        self.type = 'boss'
        self.target = player
        self.state = 'boss'

        self.damage = 10
        self.attack_speed = 1/60
        self.attack_cooldown = 1

        self.old_position = self.position.copy()
        self.animating = False

        self.ww_health = 5000
        self.ww_max_health = 5000

        self.is_dead = False

    def transform(self):
        self.form = "boss_werewolf"
        self.updateImageBoss('Ressources/perso/boss_werewolf.png', 55, 54, 0, 0)
        self.damage_image = (self.image.copy()).convert_alpha()
        self.damage_image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        self.damage_image.fill((255, 0, 0, 0), None, pygame.BLEND_RGBA_ADD)
        self.rect = self.image.get_rect()

    def update(self):
        super().update()

        self.updateTarget(self.player)
        if self.targetDistance < 100 and self.form == "npc":
            self.transform()
        if self.form == "boss_werewolf":
            self.move_npc(self.player)

        # update attack cooldown
        if self.attack_cooldown < 1:
            self.attack_cooldown += self.attack_speed

        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

        if self.health <= 0:
            self.is_dead = True
            self.kill()

    def updateTarget(self, player1):
        if self.target:
            if math.hypot(self.position[0] - player1.position[0],
                          self.position[1] - player1.position[1]) < math.hypot(self.position[0] -
                                                                               self.target.position[0],
                                                                               self.position[1] -
                                                                               self.target.position[1]):
                if self.target != player1:
                    self.target = player1
        else:
            self.target = player1
        self.targetDistance = math.hypot(self.position[0] - self.target.position[0],
                                         self.position[1] - self.target.position[1])

    def move_npc(self, player1):
        self.save_location()
        self.updateTarget(player1)
        rotation = 75
        if self.targetDistance < 1000:
            if self.targetDistance < 200:
                self.attack(player1)
            self.animating = True
            if self.position[1] > self.target.position[1]:
                self.position[1] -= self.speed
                self.change_animation("up")
                self.current_direction = "up"
            if self.position[1] < self.target.position[1]:
                self.position[1] += self.speed
                self.change_animation("down")
                self.current_direction = "down"
            if self.position[0] > self.target.position[0]:
                self.position[0] -= self.speed
                if self.position[1] - self.target.position[1] < rotation and self.position[1] - \
                        self.target.position[1] > -rotation:
                    self.change_animation("left")
                    self.current_direction = "left"
            if self.position[0] < self.target.position[0]:
                self.position[0] += self.speed
                if self.position[1] - self.target.position[1] < rotation and self.position[1] - \
                        self.target.position[1] > -rotation:
                    self.change_animation("right")
                    self.current_direction = "right"
            else:
                self.change_animation("down")
                self.animating = False

    def save_location(self):
        self.old_position = self.position.copy()

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_forth(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def attack(self, player):
        if self.attack_cooldown >= 1:
            player.take_damage(self.damage, self.position[0], self.position[1])
            self.attack_cooldown = 0

    def updateImageBoss(self, ressource, sprite_size_x, sprite_size_y, decal_x=0, decal_y=0):
        self.sprite_size_x = sprite_size_x
        self.sprite_size_y = sprite_size_y
        self.sprite_sheet = pygame.image.load(ressource)
        self.image = self.get_image(0 + decal_x, 0 + decal_y)
        self.image.set_colorkey([0, 0, 0])
        if self.form == "npc":
            self.images = {
                'down': [self.get_image(0 + decal_x, 0 + decal_y),
                         self.get_image(sprite_size_x + decal_x, 0 + decal_y),
                         self.get_image(sprite_size_x * 2 + decal_x, 0 + decal_y)],
                'up': [self.get_image(0 + decal_x, (3 * self.sprite_size_y) + decal_y),
                       self.get_image(sprite_size_x + decal_x, (3 * self.sprite_size_y) + decal_y),
                       self.get_image(sprite_size_x * 2 + decal_x, (3 * self.sprite_size_y) + decal_y)],
                'right': [self.get_image(0 + decal_x, (2 * self.sprite_size_y) + decal_y),
                          self.get_image(sprite_size_x + decal_x, (2 * self.sprite_size_y) + decal_y),
                          self.get_image(sprite_size_x * 2 + decal_x, (2 * self.sprite_size_y) + decal_y)],
                'left': [self.get_image(0 + decal_x, self.sprite_size_y + decal_y),
                         self.get_image(sprite_size_x + decal_x, self.sprite_size_y + decal_y),
                         self.get_image(sprite_size_x * 2 + decal_x, self.sprite_size_y + decal_y)]
            }
        else:
            self.images = {
                'down': [self.get_image(0 + decal_x, 0 + decal_y),
                         self.get_image((4 * sprite_size_x) + decal_x, 0 + decal_y),
                         self.get_image(0 + decal_x, (3 * self.sprite_size_y) + decal_y)],
                'up': [self.get_image(sprite_size_x + decal_x, 0 + decal_y),
                       self.get_image((5*sprite_size_x) + decal_x, 0 + decal_y),
                       self.get_image((6*sprite_size_x) + decal_x, self.sprite_size_y + decal_y)],
                'right': [self.get_image((2*sprite_size_x) + decal_x, 0 + decal_y),
                          self.get_image((6*sprite_size_x) + decal_x, 0+ decal_y),
                          self.get_image(0 + decal_x, (2 * self.sprite_size_y) + decal_y)],
                'left': [self.get_image((3*sprite_size_x) + decal_x, 0 + decal_y),
                         self.get_image(0 + decal_x, self.sprite_size_y + decal_y),
                         self.get_image(sprite_size_x + decal_x, (2*self.sprite_size_y) + decal_y)]
            }
        self.original_image = self.image