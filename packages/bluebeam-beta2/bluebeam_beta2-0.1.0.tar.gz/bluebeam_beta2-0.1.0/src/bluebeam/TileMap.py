import pygame
import pytmx
import os
from pytmx.util_pygame import load_pygame

from bluebeam.objects import Block
from math import floor, ceil

class TileMap:
    def __init__(self, globals, level, filename="TestMap.tmx"):
        self.globals = globals
        self.level = level
        #self.sourceDir = os.getcwd()
        self.sourceFileDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.map_dir = os.path.join(self.sourceFileDir, "bluebeam/tilemap_resources/")
        #print("hey", self.sourceFileDir)
        #self.tiled_map = load_pygame("tilemap_resources/" + filename)
        self.tiled_map = load_pygame(self.map_dir + filename)

        self.width  = self.tiled_map.width
        self.height = self.tiled_map.height

        # Used as a way to calculate the corners of the screen given camera position
        (screen_width, screen_height) = globals.screen_size
        self.screen_size = pygame.math.Vector2(screen_width, screen_height)

        self._load_gid_map()
        self._load_block_map()

    # Create 2d array of Image Placement
    def _load_gid_map(self):
        # Initialize empty 2d list of tiles
        self.tiles = [[0 for j in range(self.tiled_map.height)] for i in range(self.tiled_map.width )]

        # Populate 2d list of tiles
        max_gid = 0
        for layer in self.tiled_map.layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    if (gid):
                        self.tiles[x][y] = gid
                        if (gid > max_gid): max_gid = gid
        self._load_images(max_gid)

    # Load tile images used in the tilemap
    def _load_images(self, max_gid):
        self.images = []
        for gid in range(max_gid + 1):
            img = self.tiled_map.get_tile_image_by_gid(gid)
            if (img != None):
                img = img.convert()
            self.images.append(img)

    # Create list of Collision Blocks
    def _load_block_map(self):
        for tile_object in self.tiled_map.objects:
            if tile_object.name == "wall":
                pos = (tile_object.x, tile_object.y)
                block = Block(self.globals, self.level, pos, tile_object.width, tile_object.height)
                self.level.append(block)

    def load_player_pos(self):
        for tile_object in self.tiled_map.objects:
            if(tile_object.name == "player"):
                return pygame.math.Vector2(tile_object.x, tile_object.y)

    def load_pickup_info(self):
        pickups = []
        for tile_object in self.tiled_map.objects:
            if(tile_object.name == "pickup"):
                pos = pygame.math.Vector2(tile_object.x+50, tile_object.y+50)
                tup = (tile_object.type, pos)
                pickups.append(tup)
        return pickups

    def load_enemy_info(self):
        enemies = []
    
        for tile_object in self.tiled_map.objects:
            if (tile_object.name == "enemy"):
                pos = pygame.math.Vector2(tile_object.x+50, tile_object.y+50)
                enemies.append( (tile_object.type, pos) )
        return enemies

    # Draw the tiles on the screen
    def render(self, screen, camera_offset):
        (xmin, xmax, ymin, ymax) = self.calc_render_indices(camera_offset)
        for i in range(xmin, xmax):
            for j in range(ymin, ymax):
                gid = self.tiles[i][j]
                tile = self.images[gid]
                true_pos = pygame.math.Vector2(i * 64, j * 64)
                screen_pos = true_pos - camera_offset
                screen.blit(tile, screen_pos)

    def calc_render_indices(self, camera_offset):
        top_left_coords  = camera_offset
        bot_right_coords = camera_offset + self.screen_size

        # Convert screen Coordinates to Valid Tilemap coordinates
        xmin = max( floor(top_left_coords.x / 64), 0           )
        xmax = min( ceil(bot_right_coords.x / 64), self.width  )
        ymin = max( floor(top_left_coords.y / 64), 0           )
        ymax = min( ceil(bot_right_coords.y / 64), self.height )

        return (xmin, xmax, ymin, ymax)
