# Ben-Ryder 2019

import webbrowser
import pygame

import paths
import constants

import pygame_gui


class Menu:
    """ top section for user to pick state. new_game, leaderboard ..."""
    def __init__(self, display):
        self.display = display
        self.state = "menu"

        # Background Setup
        self.background = pygame_gui.Image(paths.imagePath + "background-menu.png", 0, 0)

        # Title / Header setup
        self.title = pygame_gui.Text(
            constants.DISPLAY_NAME,
            45, constants.FONTS["colour"], constants.FONTS["main"],
            430, 180)

        # Making panel around text, with padding.
        title_rect = pygame.Rect(self.title.get_rect())
        title_padding = 5
        title_rect.x -= title_padding
        title_rect.width += title_padding*2
        self.title_panel = pygame_gui.Panel(title_rect, 150, constants.COLOURS["panel"])

        # Menu location (New, Load and Leaderboard)
        self.menux = 420
        self.menuy = 300

        # GUI Menu Setup
        self.continue_button = pygame_gui.TextButton(
            [self.menux, self.menuy + 40, 150, 40],
            constants.COLOURS["panel"], constants.COLOURS["panel-hover"],
            "select level",
            constants.FONTS["sizes"]["large"], constants.FONTS["colour"], constants.FONTS["main"])

        self.editor_button = pygame_gui.TextButton(
            [self.menux, self.menuy + 90, 150, 40],
            constants.COLOURS["panel"], constants.COLOURS["panel-hover"],
            "editor",
            constants.FONTS["sizes"]["large"], constants.FONTS["colour"], constants.FONTS["main"])

        self.version = pygame_gui.Text(
            constants.version,
            constants.FONTS["sizes"]["medium"], constants.FONTS["colour"], constants.FONTS["main"],
            3, constants.DISPLAY_SIZE[1] - 20)

        self.project_github = WebLink("GitHub Page",
                                      "https://github.com/Ben-Ryder/Escape",
                                      470, constants.DISPLAY_SIZE[1] - 20)

        self.personal_site = WebLink("By Ben Ryder",
                                     "https://github.com/Ben-Ryder",
                                     constants.DISPLAY_SIZE[0] - 87, constants.DISPLAY_SIZE[1] - 20)

        self.run()

    def run(self):
        while self.state == "menu":
            self.handle_events()
            self.draw()

    def get_state(self):
        return self.state

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = "quit"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.continue_button.check_clicked():
                    self.state = "load_game"
                elif self.editor_button.check_clicked():
                    self.state = "editor"
                else:
                    self.project_github.check_clicked()
                    self.personal_site.check_clicked()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or (event.key == pygame.K_F4 and event.mod == pygame.KMOD_ALT):
                    self.state = "quit"

    def draw(self):
        self.display.fill((0, 0, 0))
        self.background.draw(self.display)

        self.title_panel.draw(self.display)
        self.title.draw(self.display)

        self.continue_button.draw(self.display)
        self.editor_button.draw(self.display)

        self.version.draw(self.display)
        self.project_github.draw(self.display)
        self.personal_site.draw(self.display)

        pygame.display.update()


class WebLink:
    """ Extension of pygame_gui.Text, when hovered over shows underline. If clicked opens href using webbrowser """
    def __init__(self, text, href, x, y):
        self.href = href

        self.text = pygame_gui.Text(
            text,
            constants.FONTS["sizes"]["medium"], constants.FONTS["colour"],
            constants.FONTS["main"],
            x, y)

        self.rect = self.text.get_rect()

        self.hover_text = pygame_gui.Text(
            text,
            constants.FONTS["sizes"]["medium"], constants.FONTS["colour"], constants.FONTS["main"],
            x, y)
        self.hover_text.graphic_font.set_underline(True)
        self.hover_text.change_text(self.hover_text.text)  # acts as update, font must be re-rendered to show underline.

    def mouse_over(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def check_clicked(self):
        if self.mouse_over():
            webbrowser.open(self.href)
            return True
        return False

    def draw(self, display):
        if self.mouse_over():
            self.hover_text.draw(display)
        else:
            self.text.draw(display)
