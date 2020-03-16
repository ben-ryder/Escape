# Ben-Ryder 2019
"""Defines player and enemies actions and movements
including control and path seeking."""
import random
import pygame

import constants
import paths

from project import game



# This should be inherited, not used directly.
# (Based of Player class taken from here:
# https://www.pygame.org/project-Rect+Collision+Response-1061-.html)

class BasePlayer:
    """Encompasses the key interface for all moving entities (ie player, enemies..)."""
    def __init__(self, position, start_vector, level):
        self.vector = start_vector
        self.linked_level = level
        self.rect = pygame.Rect(position[0], position[1], level.PLAYER_SIZE, level.PLAYER_SIZE)
        # default rect only to prevent IDE highlighting.
        #SHOULD BE OVERWRITTEN IN SUBCLASS INIT where assets are loaded!

    def update(self):
        """Update player position."""
        self.move()

    def move_by(self, x_change, y_change):
        """Move each axis separately. Note that this checks for collisions both times."""
        if x_change != 0:
            self.move_single_axis(x_change, 0)
        if y_change != 0:
            self.move_single_axis(0, y_change)

    def move(self):
        """Move 1 in the y direction."""
        self.move_by(self.vector[0], self.vector[1])

    def stop_horizontal(self):
        """Stop horizontal velocity."""
        self.vector[0] = 0

    def stop_vertical(self):
        """Stop veritcal velocity."""
        self.vector[1] = 0

    def move_single_axis(self, x_change, y_change):
        """Move the player checking for wall collsions first."""
        self.rect.x += x_change
        self.rect.y += y_change
        # If you collide with a wall, move out based on velocity
        for wall in self.linked_level.get_walls():
            if self.rect.colliderect(wall.rect):
                if x_change > 0:  # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                    self.vector[0] = 0
                if x_change < 0:  # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                    self.vector[0] = 0
                if y_change > 0:  # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                    self.vector[1] = 0
                if y_change < 0:  # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom
                    self.vector[1] = 0


