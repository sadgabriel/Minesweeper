class Direction:
  def __init__(self, x, y):
    if (x == -1 or x == 0 or x == 1) and (y == -1 or y == 0 or y == 1):
      self._x = x
      self._y = y
    else:
      raise ValueError("Direction's x and y values must be -1, 0, or 1")

  @property
  def x(self):
    return self._x

  @property
  def y(self):
    return self._y

  def __getitem__(self, index):
    if index == 0:
      return self.x
    elif index == 1:
      return self.y
    else:
      IndexError("Direction's index must be 0 or 1")

  def apply(self, pos):
    return (pos[0] + self.x, pos[1] + self.y)

UP = Direction(0, -1)
DOWN = Direction(0, 1)
LEFT = Direction(-1, 0)
RIGHT = Direction(1, 0)

DIRECTIONS8 = (Direction(-1, -1), Direction(-1, 0), Direction(-1, 1), Direction(0, -1), 
               Direction(0, 1), Direction(1, -1), Direction(1, 0), Direction(1, 1))
