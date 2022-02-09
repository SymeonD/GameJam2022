from dataclasses import dataclass
from re import S
import pygame, pytmx, pyscroll

@dataclass
class Portal:
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str

@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals : list[Portal]

class MapManager:

    def __init__(self, screen, player):
        self.maps = dict() # town_day -> Map("town_day", walls, group)
        self.screen = screen
        self.player = player
        self.current_map = "town_day"

        #chargement des maps
        self.register_map("town_day", portals=[
            Portal(from_world="town_day", origin_point="enter_house", target_world="medium_house", teleport_point="spawn_house")
        ])
        self.register_map("medium_house", portals=[
            Portal(from_world="medium_house", origin_point="exit_house", target_world="town_day", teleport_point="spawn_exit_house")
        ])

        self.teleport_player("player")

    def register_map(self, name, portals=[]) :
         # Charger la map
        tmx_data = pytmx.util_pygame.load_pygame(f"Ressources/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        #map_layer.zoom = 2

        # Les collisions
        walls = []
        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        '''
        # Dessiner les différents calques
            #gestion de la superposition du joueur avec le décor en fonction des calques
        if name == "town_day":
            dl = 6
        elif name == "medium_house":
            dl = 1

            -> PROBLEME RESOLU : 8 claques max avec le top
        '''

        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=6)
        group.add(self.player)

        # Creer un objet Map
        map = Map(name, walls, group, tmx_data, portals)
        self.maps[name] = map


    '''
    - Getters
    '''
    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_walls(self):
        return self.get_map().walls

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    '''
    - Dessin du groupe + centrage sur le joueur
    '''
    def draw(self):
        self.get_group().center(self.player.rect.center)
        self.get_group().draw(self.screen)
        
    '''
    - Update de la map
    '''
    def update(self):
        self.get_group().update()
        self.check_collisions()

    '''
    - Téléportation du joueur
    '''
    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    '''
    - Verification des collisions
    '''
    def check_collisions(self):
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)

        for sprite in self.get_group().sprites():
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()