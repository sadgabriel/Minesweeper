import pygame
from os import path
import definition
import utility
import random

class Text(pygame.sprite.DirtySprite):
  """Base class to render and control Text
  
  Update processing
  _update_font -> _update_image -> _update_rect

  Each changes need proper updates
  fontname and size -> _update_font
  text,color and antialias-> _update_image
  pos and alignment -> _update_rect
  """
  def __init__(self, text, pos, size, *, fontname='arial.ttf', alignment=(-1,-1), color=definition.WHITE, layer=0, antialias=False):
    super().__init__()
    # six basic attributes of Text
    self._text = text
    self._pos = pos
    self._size = size
    self._fontname = path.join(definition.font_dir, fontname)
    self._alignment = alignment
    self._color = color
    self._antialias = antialias
    
    # three derived attributes of Text
    # they may be updated when a basic attribute changes
    self._font = None
    self.image = None
    self.rect = None

    # for layer control
    self._layer = layer

    self._update_font()

  def _update_font(self):
    self._font = pygame.font.Font(self.fontname, self.size)
    self._update_image()

  def _update_image(self):
    self.image = self._font.render(self.text, self.antialias, self.color, definition.TRANSPARENT)
    self.image.set_colorkey(definition.TRANSPARENT)
    self._update_rect()
  
  def _update_rect(self):
    self.rect = self.image.get_rect()
    utility.move_rect_by_alignment(self.rect, self._pos, self._alignment)
    self.dirty = 1

  def __str__(self):
    return f"{str(self.rect)}: {self.text}"

  @property
  def text(self):
    return self._text

  @property
  def pos(self):
    return self._pos

  @property
  def size(self):
    return self._size

  @property
  def fontname(self):
    return self._fontname

  @property
  def alignment(self):
    return self._alignment

  @property
  def color(self):
    return self._color

  @property
  def antialias(self):
    return self._antialias

  @text.setter
  def text(self, text):
    self._text = text
    self._update_image()
  
  @pos.setter
  def pos(self, pos):
    self._pos = pos
    self._update_rect()

  @size.setter
  def size(self, size):
    self._size = size
    self._update_font()
  
  @fontname.setter
  def fontname(self, fontname):
    self._fontname = fontname
    self._update_font()
  
  @alignment.setter
  def alignment(self, alignment):
    self._alignment = alignment
    self._update_rect()
  
  @color.setter
  def color(self, color):
    self._color = color
    self._update_image()

  @antialias.setter
  def antialias(self, antialias):
    self._antialias = antialias
    self._update_image()


class Image(pygame.sprite.DirtySprite):
  """Base class to render and control image file
  
  update processing
  _update_original_image -> _apply_transform -> _update_rect

  each changes need proper updates
  filename -> _update_original_image
  size and angle -> _apply_transform
  pos and alignment -> _update_rect
  """
  def __init__(self, filename, pos, alignment=(-1,-1), size=None, angle=0, layer=0):
    super().__init__()
    self._filename = filename
    self._pos = pos
    self._alignment = alignment
    self._size = size
    self._angle = angle

    self._original_image = None
    self.image = None
    self.rect = None

    self._layer = layer

    self._update_original_image()
    if self._size is None:
      self._size = self.rect.size

  def _update_original_image(self):
    self._original_image = pygame.image.load(path.join(definition.img_dir, self._filename)).convert()
    self._apply_transform()
  
  def _apply_transform(self):
    self.image = self._original_image
    if self._size is not None:
      self.image = pygame.transform.scale(self.image, self._size)
    if self._angle is not None:
      self.image = pygame.transform.rotate(self.image, self._angle)
    self._update_rect()

  def _update_rect(self):
    self.rect = self.image.get_rect()
    utility.move_rect_by_alignment(self.rect, self._pos, self._alignment)    
    self.dirty = 1

  @property
  def filename(self):
    return self._filename
  
  @property
  def pos(self):
    return self._pos
  
  @property
  def alignment(self):
    return self._alignment
  
  @property
  def size(self):
    return self._size
  
  @property
  def angle(self):
    return self._angle
  
  @filename.setter
  def filename(self, filename):
    self._filename = filename
    self._update_original_image()
  
  @pos.setter
  def pos(self, pos):
    self._pos = pos
    self._update_rect()
  
  @alignment.setter
  def alignment(self, alignment):
    self._alignment = alignment
    self._update_rect()
  
  @size.setter
  def size(self, size):
    self._size = size
    self._apply_transform()
  
  @angle.setter
  def angle(self, angle):
    self._angle = angle % 360
    self._apply_transform()


