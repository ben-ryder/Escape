# Ben-Ryder 2019

import pygame
import random

import paths
import constants
import exceptions

from project import game
import project.data as data


class Tile:
    def __init__(self, level, row, col, filename):  # filename shows type of tile to be displayed.
        self.position = [row, col]
        self.image = pygame.image.load(paths.imagePath + filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, [level.TILE_SIZE, level.TILE_SIZE])
        self.rect = self.image.get_rect().move(game.get_pixel_position(level, [row, col]))

    def draw(self, display):
        display.blit(self.image, [self.rect.x, self.rect.y])


class IrregularWall:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)


class Exit(Tile):
    def __init__(self, level, row, col, direction):
        self.direction = direction  # either top, bottom, left or right (side of tile the exit is on)
        super().__init__(level, row, col, "exit-closed-%s.png" % self.direction)
        self.open = False

    def unlock(self):
        self.open = True
        size = self.image.get_size()  # keeping old size to apply to new image loaded
        self.image = pygame.image.load(paths.imagePath + "exit-open-%s.png" % self.direction).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)

    def is_closed(self):
        return not self.open

    def is_open(self):
        return self.open

    def get_open_walls(self):  # used in collisions when exit is open, wont use Exit.rect but whats returned here.
        top_rect = IrregularWall([self.rect.x, self.rect.y, self.rect.width, 1])
        bottom_rect = IrregularWall([self.rect.x, self.rect.y + self.rect.height - 1, self.rect.width, 1])
        right_rect = IrregularWall([self.rect.x + self.rect.width - 1, self.rect.y, 1, self.rect.height])
        left_rect = IrregularWall([self.rect.x, self.rect.y, 1, self.rect.height])

        if self.direction == "top":
            return [right_rect, bottom_rect, left_rect]
        elif self.direction == "right":
            return [top_rect, bottom_rect, left_rect]
        elif self.direction == "bottom":
            return [top_rect, right_rect, left_rect]
        elif self.direction == "left":
            return [top_rect, right_rect, bottom_rect]


class Key(Tile):  # mirrors Tile, but doesnt take filename. Done for clarity as a key is conceptually not a Tile
    def __init__(self, level,  row, col):
        super().__init__(level, row, col, "key.png")


