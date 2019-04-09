# Ben-Ryder 2019

import pygame_gui.text
import pygame_gui.panel


# Cheating with TextButton inherit, but will work for now. TODO: make proper label. Inherit by Textbutton instead?
class Label(pygame_gui.TextButton):

    def mouse_over(self):
        return False

