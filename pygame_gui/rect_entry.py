# Ben-Ryder 2019

import pygame
import pygame_gui.text
import pygame_gui.image


class RectEntry:
    def __init__(self, rect, outline,
                 colour, outline_colour,
                 hover_colour, hover_outline_colour,
                 focused_colour, focused_outline_colour,
                 focused_hover_colour, hover_focused_outline_colour,
                 initial_text, text_size, text_colour, text_font, text_padx, text_pady,
                 sticky):

        # Colour Setup
        self.colour = colour
        self.outline_colour = outline_colour

        self.hover_colour = hover_colour
        self.hover_outline_colour = hover_outline_colour

        self.focused_colour = focused_colour
        self.focused_outline_colour = focused_outline_colour

        self.focused_hover_colour = focused_hover_colour
        self.hover_focused_outline_colour = hover_focused_outline_colour

        # Physical Setup
        self.rect = pygame.Rect(rect)
        self.outline = outline

        # Text Setup
        # self.text_padx = text_padx
        # self.text_pady = text_pady
        self.text_padx =  self.text_pady = 0
        self.active = False
        self.sticky = sticky  # sticky if text should remain when entry re-clicked on.
        self.text = pygame_gui.Text(initial_text, text_size, text_colour, text_font,
                                    self.rect.x+self.text_padx, self.rect.y+self.text_pady)

        padding_x = (self.rect.width - self.text.rect.width) / 2
        padding_y = (self.rect.height - self.text.rect.height) / 2
        self.text.x += padding_x
        self.text.y += padding_y

        self.backspace = False  # allows for continuous backspace. (as long as handle_event_up() is also called)
        self.backspace_delay = 7  # READ ME!! - works as delayed by x frames, for higher frame rates increase delay.
        self.backspace_counter = 0

    def center_text(self):
        # allowing dynamic re-adjustments
        self.text.x, self.text.y = self.rect.topleft
        padding_x = (self.rect.width - self.text.rect.width) / 2
        padding_y = (self.rect.height - self.text.rect.height) / 2
        self.text.x += padding_x
        self.text.y += padding_y

    def get_text(self):
        return self.text.text

    def mouse_over(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False

    def check_clicked(self):
        if self.mouse_over():
            self.active = True
            if not self.sticky:
                self.text.change_text("")
        else:
            self.active = False
            self.backspace = False

    def handle_event(self, event):
        if self.active:
            key_uni = event.unicode
            key_str = pygame.key.name(event.key)

            if key_str == "backspace":
                self.backspace = True  # deletes characters in draw()
            elif key_str == "space" and self.text.graphic_text.get_width() < self.rect[2] - self.text_padx*3:
                self.text.change_text(self.text.text + " ")
            else:
                if self.text.graphic_text.get_width() < self.rect[2]-self.text_padx*3 and key_uni.isprintable():
                    if pygame.key.get_mods() & pygame.KMOD_CAPS or pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        self.text.change_text(self.text.text+key_uni.upper())
                    else:
                        self.text.change_text(self.text.text+key_uni.lower())

                self.center_text()

    def handle_event_up(self, event):
        if self.active:
            key_str = pygame.key.name(event.key)

            if key_str == "backspace":
                self.backspace = False

    def draw(self, display):
        # Delete character if suppose to. (done here as definitely called every game loop)
        if self.backspace:
            if self.backspace_counter >= self.backspace_delay:
                self.text.change_text(self.text.text[:-1])
                self.backspace_counter = 0
                self.center_text()
            else:
                self.backspace_counter += 1

        # Drawing
        if self.mouse_over() and self.active:
            pygame.draw.rect(display, self.focused_hover_colour, self.rect)
            pygame.draw.rect(display, self.hover_focused_outline_colour, self.rect, self.outline)
        elif self.active:
            pygame.draw.rect(display, self.focused_colour, self.rect)
            pygame.draw.rect(display, self.focused_outline_colour, self.rect, self.outline)
        elif self.mouse_over():
            pygame.draw.rect(display, self.hover_colour, self.rect)
            pygame.draw.rect(display, self.hover_outline_colour, self.rect, self.outline)
        else:
            pygame.draw.rect(display, self.colour, self.rect)
            pygame.draw.rect(display, self.outline_colour, self.rect, self.outline)
        self.text.draw(display)
