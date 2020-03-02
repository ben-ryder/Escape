#Unit tests made by Brandon Withington
import unittest
import sys
from mock import Mock
import data
import os
# == Writing functions to be tested ==
#
#   Attempted to write a mock test for both the save and is_wall functions
#   found in the level.py file but they would not work. I kept getting errors
#   that indicated unit testing on our files would be very hard to accomplish
#   it would say that "level.py has no attribute save / is_wall"
#   I had to shift all of the other files it was importing to be local to this file
#   as for some reason, whenever I imported "level.py" it would say in the terminal : "module paths not found"
#
#   Below is what my two unit test functions would have looked like.
#
# class test_isWall(unittest.TestCase):
#    def test_isWall(self):
#        mock_wall = Mock()
#        level.is_wall(mock_wall, 2)
#        mock_wall.PostUpdate.assert_called_with(2)
#
# class test_save(unittest.TestCase):
#    def test_save(self):
#        mock_save = Mock()
#        level.save(mock_save, filename)
#        mock_save.PostUpdate.assert_called_with(filename)

# had to take the level initializer from the level.py file in order to test several functions correctly.

class LevelModel:
    def __init__(self, filename=None):
        if filename is not None and os.path.isfile(paths.dataPath + filename):
            self.load(filename)
        else:
            # Default values if not loading file
            self.TILE_SIZE = 50
            self.MAP_SIZE = [20, 14]

            self.format = None

            # Keys Setup
            self.keys = []

            # Sizing Setup (All based of map and tile size, so same if default or loaded)
            self.DISPLAY_SIZE = None
            self.EDITOR_SIZE = None

            self.PLAYER_SIZE = None
            self.PLAYER_PADDING = None

            self.ENEMY_SIZE = None
            self.ENEMY_PADDING = None

# Had to pick the function from the actual file itself.
#   I then had to remove the definition of tile_size, map size and map format as they were producing
#   terminal errors when attempting to load them.

def save(self, filename):
    level = {

    }
    try:
        data.save(level, filename)
        return True
    except IsADirectoryError:
        return False

class test_saveFunction(unittest.TestCase):
    def test_saveFunct(self):
        result = save(self, "test_filename")
        self.assertEqual(result, True)

# Testing size changer functions (tile size && map size)

def change_tile_size(self, new):
    self.TILE_SIZE = new
    return self.TILE_SIZE

class test_setTileSize(unittest.TestCase):
    def test_setTileS(self):
        self.assertEqual(change_tile_size(self, 75), 75)
        self.assertEqual(change_tile_size(self, 999999), 999999)
        self.assertEqual(change_tile_size(self, 0), 0)
        self.assertEqual(change_tile_size(self, -1), -1)

def change_map_size(self, new):
    self.MAP_SIZE = new
    return self.MAP_SIZE

class test_setMapSize(unittest.TestCase):
    def test_setMapS(self):
        self.assertEqual(change_map_size(self, 75), 75)
        self.assertEqual(change_map_size(self, 0), 0)
        self.assertEqual(change_map_size(self, -1), -1)

# Testing Load function
# The test has to be reloaded in order to test the load function.
# The test function above will create a file for this load function to
# load. It just needs to be called again after to test the load function properly.

def load(self, filename):
    try:
        data.load(filename)
        return True
    except IsADirectoryError:
        return False

class testLoad(unittest.TestCase):
    def test_load(self):
        self.assertEqual(load(self, "test_filename"), True)


if __name__ == '__main__':
    unittest.main()
