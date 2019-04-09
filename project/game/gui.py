# Ben-Ryder 2019

import pygame
import pygame_gui

import constants


class GameOverMenu:
    def __init__(self, display, reason):
        self.display = display

        size = [250, 100]
        self.rect = pygame.Rect(display.get_width()/2 - size[0]/2, display.get_height()/2 - size[1]/2, size[0], size[1])
        self.background = pygame_gui.Panel(self.rect, 255, (10, 10, 10))

        if reason == "won":
            text = "Level Completed"
        elif reason == "lost":
            text = "Level Failed"
        else:
            raise Exception("Invalid reason for game end")

        self.title = pygame_gui.Text(text, 26, (255, 255, 255), constants.FONTS["main-bold"], self.rect.x, self.rect.y + 10)
        self.title.change_position(self.rect.centerx - self.title.rect.width/2, self.title.rect.y)

        sizes = [self.rect.width/2, self.rect.height/2]
        self.menu_button = pygame_gui.TextButton([self.rect.x, self.rect.centery, sizes[0], sizes[1]],
                                                 (10, 10, 10), (30, 30, 30),
                                                 "< menu", constants.FONTS["sizes"]["medium"],
                                                 constants.FONTS["colour"], constants.FONTS["main"])

        self.restart_button = pygame_gui.TextButton([self.rect.centerx, self.rect.centery, sizes[0], sizes[1]],
                                                    (10, 10, 10), (30, 30, 30),
                                                    "restart >", constants.FONTS["sizes"]["medium"],
                                                    constants.FONTS["colour"], constants.FONTS["main"])

        self.option = "game-over"
        self.run()

    def run(self):
        while self.option == "game-over":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.option = "quit"

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or (event.key == pygame.K_F4 and event.mod == pygame.KMOD_ALT):
                        self.option = "quit"
                    elif event.key == pygame.K_LEFT:
                        self.option = "menu"
                    elif event.key == pygame.K_RIGHT:
                        self.option = "game"

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.menu_button.check_clicked():
                        self.option = "menu"
                    elif self.restart_button.check_clicked():
                        self.option = "game"

            self.draw()

    def get_option(self):
        return self.option

    def handle_click(self):
        self.option = "game"

    def draw(self):
        self.display.fill((255, 10, 10))
        self.background.draw(self.display)
        self.title.draw(self.display)
        self.menu_button.draw(self.display)
        self.restart_button.draw(self.display)
        pygame.draw.rect(self.display, (255, 255, 255), self.rect, 2)
        pygame.display.update(self.rect)  # update only menu area
