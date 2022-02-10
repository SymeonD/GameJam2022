from dataclasses import dataclass
from Model.NPC import NPC
from Model.NPC_Werewolf import NPC_Werewolf
from re import S
import pygame, pytmx, random

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
    group: pygame.sprite.Group()
    tmx_data: pytmx.TiledMap
    tmx_data_element: pytmx.TiledTileLayer
    portals: list[Portal]
    npc: list[NPC]

class MapManager:

    def __init__(self, screen, player):
        self.maps = dict() # town -> ["town_day","town_night"]
        self.screen = screen
        self.player = player
        self.timeState = 0
        self.current_map = "town"
        self.npc_group = pygame.sprite.Group()

        #chargement des maps
        self.tmx_data = None
        self.tmx_data_element = []
        self.register_map("town_day", portals=[
            Portal(from_world="town_day", origin_point="enter_medium_house", target_world="medium_house", teleport_point="spawn_medium_house"),
            Portal(from_world="town_day", origin_point="enter_small_house", target_world="small_house", teleport_point="spawn_small_house"),
            Portal(from_world="town_day", origin_point="enter_big_house", target_world="big_house", teleport_point="spawn_big_house"),
            Portal(from_world="town_day", origin_point="enter_forest_day", target_world="forest_day", teleport_point="spawn_forest_day")
        ])
        self.register_map("town_night", portals=[
            Portal(from_world="town_night", origin_point="enter_medium_house", target_world="medium_house", teleport_point="spawn_medium_house"),
            Portal(from_world="town_night", origin_point="enter_small_house", target_world="small_house", teleport_point="spawn_small_house"),
            Portal(from_world="town_night", origin_point="enter_big_house", target_world="big_house", teleport_point="spawn_big_house"),
            Portal(from_world="town_night", origin_point="enter_forest_night", target_world="forest_night", teleport_point="spawn_forest_night")
        ])

        self.register_map("forest_day", portals=[
            Portal(from_world="forest_day", origin_point="exit_forest_day", target_world="town_day",
                   teleport_point="spawn_exit_forest_day")
        ])
        self.register_map("forest_night", portals=[
            Portal(from_world="forest_night", origin_point="exit_forest_night", target_world="town_night", teleport_point="spawn_exit_forest_night"),
            Portal(from_world="forest_night", origin_point="enter_jail", target_world="jail", teleport_point="spawn_jail")
        ])

        self.register_map("jail", portals=[
            Portal(from_world="jail", origin_point="exit_jail", target_world="forest_night", teleport_point="spawn_exit_jail")
        ])
        self.register_map("jail", portals=[
            Portal(from_world="jail", origin_point="exit_jail", target_world="forest_night",
                   teleport_point="spawn_exit_jail")
        ])

        self.register_map("medium_house", portals=[
            Portal(from_world="medium_house", origin_point="exit_medium_house", target_world="town_day", teleport_point="spawn_exit_medium_house")
        ])
        self.register_map("medium_house", portals=[
            Portal(from_world="medium_house", origin_point="exit_medium_house", target_world="town_day",
                   teleport_point="spawn_exit_medium_house")
        ])

        self.register_map("small_house", portals=[
            Portal(from_world="small_house", origin_point="exit_small_house", target_world="town_day", teleport_point="spawn_exit_small_house")
        ])
        self.register_map("small_house", portals=[
            Portal(from_world="small_house", origin_point="exit_small_house", target_world="town_day",
                   teleport_point="spawn_exit_small_house")
        ])
        
        self.register_map("big_house", portals=[
            Portal(from_world="big_house", origin_point="exit_big_house", target_world="town_day", teleport_point="spawn_exit_big_house")
        ])
        self.register_map("big_house", portals=[
            Portal(from_world="big_house", origin_point="exit_big_house", target_world="town_day",
                   teleport_point="spawn_exit_big_house")
        ])


        self.renderedmap = self.renderWholeTMXMapToSurface(self.maps[self.current_map][self.timeState].tmx_data)
        self.rendered_elements = self.maps[self.current_map][self.timeState].tmx_data_element

        self.teleport_player("player")

    def register_map(self, name, portals=[]) :
         # Charger la map
        self.tmx_data = pytmx.util_pygame.load_pygame(f"Ressources/{name}.tmx")
        self.tmx_data_element = []
        for tile_layer in self.tmx_data.get_layer_by_name("top"):
            self.tmx_data_element = tile_layer

        # Les collisions
        walls = []
        npc_list = []
        for obj in self.tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        #Gestion des npc
            if obj.type == "spawn_point":
                if random.randint(1, 2) == 1:
                    npc_list.append(NPC(obj.x, obj.y, "npc", self.screen, self.player))
                else:
                    npc_list.append(NPC_Werewolf(obj.x, obj.y, "werewolf", self.screen, random.randint(1,5), self.player))

        #group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=6)
        group = pygame.sprite.Group()
        group.add(self.player)
        group.add(npc_list)

        self.npc_group.add(npc_list)

        # Creer un objet Map
        maplist = []
        map = Map(name, walls, group, self.tmx_data, self.tmx_data_element, portals, npc_list)
        name = name.split('_')[0]
        maplist.append(map)
        if name in self.maps:
            map.group = self.maps[name][0].group
            maplist.append(self.maps[name][0])
            self.maps[name] = maplist
        else:
            self.maps[name] = maplist

    '''
    - Creer map à partir de tmx data
    '''

    # Convert HTML-like colour hex-code to integer triple tuple
    # E.g.: "#892da0" -> ( 137, 45, 160 )
    def hexToColour(self, hash_colour):
        red = int(hash_colour[1:3], 16)
        green = int(hash_colour[3:5], 16)
        blue = int(hash_colour[5:7], 16)
        return (red, green, blue)

    # Given a loaded pytmx map, create a single image which holds a
    # rendered version of the whole map.
    def renderWholeTMXMapToSurface(self, tmx_map):
        width = tmx_map.tilewidth * tmx_map.width
        height = tmx_map.tileheight * tmx_map.height

        # This surface could be huge
        surface = pygame.Surface((width, height))

        # Some maps define a base-colour, if so, fill the background with it
        if (tmx_map.background_color):
            colour = tmx_map.background_color
            if (type(colour) == str and colour[0].startswith('#')):
                colour = self.hexToColour(colour)
                surface.fill(colour)
            else:
                print("ERROR: Background-colour of [" + str(colour) + "] not handled")

        # For every layer defined in the map
        for layer in tmx_map.visible_layers:
            # if the Layer is a grid of tiles
            if (isinstance(layer, pytmx.TiledTileLayer)):
                for x, y, gid in layer:
                    tile_bitmap = tmx_map.get_tile_image_by_gid(gid)
                    if (tile_bitmap):
                        surface.blit(tile_bitmap, (x * tmx_map.tilewidth, y * tmx_map.tileheight))
            # if the Layer is a big(?) image
            elif (isinstance(layer, pytmx.TiledImageLayer)):
                image = get_tile_image_by_gid(layer.gid)
                if (image):
                    surface.blit(image, (0, 0))
            # Layer is a tiled group (woah!)
            elif (isinstance(layer, pytmx.TiledObjectGroup)):
                print("ERROR: Object Group not handled")

        return surface

    '''
    - Getters
    '''
    def get_map(self):
        return self.maps[self.current_map][self.timeState]

    def get_group(self):
        return self.get_map().group

    def get_walls(self):
        return self.get_map().walls

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    def get_group_npc(self):
        return self.npc_group

    '''
    - Dessin du groupe + centrage sur le joueur
    '''
    def draw(self):
        #self.get_group().center(self.player.rect.center)
        #self.get_group().draw(self.screen)
        print("draw")

    '''
    - Update de la map
    '''
    def update(self):
        #draw background map
        self.screen.blit(self.renderedmap, (0, 0))

        self.get_group().update()
        self.check_collisions()
        #self.check_time()

        #draw top layer
        for x, y, tile in self.get_map().tmx_data.get_layer_by_name("top").tiles():
            tile.set_colorkey([0, 0, 0])
            self.screen.blit(tile, (x*16, y*16))

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
            if portal.from_world.split('_')[0] == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world.split('_')[0]
                    self.renderedmap = self.renderWholeTMXMapToSurface(self.maps[self.current_map][self.timeState].tmx_data)
                    self.rendered_elements = self.maps[self.current_map][self.timeState].tmx_data_element
                    self.teleport_player(copy_portal.teleport_point)


        for sprite in self.get_group().sprites():
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def change_time(self):
        if self.timeState == 1:
            self.timeState = 0
        else:
            self.timeState = 1

        '''
        if self.timeState == "jour" and self.current_map == "town_night" or self.current_map == "forest_night":
            if self.current_map == "town_night":
                self.current_map = "town_day"
            elif self.current_map == "forest_night":
                self.current_map = "forest_day"

        if self.timeState == "nuit" and self.current_map == "town_day" or self.current_map == "forest_day":
            if self.current_map == "town_day":
                self.current_map = "town_night"
            elif self.current_map == "forest_day":
                self.current_map = "forest_night"
        '''

        self.renderedmap = self.renderWholeTMXMapToSurface(self.maps[self.current_map][self.timeState].tmx_data)
        self.rendered_elements = self.maps[self.current_map][self.timeState].tmx_data_element
        
            

