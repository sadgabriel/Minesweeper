import pygame
from os import path
from . import directory, color, utility

class Sprite(pygame.sprite.DirtySprite):
  def __init__(self, groups=list()):
    super().__init__()

    self._parents = list(groups)
    for parent in self._parents:
      parent.add(self)

  def kill(self):
    for parent in self._parents:
      parent.set_dirty()

    self._parents.clear()

    super().kill()
  
  def set_dirty(self, dirty=1, ignore_2 = False):
    """Set self.dirty to dirty
    if already self.dirty is 2, dirty is 1 and ignore_2 is False, than it skips the work"""
    if not(not ignore_2 and self.dirty == 2 and dirty == 1):
      self.dirty = dirty


class Group(pygame.sprite.LayeredDirty):
  pass
  

class Text(Sprite):
  """Base class to render and control Text
  
  Update processing
  _update_font -> _update_image -> _update_rect

  Each changes need proper updates
  fontname and size -> _update_font
  text,color and antialias-> _update_image
  pos and alignment -> _update_rect
  """
  def __init__(self, text, pos, size, *, fontname='arial.ttf', alignment=(-1,-1), color=color.WHITE, layer=0, antialias=False):
    super().__init__()
    # six basic attributes of Text
    self._text = text
    self._pos = pos
    self._size = size
    self._fontname = path.join(directory.font_dir, fontname)
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
    self.image = self._font.render(self.text, self.antialias, self.color, color.TRANSPARENT)
    self.image.set_colorkey(color.TRANSPARENT)
    self._update_rect()
  
  def _update_rect(self):
    self.rect = self.image.get_rect()
    utility.move_rect_by_alignment(self.rect, self._pos, self._alignment)
    self.dirty = 1

  def __repr__(self):
    return f"Text({str(self.rect)}, {self.text})"

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


class Image(Sprite):
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
    self._original_image = pygame.image.load(path.join(directory.img_dir, self._filename)).convert()
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


class Composite(Sprite):
  """Sprite which has other Sprites"""
  def __init__(self, left, top, width, height):
    super().__init__()
    self.rect = pygame.Rect(left, top, width, height)
    self.image = pygame.Surface(self.rect.size)
    self.bgd = self.image.copy()
    self.image.fill(color.TRANSPARENT)
    self.image.set_colorkey(color.TRANSPARENT)

    self._children = Group()
    self._clean_len = 0
  
  def add(self, spr: Sprite):
    self._children.add(spr)
    spr._parents.append(self)

  def remove(self, spr):
    self._children.remove(spr)
    self.set_dirty()

  def update(self):
    super().update()

    # Update all sprites
    # If there are any changes, set itself dirty
    for spr in self._children:
      spr.update()
      if spr.dirty != 0:
        self.set_dirty()
    
    self._children.draw(self.image, bgd=self.bgd)
  
  