class Level:
    def __init__(self, filename):
        self.data = data.load(filename)

        self.format = self.data["map-format"]
        self.enemies = self.data["enemies"]

        # Setting Display and Sizing based of level settings
        self.TILE_SIZE = self.data["tile-size"]
        self.MAP_SIZE = self.data["map-size"]

        self.DISPLAY_SIZE = [self.TILE_SIZE * self.MAP_SIZE[0], self.TILE_SIZE * self.MAP_SIZE[1]]

        self.PLAYER_SIZE = round(0.7 * self.TILE_SIZE)
        self.PLAYER_PADDING = self.TILE_SIZE - self.PLAYER_SIZE

        self.ENEMY_SIZE = round(0.5 * self.TILE_SIZE)
        self.ENEMY_PADDING = self.TILE_SIZE - self.ENEMY_SIZE

        # Map Setup
        self.walls = []
        self.path = []
        self.spawn = None
        self.exit = None

        spawn_number = 0
        exit_number = 0

        for row in range(len(self.format)):
            for col in range(len(self.format[0])):
                if self.format[row][col] == "1":
                    self.walls.append(Tile(self, row, col, "wall.png"))

                elif self.format[row][col] == "0":
                    self.path.append(Tile(self, row, col,  "path.png"))

                elif self.format[row][col] == "p":
                    self.path.append(Tile(self, row, col, "spawn-point.png"))
                    self.spawn = [row, col]
                    spawn_number += 1

                elif self.format[row][col] == "s":
                    self.path.append(Tile(self, row, col, "safe-point.png"))

                elif self.format[row][col] == "t":
                    self.exit = Exit(self, row, col, "top")
                    exit_number += 1

                elif self.format[row][col] == "l":
                    self.exit = Exit(self, row, col, "left")
                    exit_number += 1

                elif self.format[row][col] == "b":
                    self.exit = Exit(self, row, col, "bottom")
                    exit_number += 1

                elif self.format[row][col] == "r":
                    self.exit = Exit(self, row, col, "right")
                    exit_number += 1

                else:
                    raise exceptions.InvalidTileType("tile of invalid type %s defined" % self.format[row][col])

        # Validation Checking
        # Spawn and Exit defined correctly
        if spawn_number == 0:
            raise exceptions.SpawnNotFound("no spawn position found")
        elif spawn_number > 1:
            raise exceptions.ExcessSpawns("more than one spawn position defined")

        if exit_number == 0:
            raise exceptions.ExitNotFound("no exit found")
        elif exit_number > 1:
            raise exceptions.ExcessExits("more than one exit defined")

        # Spawn and exit are connected
        if not game.GridPath(self.format, self.spawn, self.exit.position, constants.WALL_FORMATS):
            raise exceptions.SpawnExitConnection("spawn and exit have no path between them")

        # Key Setup
        self.keys = []
        for key in self.data["keys"]:
            if self.format[key[0]][key[1]] != "0":
                raise exceptions.KeyPositionError("Key at %s is on an invalid tile" % key)

            elif not game.GridPath(self.format, self.spawn, key, constants.WALL_FORMATS):
                raise exceptions.KeyAccessError("Key at %s is unreachable" % key)

            else:
                self.keys.append(Key(self, key[0], key[1]))

    def update(self):
        if len(self.keys) == 0:
            self.exit.unlock()

    def get_walls(self):
        if self.exit.is_closed():
            return self.walls + [self.exit]
        else:
            return self.walls + self.exit.get_open_walls()  # IrregularWall shares interface needed with Tile

    def get_spawn(self):
        return self.spawn

    def get_random_point(self):
        row, col = [0, 0]  # assumes 0, 0 will always be a wall!
        while self.format[row][col] != "0":
            row, col = [random.randint(0, len(self.format) - 1), random.randint(0, len(self.format[0]) - 1)]
        return [row, col]  # point will always be a path tile

    def draw_paths(self, display):
        for tile in self.path:
            tile.draw(display)

        for key in self.keys:
            key.draw(display)

    def draw_walls(self, display):
        for tile in self.walls:
            tile.draw(display)

        self.exit.draw(display)

    def draw_grid(self, display):
        for row in range(len(self.format)):
            for col in range(len(self.format[1])):
                pygame.draw.line(display, constants.COLOURS["dark-gray"],
                                 [0, col * self.TILE_SIZE],
                                 [row * self.TILE_SIZE, col * self.TILE_SIZE], 1)

                pygame.draw.line(display, constants.COLOURS["dark-gray"],
                                 [row*self.TILE_SIZE, 0],
                                 [row*self.TILE_SIZE, constants.DISPLAY_SIZE[1]], 1)

"""
All levels are defined like this (and saved/loaded using JSON).
level = {

    tile_size: int
    map_size = [int, int]

    map_format: 2d array consisting of basic wall/path layout. ALSO INCLUDES: player_spawn and exit square.
        options for each tile:
            "1" = wall
            "0" = path
            "s" = safe point (wall for enemies, they can't move through it)
            "p" = spawn point (ONE ALLOWED)
            exits: (ONE ALLOWED)
            "t" = exit (though top of wall)
            "b" = exit (though bottom of wall)
            "l" = exit(though left of wall)
            "r" = exit (though right of wall)

    keys: list of positions ie: [x, y] on the map where the keys are placed.

    enemies: list containing all the enemies that populate the level.
        enemy:
            type: type of enemy
                options:
                    "ep": patrol  (an enemy who defaults to a set patrol)
                    "er": random  (an enemy who randomly explores the map)
                    "es": seeker  (an enemy who actively pursues the player)

            spawn: position ie: [x, y] enemy spawns in.

            FOR ENEMY type: "ep" (a patrolling enemy)
            patrol: list of patrol commands
                SPAWN IS ALWAYS FIRST COMMAND, doesn't need to be included.
                options for commands:
                    [x, y]: position to go to. (A* path finder is used to get from current to this position)
                    number: wait for the desired time, where number is in seconds (int or real)

                Patrolling Enemies loops continuously around the patrol

}

Level Validation:
When parsing the level at game creation, a series of validity checks are made, to ensure the level is playable.

map_format:
- check for invalid tile options.
- check for full outer wall so player can't escape the map. (exits can be at edge, they count as full walls when closed)
- check for only one spawn point
- check for only one exit

- check spawn point and exit are connected. (performs path find between points)

keys:
- check all positions are on map and a valid tile

- check all keys are collectible. (performs path find between every key and the spawn point)

enemies:
- check all enemies of valid type.
- check all enemies of type "p" (patrol) have a patrol.
- check all enemies have unique spawns, which are also not the players, and are on valid tiles.
FOR EACH ENEMY PATROL:
    - check patrol points are all on valid tiles
    - check a path can be found between all points
"""