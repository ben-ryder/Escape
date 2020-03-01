# Ben-Ryder 2019

import pygame
import os

import paths
import constants

import pygame_gui

import project.data as data

class LoadGame:
    """ Lets user select games from a list of files from paths.GamePath """
    def __init__(self, display):
        self.display = display
        self.state = "load_game"
        self.game_reference = None

        # Background Setup
        self.background = pygame_gui.Image(paths.imagePath + "background-load.png", 0, 0)
        #self.back_panel = pygame_gui.Panel([100, 100, 800, 500], 150, constants.COLOURS["panel"])

        # GUI Setup
        self.back_button = pygame_gui.Button(paths.uiPath + "backwhite.png",
                                             paths.uiPath + "backwhite-hover.png",
                                             5, 5)
        self.title = pygame_gui.Text(
            "Select Level: ",
            constants.FONTS["sizes"]["large"], constants.FONTS["colour"], constants.FONTS["main"],
            275, 55)

        self.file_selector = FileSelector(self, [275, 100])
        self.try_delete = None  # if True, displays delete_message, try's to delete file in to_delete if ok pressed
        self.to_delete = None
        # #self.delete_message = GUI.CheckMessage(self, "Are You Sure?", ["The game will be permanently deleted,",
        #                                                                "and can't be recovered!"])

        self.page_back_button = pygame_gui.Button(paths.uiPath + "pageback.png", paths.uiPath + "pageback-hover.png",
                                                  670, 53)
        self.page_forward_button = pygame_gui.Button(paths.uiPath + "pageforward.png",
                                                     paths.uiPath + "pageforward-hover.png",
                                                     710, 53)

        self.run()

    def run(self):
        while self.state == "load_game":
            self.handle_events()
            self.draw()

    def get_state(self):
        print("loadgame.py, class=LoadGame")#added for unit test assignment
        print("UNITTEST-Getting state: \"" + str(self.state) + "\"")#added for unit test assignment
        print()#added for unit test assignment
        return self.state

    def get_game(self):
        print("loadgame.py, class=LoadGame")#added for unit test assignment
        print("UNITTEST-Getting game: \"" + str(self.game_reference) + "\"")#added for unit test assignment
        print()#added for unit test assignment
        return self.game_reference

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = "quit"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # # if self.try_delete:  # channel inputs to delete message only
                # #     self.delete_message.handle_click()
                # #
                # #     delete = self.delete_message.get_result()
                # #     if delete:  # must get state of message, then handle it, not done in message.
                # #         self.delete_game()
                # #     elif not delete:
                # #         self.reset_delete()
                #
                # else:
                if not self.file_selector.check_clicked():
                    if self.back_button.check_clicked():
                        print("loadgame.py, class=LoadGame")#added for unit test assignment
                        print("UNITTEST-Back button clicked. Setting state to menu")#added for unit test assignment
                        print()#added for unit test assignment
                        self.state = "menu"

                    elif self.page_back_button.check_clicked():
                        print("loadgame.py, class=LoadGame")#added for unit test assignment
                        print("UNITTEST-Page back button clicked")#added for unit test assignment
                        print()#added for unit test assignment
                        self.file_selector.page_back()

                    elif self.page_forward_button.check_clicked():
                        print("loadgame.py, class=LoadGame")#added for unit test assignment
                        print("UNITTEST-Page back button clicked")#added for unit test assignment
                        print()#added for unit test assignment
                        self.file_selector.page_forward()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or (event.key == pygame.K_F4 and event.mod == pygame.KMOD_ALT):
                    print("loadgame.py, class=LoadGame")#added for unit test assignment
                    print("UNITTEST-ESC key or ATL-F4 clicked, Exiting...")#added for unit test assignment
                    print()#added for unit test assignment
                    self.state = "quit"

    def delete_game(self):
        data.delete(paths.gamePath + self.to_delete)
        self.file_selector.refresh_list()
        self.reset_delete()

    def select_game(self, game_name):
        print("loadgame.py, class=LoadGame")#added for unit test assignment
        print("UNITTEST-Game: " + str(game_name) + " selected. quiting load game routine and starting game routine")#added for unit test assignment
        print()#added for unit test assignment
        self.game_reference = game_name
        self.state = "game"  # effectively quits load game

    def try_delete_game(self, game_name):
        self.try_delete = True
        self.to_delete = game_name

    def reset_delete(self):
        self.to_delete = None
        self.try_delete = False

    def draw(self):
        self.display.fill((0, 0, 0))
        self.background.draw(self.display)

        self.title.draw(self.display)
        self.back_button.draw(self.display)

        self.file_selector.draw(self.display)
        self.page_back_button.draw(self.display)
        self.page_forward_button.draw(self.display)

        # if self.try_delete:
        #     self.delete_message.draw(self.display)

        pygame.display.update()


