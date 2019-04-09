# Ben-Ryder 2019

import paths

version = "v1.0-pre"

DISPLAY_SIZE = [1000, 700]  # default only in menus. CHANGES BASED ON TILE RESOLUTION IN GAME AND EDITOR.
DISPLAY_NAME = "Escape"
FPS = 66

COLOURS = {
    "black": (0, 0, 0),
    "light-gray": (100, 100, 100),
    "dark-gray": (45, 45, 45),
    "red": (255, 0, 0),
    "white": (255, 255, 255),
    "orange": (255, 165, 0),
    "yellow": (255, 220, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "indigo": (75, 0, 130),
    "magenta": (255, 0, 255),

    "panel": (50, 50, 50),
    "panel-hover": (60, 60, 60),
}

FONTS = {"main": paths.fontPath + "SourceSansPro-Light.ttf",
         "main-bold": paths.fontPath + "SourceSansPro-Semibold.ttf",
         "main-italic": paths.fontPath + "SourceSansPro-LightIt.ttf",
         "main-bold-italic": paths.fontPath + "SourceSansPro-SemiboldIt.ttf",
         "sizes":
             {"large": 20,
              "medium": 15,
              "small": 12},
         "colour": COLOURS["white"]}

WALL_FORMATS = ["1", "t", "b", "l", "r", "p", "s"]
# 0 = path, 1 = wall. t/b/l/r = exits, p = player spawn, s = safe point
