# Ben-Ryder 2019

import os
import pygame
import time

import constants
import paths
import exceptions

from project import game

import pygame_gui


class Controller:
    def __init__(self, map_name):
        # Game Setup
        self.map_name = map_name
        self.level = game.Level(self.map_name)
        self.state = "game"

        # Display Setup
        self.display = pygame.display.set_mode(self.level.DISPLAY_SIZE)  # adapts to map size
        pygame.display.set_caption(constants.DISPLAY_NAME + " - " + os.path.basename(map_name))
        self.clock = pygame.time.Clock()
        self.back_button = pygame_gui.Button(paths.uiPath + "backwhite.png", paths.uiPath + "backwhite-hover.png", 5, 5)
        # self.back_button.resize(self.level.TILE_SIZE, self.level.TILE_SIZE)

        # Player Setup
        spawn = game.get_pixel_position(self.level, self.level.get_spawn())
        spawn = [position + self.level.PLAYER_PADDING/2 for position in spawn]  # center player in tile
        self.player = game.UserPLayer(spawn, [0, 0], self.level)

        # Enemy Setup
        self.enemies = []
        for enemy in self.level.enemies:
            if enemy["type"] == "er":
                self.enemies.append(game.RandomPatrol(self.level, enemy["spawn"]))

            elif enemy["type"] == "es":
                self.enemies.append(game.EnemySeeker(self.level, self.player, enemy["spawn"]))

            elif enemy["type"] == "ep":
                self.enemies.append(game.EnemyPatrol(self.level, enemy["patrol"]))

            else:
                raise exceptions.InvalidEnemyType("%s not recognised" % enemy["type"])

        # Enemy Validation TODO: Validation. All enemies need checking (left for now as editor prevents this)
        # All enemy spawns on valid tile
        # For all patrols:
        # each point is valid tile position
        # path can be made between each joining point

    def play(self):
        while self.state not in ["menu", "quit"]:
            if self.state in ["won", "lost"]:
                self.state = game.GameOverMenu(self.display, self.state).get_option()  # run menu, get option when done
                if self.state == "game":
                    self.__init__(self.map_name)

            else:
                self.handle_events()

                self.player.update()
                self.level.update()

                for enemy in self.enemies:
                    enemy.update()
                    if self.player.rect.colliderect(enemy.rect):
                        self.state = "lost"

                for key in self.level.keys:
                    if self.player.rect.colliderect(key.rect):
                        self.level.keys.remove(key)

                if self.level.exit.is_open():
                    if self.level.exit.rect.contains(self.player.rect):
                        self.state = "won"

                self.draw()

        return self.state

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = "quit"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or (event.key == pygame.K_F4 and event.mod == pygame.KMOD_ALT):
                    self.state = "quit"
                self.handle_key_down(event.key)  # handles only pygame.KEYDOWN, not persistently pressed keys.

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(pygame.mouse.get_pos())

        self.handle_pressed_keys()  # pygame.key.get_pressed not pygame.KEYDOWN

    def handle_key_down(self, key):
        if key == pygame.K_v:
            pygame.image.save(self.display, "background-%s.png" % time.time())  # adds timestamp to make it unique

    def handle_pressed_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player.move_up()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player.move_down()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left()

    def handle_click(self, position):  # TODO: pygame_gui change. Use position not mouse.get_pos() for testing.
        if self.back_button.check_clicked():
            self.state = "menu"

    def draw(self):
        self.display.fill(constants.COLOURS["dark-gray"])

        self.level.draw_paths(self.display)
        self.level.draw_grid(self.display)

        self.player.draw(self.display)

        self.level.draw_walls(self.display)

        for enemy in self.enemies:
            enemy.draw(self.display)

        self.back_button.draw(self.display)

        pygame.display.update()
        self.clock.tick(constants.FPS)