class ComplexSprite(pygame.sprite.DirtySprite):
  """DirtySprite which has other DirtySprites on it"""
  def __init__(self, left, top, width, height):
    super().__init__()
    self.rect = pygame.Rect(left, top, width, height)
    self.image = pygame.Surface(self.rect.size)
    self.image.fill(definition.TRANSPARENT)
    self.bgd = self.image.copy()
    self.image.set_colorkey(definition.TRANSPARENT)

    self._sprites = pygame.sprite.LayeredDirty()
    self._clean_len = 0
  
  def add(self, sprite: pygame.sprite.DirtySprite):
    self._sprites.add(sprite)
    self._clean_len = self._clean_len + 1
    sprite.dirty = 1

  def update(self):
    super().update()
    self._check_clean()

    for sprite in self._sprites:
      sprite.update()
      if sprite.dirty != 0:
        self.set_dirty()
        
    self._sprites.draw(self.image, bgd=self.bgd)
  
  def _check_clean(self):
    """Set self.dirty to 1 if there is any removed sprite"""
    if len(self._sprites) != self._clean_len:
      self._clean_len = len(self._sprites)
      self.set_dirty()
  
  def set_dirty(self, dirty=1, consider_2 = True):
    """Set self.dirty to dirty
    if already self.dirty is 2, dirty is 1 and ignore_2 is False, than it skips the work"""
    if not(self.dirty == 2 and dirty == 1 and consider_2):
      self.dirty = dirty


class Box(ComplexSprite):
  def __init__(self, x, y):
    super().__init__(x*32, y*32, 32, 32)

    self.mine = False
    self.opened = False
    self.flaged = False
    self.number = 0

    self.bgd.fill(definition.GRAY)
    self.set_dirty()
    

  def open(self):
    if self.flaged:
      return
    
    self.opened = True

    if self.mine:
      self.bgd.fill(definition.RED)
      self.image.fill(definition.RED)
      self.set_dirty()
    else:
      self.bgd.fill(definition.WHITEGRAY)
      self.image.fill(definition.WHITEGRAY)
      self.set_dirty()
      if self.number:
        self.add(Text(str(self.number), (15,15), 30, alignment=(0,0), color=definition.BLACK))
    
  def toggle_flag(self):
    self.flaged = not self.flaged

    if self.flaged:
      self.bgd.fill(definition.YELLOW)
      self.image.fill(definition.YELLOW)
      self.set_dirty()
    else:
      self.bgd.fill(definition.GRAY)
      self.image.fill(definition.GRAY)
      self.set_dirty()

class Board(ComplexSprite):
  def __init__(self, x, y, n):
    super().__init__(0, 0, x*32, y*32)
    self.x = x
    self.y = y
    self.n = n

    if n > x*y - 9:
      raise ValueError("Too Many Mines!")

    self._initialized = False

    self.boxes = [[Box(i, j) for j in range(y)] for i in range(x)]
    for box_column in self.boxes:
      for b in box_column:
        self.add(b)

  def find_collide(self, cursur_pos):
    return (cursur_pos[0] // 32, cursur_pos[1] // 32)

  def _is_out_of_range(self, pos):
    return pos[0] < 0 or pos[0] >= self.x or pos[1] < 0 or pos[1] >= self.y

  def _get(self, pos):
    if self._is_out_of_range(pos):
      return None
    return self.boxes[pos[0]][pos[1]]

  def is_opened(self, pos):
    if self._is_out_of_range(pos):
      return False
    return self._get(pos).opened

  def is_flaged(self, pos):
    if self._is_out_of_range(pos):
      return False
    return self._get(pos).flaged

  def is_mine(self, pos):
    if self._is_out_of_range(pos):
      return False
    return self._get(pos).mine

  def toggle_flag(self, pos):
    if self._is_out_of_range(pos):
      raise IndexError("Out of Range")
    self._get(pos).toggle_flag()

  def get_number(self, pos):
    if self._is_out_of_range(pos):
      raise IndexError("Out of Range")
    return self._get(pos).number

  def is_initialized(self):
    return self._initialized

  def init(self, pos):
    self._initialized = True

    mine = 0
    while mine <= self.n:
      rand_pos = (random.randint(0, self.x-1), random.randint(0, self.y-1))
      
      if self.is_mine(rand_pos):
        continue

      ok = True
      for direction in ((-1,-1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
        if (pos[0]+direction[0], pos[1]+direction[1]) == rand_pos:
          #nonlocal ok
          ok = False

      if ok:
        self._get(rand_pos).mine = True
        mine = mine + 1
        for direction in ((-1,-1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
          pos2 = (rand_pos[0]+direction[0], rand_pos[1]+direction[1])
          if self._get(pos2):
            self._get(pos2).number = self._get(pos2).number + 1
        

  def open(self, pos):
    if not self._get(pos) or self.is_flaged(pos):
      return
    self._get(pos).open()
    if self._get(pos).number == 0:
      for direction in ((-1,-1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
        pos2 = (pos[0]+direction[0], pos[1]+direction[1])
        if self._get(pos2) and not self.is_opened(pos2):
          self.open(pos2)