# Custom Players (using specific sprite assets, so has certain hardcoded values + files)
class UserPLayer(BasePlayer):
    """Defines a custom player that uses hardcoded values and files."""
    def __init__(self, position, start_vector, level):
        super().__init__(position, start_vector, level)
        self.speed = 3

        # Sprite Image Setup
        self.image = pygame.image.load(paths.imagePath + "player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, [level.PLAYER_SIZE, level.PLAYER_SIZE])
        self.rect = self.image.get_rect().move(position)

    def move_up(self):
        """Move up based on speed."""
        self.move_by(0, -self.speed)

    def move_down(self):
        """Move down based on speed."""
        self.move_by(0, self.speed)

    def move_left(self):
        """Move left based on speed."""
        self.move_by(-self.speed, 0)

    def move_right(self):
        """Move right based on speed."""
        self.move_by(self.speed, 0)

    def draw(self, display):
        """Put the drawn image in square."""
        display.blit(self.image, [self.rect.x, self.rect.y])


class Timer:  # starts tracking from point of declaration.
    """Timer to check that game is still in progress."""
    def __init__(self, sec, mins=0, hrs=0):
        self.target = sec + mins*60 + hrs*60*60
        self.start = pygame.time.get_ticks()

    def has_ended(self):
        """Checks if game has ended."""
        sec = (pygame.time.get_ticks()-self.start)/1000
        return sec >= self.target


class PatrolTimer(Timer):  # starts tracking from point of declaration.
    """Used as timer for EnemyPatrol."""
    def __init__(self, sec, mins=0, hrs=0):
        super().__init__(sec, mins, hrs)
        self.active = False

    def is_active(self):
        """Is the timer active."""
        return self.active

    def set_new(self, sec):
        """Only seconds needed for patrol, so interface hides mins and hrs."""
        self.__init__(sec)
        self.active = True

    def end(self):
        """Has patrol ended."""
        self.active = False


class EnemyPatrol(BasePlayer):
    """Defines the patrol enemy which follows certain route on a timer."""
    def __init__(self, level, patrol):
        # level is custom object, requiring .format for grid format and .walls for collision_objects

        # Positioning unit on square of first point on its patrol
        position = game.get_pixel_position(level, patrol[0])
        position = [position[0] + level.ENEMY_PADDING/2, position[1] + level.ENEMY_PADDING/2]
        super().__init__(position, [0, 0], level)

        self.format = level.format  # Used for enemy to find paths. Assumes format never changes!

        self.speed = 1

        self.patrol = patrol  # list of key points to visit
        self.current_target = 0  # index of patrol list
        self.path = [] # list of all points between current patrol point and next point.
        # path works as stack. index 0 is always next square target
        # pop off when reached for next target.
        self.timer = PatrolTimer(0)
        # timer used to pause for so long on a square

        # Sprite Image Setup
        self.image = pygame.image.load(paths.imagePath + "enemy-patrol.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, [level.ENEMY_SIZE, level.ENEMY_SIZE])
        self.rect = self.image.get_rect().move(position)

        self.target_rect = pygame.Rect([0, 0, 0, 0])

    def update(self):
        self.move()

        if self.timer.is_active():
            if self.timer.has_ended():
                self.step_patrol()
                self.update_path()

        elif len(self.path) > 0:
            # Checking if reached next tile, if so stepping target to next in path.
            x_pos, y_pos = game.get_pixel_position(self.linked_level, self.path[0])
            self.target_rect = pygame.Rect(x_pos, y_pos, self.linked_level.TILE_SIZE, self.linked_level.TILE_SIZE)
            self.target_rect.inflate_ip(-self.linked_level.ENEMY_PADDING, -self.linked_level.ENEMY_PADDING)

            reached_target = False
            if self.rect.top <= self.target_rect .top and self.vector[1] < 0:
                reached_target = True
            elif self.rect.bottom >= self.target_rect.bottom and self.vector[1] > 0:
                reached_target = True
            elif self.rect.left <= self.target_rect.left and self.vector[0] < 0:
                reached_target = True
            elif self.rect.right >= self.target_rect.right and self.vector[0] > 0:
                reached_target = True

            if reached_target:
                self.step_path()
                # assigning so player is re-centered to tile if gone > boundary.
                self.rect = self.target_rect

        else:
            self.step_patrol()
            self.update_path()

    def step_path(self):
        """Pop the path from the stack."""
        self.path.pop(0)
        if len(self.path) > 0:
            self.update_vector()

    def update_vector(self):
        """Update direction of player/enemy."""
        if self.timer.is_active():
            self.vector = [0, 0]
        else:
            try:
                if game.get_tile_position(self.linked_level, self.rect.topleft)[0] < self.path[0][0]:
                    self.vector[0] = self.speed
                elif game.get_tile_position(self.linked_level, self.rect.topleft)[0] > self.path[0][0]:
                    self.vector[0] = -self.speed
                else:
                    self.stop_horizontal()

                if game.get_tile_position(self.linked_level, self.rect.topleft)[1] < self.path[0][1]:
                    self.vector[1] = self.speed
                elif game.get_tile_position(self.linked_level, self.rect.topleft)[1] > self.path[0][1]:
                    self.vector[1] = -self.speed
                else:
                    self.stop_vertical()
            except IndexError:
                print(self, self.path)

    def step_patrol(self):
        """Continue patrolling."""
        if self.current_target < len(self.patrol)-1:
            self.current_target += 1
        else:
            self.current_target = 0

    def update_path(self):
        """Create a path for the enemy."""
        if not isinstance(self.patrol[self.current_target], (int, float)):
            self.path = game.GridPath(self.format,
                                      game.get_tile_position(self.linked_level, self.rect.topleft),
                                      self.patrol[self.current_target], constants.WALL_FORMATS).get_path()
            self.timer.end()
        else:
            self.timer.set_new(self.patrol[self.current_target])

        self.update_vector()

    def draw(self, display):
        """Draw custom enemy."""
        display.blit(self.image, [self.rect.x, self.rect.y])
        # pygame.draw.rect(display, (100, 0, 0), self.rect, 1) # collision rect, for visual test only

        # Visual Testing
        # for x, y in self.path:
        #     x, y = game.get_pixel_position([x, y])
        #     pygame.draw.rect(display, (0, 150, 0), [x, y, level.TILE_SIZE, level.TILE_SIZE], 1)
        #
        # try:
        #     x, y = game.get_pixel_position(self.path[len(self.path)-1])
        #     target_tile_rect = pygame.Rect(x, y, level.TILE_SIZE, level.TILE_SIZE)
        #     pygame.draw.rect(display, (100, 0, 0), target_tile_rect, 2)
        # except IndexError:
        #     pass
        # #
        # pygame.draw.rect(display, (255, 255, 0), self.target_rect, 1)


def get_random_patrol(level, spawn, points=10):
    """Get random patrol."""
    random_patrol = [spawn]
    while len(random_patrol) < points:
        point = level.get_random_point()
        if game.GridPath(level.format, spawn, point, constants.WALL_FORMATS).get_path() is not None and \
                point != random_patrol[len(random_patrol)-1]:  # not the same as last tile
            # point accessible from enemy spawn
            random_patrol.append(point)
            if random.randrange(1, 10) < 4:  # 4/10 chance to pause.
                random_patrol.append(round(random.uniform(1, 3), 2))
    return random_patrol


class RandomPatrol(EnemyPatrol):
    """Defines the random patroller enemy."""
    def __init__(self, level, spawn, points=10):
        # level is custom object, requiring .format for grid format and .walls for collision_objects
        patrol = get_random_patrol(level, spawn, points)
        super().__init__(level, patrol)

        # Positioning unit i =n square of first point on its patrol
        position = game.get_pixel_position(self.linked_level, patrol[0])
        position = [position[0] + level.ENEMY_PADDING/2, position[1] + level.ENEMY_PADDING/2]

        self.format = level.format

        self.speed = 2

        self.patrol = patrol
        self.current_target = 0  # index of patrol list
        self.path = []  # works as stack. index 0 is always next square target, pop of when reached for next.

        # Sprite Image Setup
        self.image = pygame.image.load(paths.imagePath + "enemy-random.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, [level.ENEMY_SIZE, level.ENEMY_SIZE])
        self.rect = self.image.get_rect().move(position)

        self.target_tile_rect = pygame.Rect([0, 0, 0, 0])


class EnemySeeker(EnemyPatrol):
    """Defines the seeker enemy."""
    def __init__(self, level, player, spawn):
        super().__init__(level, [spawn])
        self.target_player = player
        # Sprite Image Setup
        self.image = pygame.image.load(paths.imagePath + "enemy-seeker.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, [level.ENEMY_SIZE, level.ENEMY_SIZE])
        self.rect = self.image.get_rect().move(game.get_pixel_position(self.linked_level, spawn))
        self.rect.move_ip(level.ENEMY_PADDING/2, level.ENEMY_PADDING/2)
        self.active = False  # if it can chase after the player

    def update(self):
        self.move()

        if self.active:
            if len(self.path) > 0:
                # Checking if reached next tile, if so stepping target to next in path.
                x_pos, y_pos = game.get_pixel_position(self.linked_level, self.path[0])
                self.target_rect = pygame.Rect(x_pos, y_pos, self.linked_level.TILE_SIZE, self.linked_level.TILE_SIZE)
                self.target_rect.inflate_ip(-self.linked_level.ENEMY_PADDING, -self.linked_level.ENEMY_PADDING)

                reached_target = False
                if self.rect.top <= self.target_rect .top and self.vector[1] < 0:
                    reached_target = True
                elif self.rect.bottom >= self.target_rect.bottom and self.vector[1] > 0:
                    reached_target = True
                elif self.rect.left <= self.target_rect.left and self.vector[0] < 0:
                    reached_target = True
                elif self.rect.right >= self.target_rect.right and self.vector[0] > 0:
                    reached_target = True

                if reached_target:
                    self.step_path()

                    # assigning so player is re-centered to tile if gone > boundary.
                    self.rect = self.target_rect
                    self.update_path()

            else:
                self.step_patrol()
                self.update_path()
        else:
            self.update_path()

    def update_vector(self):
        if not self.active:
            self.vector = [0, 0]
        else:
            if game.get_tile_position(self.linked_level, self.rect.topleft)[0] < self.path[0][0]:
                self.vector[0] = self.speed
            elif game.get_tile_position(self.linked_level, self.rect.topleft)[0] > self.path[0][0]:
                self.vector[0] = -self.speed
            else:
                self.vector[0] = 0

            if game.get_tile_position(self.linked_level, self.rect.topleft)[1] < self.path[0][1]:
                self.vector[1] = self.speed
            elif game.get_tile_position(self.linked_level, self.rect.topleft)[1] > self.path[0][1]:
                self.vector[1] = -self.speed
            else:
                self.vector[1] = 0

    def update_path(self):
        self.path = game.GridPath(self.format,
                                  game.get_tile_position(self.linked_level, self.rect.topleft),
                                  game.get_tile_position(self.linked_level, self.target_player.rect.center),
                                  constants.WALL_FORMATS
                                  ).get_path()
        if self.path is not None:
            self.active = True
        else:
            self.active = False

        self.update_vector()
