import tcod as libtcod
from random import randint
from map_objects.rectangle import Rect
from map_objects.tile import Tile
from entity import Entity
from colors import colors
import ai

class GameMap:
    def __init__(self, width, height, entities, items):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        self.entities = entities
        self.items = items

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player):
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            # random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # random position without going out of the boundaries of the map
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            # "Rect" class makes rectangles easier to work with
            new_room = Rect(x, y, w, h)

            # run through the other rooms and see if they intersect with this one
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # this means there are no intersections, so this room is valid

                # "paint" it to the map's tiles
                self.create_room(new_room)

                # center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    # this is the first room, where the player starts at
                    player.x = new_x
                    player.y = new_y
                else:
                    # all rooms after the first:
                    # connect it to the previous room with a tunnel

                    # center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # flip a coin (random number that is either 0 or 1)
                    if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                        # finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

    def create_room(self, room):
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

                i = randint(0, 3)
                if i == 1:
                    self.items.insert(0, Entity(x, y, '.', "Stone", libtcod.grey))
                elif i == 2:
                    self.items.insert(0, Entity(x, y, '"', "Grass", colors.get('grass')))

                i = randint(0, 60)
                if i == 1:
                    bot = Entity(x, y, 'W', "WANDERER", libtcod.green, ai.wanderer_text)
                    self.entities.insert(0, bot)
                elif i == 2:
                    bot = Entity(x, y, 'G', "GATHERER", libtcod.green, ai.gatherer_text)
                    self.entities.insert(0, bot)
                elif i == 3:
                    bot = Entity(x, y, 'M', "MINER", libtcod.green, ai.miner_text)
                    self.entities.insert(0, bot)

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def is_blocked(self, x, y):
        if x == 0 or y == 0:
            return True
        if x == self.width-1 or y == self.height-1:
            return True
        if self.tiles[x][y].blocked:
            return True
        for entity in self.entities:
            if entity.x == x and entity.y == y and entity.blocking:
                return True

        return False
