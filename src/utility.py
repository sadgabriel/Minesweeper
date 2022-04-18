import pygame
import definition
import math


def move_rect_by_alignment(rect, pos, alignment):
  if alignment[0] == -1:
    rect.left = pos[0]
  elif alignment[0] == 0:
    rect.centerx = pos[0]
  elif alignment[0] == 1:
    rect.right = pos[0]
  else:
    raise ValueError("alignment must be a tuple of -1, 0, or 1 whose length is 2 like (-1, 0), (1, -1), or (1, 1)")

  if alignment[1] == -1:
    rect.top = pos[1]
  elif alignment[1] == 0:
    rect.centery = pos[1]
  elif alignment[1] == 1:
    rect.bottom = pos[1]
  else:
    raise ValueError("alignment must be a tuple of -1, 0, or 1 whose length is 2 like (-1, 0), (1, -1), or (1, 1)")


class DirectionFinder:
  def __init__(self):
    self._sprites = pygame.sprite.LayeredDirty()

  def add(self, sprite):
    if sprite in self._sprites:
      raise ValueError("The sprite is already in this DirectionFinder")
    else:
      self._sprites.add(sprite)

  def remove(self, sprite):
    if not (sprite in self._sprites):
      raise ValueError("The sprite is not in this DirectionFinder")
    else:
      self._sprites.remove(sprite)

  def find(self, fiducial_sprite: pygame.sprite.DirtySprite, direction, fiducial_angle=5):
    """Find and return the sprite which is just next to fiducial_sprite"""
    if fiducial_angle < 0:
      raise ValueError("fiducial angle must be positive")

    candidates = list()

    get_pos1 = None
    get_pos2 = None

    if direction == definition.UP:
      get_pos1 = lambda sprite: sprite.rect.midleft
      get_pos2 = lambda sprite: sprite.rect.midright
    elif direction == definition.DOWN:
      get_pos1 = lambda sprite: sprite.rect.midright
      get_pos2 = lambda sprite: sprite.rect.midleft
    elif direction == definition.LEFT:
      get_pos1 = lambda sprite: sprite.rect.midbottom
      get_pos2 = lambda sprite: sprite.rect.midtop
    elif direction == definition.RIGHT:
      get_pos1 = lambda sprite: sprite.rect.midtop
      get_pos2 = lambda sprite: sprite.rect.midbottom
    else:
      raise ValueError("direction must be UP, DOWN, LEFT or RIGHT in definition.py")

    a1 = get_pos1(fiducial_sprite)
    a2 = get_pos2(fiducial_sprite)

    print("a1 and a2: ", a1, a2)  ######################

    for sprite in self._sprites:
      print("testing sprite: ", sprite)  ###############
      print("direction: ", direction)  ###############
      if direction == definition.UP and fiducial_sprite.rect.centery <= sprite.rect.centery:
        print("continued")  #######################
        continue
      elif direction == definition.DOWN and fiducial_sprite.rect.centery >= sprite.rect.centery:
        print("continued", fiducial_sprite.rect.centery, sprite.rect.centery)  #######################
        continue
      elif direction == definition.LEFT and fiducial_sprite.rect.centerx <= sprite.rect.centerx:
        print("continued")  #######################
        continue
      elif direction == definition.RIGHT and fiducial_sprite.rect.centerx >= sprite.rect.centerx:
        print("continued")  #######################
        continue

      x1 = get_pos1(sprite)
      x2 = get_pos2(sprite)

      angle21 = find_angle(find_vector(a2, x1))
      angle12 = find_angle(find_vector(a1, x2))
      base_angle = find_angle(direction)

      flag1 = False
      flag2 = False

      if direction == definition.LEFT:  ############################
        flag1 = angle12 >= base_angle - fiducial_angle or angle12 < -90
        flag2 = angle21 <= -base_angle + fiducial_angle or angle21 > 90
      else:
        flag1 = angle12 >= base_angle - fiducial_angle
        flag2 = angle21 <= base_angle + fiducial_angle

      if flag1 and flag2:
        candidates.append(sprite)
        print("appended")  ##################
      else:
        print("passed")  #############

    print("candidates: ", candidates) ######

    if candidates:
      if direction == definition.UP:
        return max(candidates, key=lambda sprite: (sprite.rect.centery - abs(sprite.rect.centerx - fiducial_sprite.rect.centerx)))
      elif direction == definition.DOWN:
        return min(candidates, key=lambda sprite: (sprite.rect.centery + abs(sprite.rect.centerx - fiducial_sprite.rect.centerx)))
      elif direction == definition.LEFT:
        return max(candidates, key=lambda sprite: (sprite.rect.centerx - abs(sprite.rect.centery - fiducial_sprite.rect.centery)))
      elif direction == definition.RIGHT:
        return min(candidates, key=lambda sprite: (sprite.rect.centerx + abs(sprite.rect.centery - fiducial_sprite.rect.centery)))
    else:
      print("fiducial_sprite is returned")  #########################
      return fiducial_sprite


def find_vector(point1, point2):
  """Return vector of point1 to point2"""
  return (point2[0] - point1[0], point2[1] - point1[1])


def find_angle(vector):
  return math.degrees(math.atan2(vector[1], vector[0]))
