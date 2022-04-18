from os import path

WIDTH = 1080
HEIGHT = 720
FPS = 60

src_dir = path.dirname(__file__)
home_dir = path.dirname(src_dir)
font_dir = path.join(home_dir, 'font')
img_dir = path.join(home_dir, 'img')


TRANSPARENT = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WHITEGRAY = (127, 127, 127)
GRAY = (63, 63, 63)
RED = (255, 0, 0)
BLUE = (1, 2, 253)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)