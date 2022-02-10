from dataclasses import dataclass
from re import S
import pygame, pytmx#, pyscroll

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

class MapManager:

    def __init__(self, screen, player):
        self.maps = dict() # town_day -> Map("town_day", walls, group)
        self.screen = screen
        self.player = player
        self.current_map = "town_day"

        #chargement des maps
        self.tmx_data = None
        self.tmx_data_element = []
        self.register_map("town_day", portals=[
            Portal(from_world="town_day", origin_point="enter_house", target_world="medium_house", teleport_point="spawn_house")
        ])

        self.register_map("medium_house", portals=[
            Portal(from_world="medium_house", origin_point="exit_house", target_world="town_day", teleport_point="spawn_exit_house")
        ])

        self.renderedmap = self.renderWholeTMXMapToSurface(self.maps[self.current_map].tmx_data)
        self.rendered_elements = self.maps[self.current_map].tmx_data_element
        #self.rendered_elements = self.renderWholeTMXMapToSurface(self.maps[self.current_map].tmx_data_element)

        self.teleport_player("player")

    def register_map(self, name, portals=[]) :
         # Charger la map
        self.tmx_data = pytmx.util_pygame.load_pygame(f"Ressources/{name}.tmx")
        self.tmx_data_element = []
        for tile_layer in self.tmx_data.get_layer_by_name("top"):
            self.tmx_data_element = tile_layer
            #for tile_object in tile_layer:
            #    self.tmx_data_element.append(tile_object)
        #map_data = pyscroll.data.TiledMapData(self.tmx_data)
        #map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        #map_layer.zoom = 2

        # Les collisions
        walls = []
        for obj in self.tmx_data.objects:
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

        #group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=6)
        group = pygame.sprite.Group()
        group.add(self.player)

        # Creer un objet Map
        map = Map(name, walls, group, self.tmx_data, self.tmx_data_element, portals)
        self.maps[name] = map

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
        #self.get_group().center(self.player.rect.center)
        self.get_group().draw(self.screen)
        
    '''
    - Update de la map
    '''
    def update(self):
        self.screen.blit(self.renderedmap, (0, 0))
        for sprite in self.get_group().sprites():
            self.screen.blit(sprite.image, sprite.rect)
        for x, y, tile in self.get_map().tmx_data.get_layer_by_name("top").tiles():
            self.screen.blit(tile, (x*16, y*16))
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
                    self.renderedmap = self.renderWholeTMXMapToSurface(self.maps[self.current_map].tmx_data)
                    self.rendered_elements = self.maps[self.current_map].tmx_data_element
                    #self.rendered_elements = self.renderWholeTMXMapToSurface(self.maps[self.current_map].tmx_data_element)
                    self.teleport_player(copy_portal.teleport_point)

        for sprite in self.get_group().sprites():
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()