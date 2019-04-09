# Ben-Ryder 2019

def get_pixel_position(level, point):
    return [level.TILE_SIZE * point[0], level.TILE_SIZE * point[1]]


def get_tile_position(level, point):
    return [int(point[0] / level.TILE_SIZE), int(point[1] / level.TILE_SIZE)]