class FileSelector:
    """ Responsible for the list of files seen on screen """
    def __init__(self, control, origin):
        self.control = control  # control being LoadGame Object
        self.origin = origin
        self.max_amount = 8  # split into lists of amount (pages of so many games)

        # Load Game Names From Directory
        self.games = sorted([file for file in os.listdir(paths.customGamePath)]) + sorted([file for file in os.listdir(paths.gamePath)])
        try:
            self.games.remove(".gitignore")  # .gitignore present to stop data being pushed/pulled but still in directory.
        except ValueError:
            pass
        self.split_games = [self.games[i:i + self.max_amount] for i in range(0, len(self.games), self.max_amount)]
        # ^ splits games list into equal sub-lists of self.max_amount.

        # GUI Setup
        self.current_page = 0
        self.game_pages = []
        padding = 70  # space between file slots
        for page in self.split_games:
            self.game_pages.append([])
            counter = 0
            for game_name in page:
                self.game_pages[len(self.game_pages)-1].append(
                    GameSlot(self.control, game_name, [self.origin[0], self.origin[1] + padding*counter])
                )
                counter += 1

    def refresh_list(self):
        self.__init__(self.control, self.origin)

    def check_clicked(self):
        try:
            for slot in self.game_pages[self.current_page]:
                slot.handle_click()
        except IndexError:  # no games in file
            pass

    def page_forward(self):
        print("loadgame.py, class=FileSelector")#added for unit test assignment
        print("UNITTEST-Moving page forward")#added for unit test assignment
        print()#added for unit test assignment
        if self.current_page < len(self.game_pages)-1:
            self.current_page += 1
        else:
            self.current_page = 0

    def page_back(self):
        print("loadgame.py, class=FileSelector")#added for unit test assignment
        print("UNITTEST-Moving page backward")#added for unit test assignment
        print()#added for unit test assignment
        if self.current_page > 0:
            self.current_page -= 1
        else:
            self.current_page = len(self.game_pages)-1

    def draw(self, display):
        try:
            for game_slot in self.game_pages[self.current_page]:
                game_slot.draw(display)
        except IndexError:  # in case there are no games.
            pass


class GameSlot:
    """ A individual game slot, seen on the screen. managed by FileSelector"""
    def __init__(self, control, game_name, position):
        self.control = control  # Control in this case is the LoadGame object.
        self.game_name = game_name
        self.position = position

        # GUI Setup
        self.back_panel = pygame_gui.Panel([self.position[0], self.position[1], 450, 50],
                                           255, constants.COLOURS["panel"])
        self.back_panel_hover = pygame_gui.Panel([self.position[0], self.position[1], 450, 50],
                                                 255, constants.COLOURS["panel-hover"])

        self.text = pygame_gui.Text(
            game_name,
            constants.FONTS["sizes"]["medium"], constants.FONTS["colour"], constants.FONTS["main"],
            self.position[0] + 50, self.position[1] + 15)

        # self.quit_button = pygame_gui.Button(paths.uiPath + "cross.png",
        #                                      paths.uiPath + "cross-hover.png",
        #                                      self.position[0]+450, self.position[1] + 8)

    def handle_click(self):
        # if self.quit_button.check_clicked():
        #     self.control.try_delete_game(self.game_name)

        if self.mouse_over():
            print("loadgame.py, Class=GameSlot")#added for unit test assignment
            print("UNITTEST-Gameslot clicked. Loading game: " + str(self.game_name) )#added for unit test assignment
            print()#added for unit test assignment
            self.control.select_game(self.game_name)

    def mouse_over(self):
        return self.back_panel.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self, display):
        if self.mouse_over():
            self.back_panel_hover.draw(display)
        else:
            self.back_panel.draw(display)

        self.text.draw(display)
        # self.quit_button.draw(display)
