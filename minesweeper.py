import pygame
import pypower.game, pypower.scene, pypower.sprite, pypower.color, pypower.direction
import random

class Minesweeper(pypower.game.Game):
  def __init__(self):
    super().__init__(1080, 720, 60)
    self.scene_manager.init("Main", MainScene(self))

    pygame.display.set_caption("Minesweeper")


class MainScene(pypower.scene.Scene):
  def __init__(self, game):
    super().__init__(game)
    
    self.board = Board(16, 16, 40)
    self.all_sprites.add(self.board)

  def handle_events(self, events):
    for event in events:
      if event.type == pygame.MOUSEBUTTONDOWN:
        for spr in self.all_sprites:
          if spr.rect.collidepoint(event.pos):
            if spr == self.board and not self.board.game_over:
              index = self.board.get_index_from_pos(event.pos)
              if event.button == 1:
                # Open Box
                self.board.open(index)
                if self.board.game_over:
                  # Game Over
                  pass
              elif event.button == 2:
                # Open Surrounding Boxes
                flaged = 0
                for direction in pypower.direction.DIRECTIONS8:
                  if self.board.is_flaged(index+direction):
                    flaged += 1

                if self.board.is_opened(index) and flaged == self.board.get_number(index):
                  for direction in pypower.direction.DIRECTIONS8:
                    self.board.open(index+direction)

                  if self.board.game_over:
                    # Game Over
                    pass
              elif event.button == 3:
                # Toggle Flag
                self.board.toggle_flag(index)
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          self.board.kill()
          self.board = Board(self.board.x, self.board.y, self.board.n)
          self.all_sprites.add(self.board)
                
class Board(pypower.sprite.Composite):
  def __init__(self, x, y, n):
    super().__init__(0, 0, 32*x, 32*y)
    self.x = x
    self.y = y
    self.n = n
    
    if n > x*y - 9:
      raise ValueError("Too Many Mines!")
    
    self._initialized = False
    self.game_over = False

    self._boxes = [[Box(i, j) for j in range(y)] for i in range(x)]
    for box_column in self._boxes:
      for box in box_column:
        self.add(box)

  def get_index_from_pos(self, pos):
    return (pos[0] // 32, pos[1] // 32)
  
  def is_vaild(self, index):
    return index[0] >= 0 and index[0] < self.x and index[1] >= 0 and index[1] < self.y

  def _get(self, index):
    if not self.is_vaild(index):
      raise IndexError("Invaild Index")
    return self._boxes[index[0]][index[1]]

  def is_opened(self, index):
    if self.is_vaild(index):
      return self._get(index).opened
    else:
      return False

  def is_flaged(self, index):
    if self.is_vaild(index):
      return self._get(index).flaged
    else:
      return False

  def is_mine(self, index):
    if self.is_vaild(index):
      return self._get(index).mine
    else:
      return False

  def get_number(self, index):
    if self.is_vaild(index):
      return self._get(index).number
    else:
      raise IndexError("Invaild Index")

  def toggle_flag(self, index):
    if self.is_vaild(index) and not self.is_opened(index):
      self._get(index).toggle_flag()

  def init(self, index):
    self._initialized = True
    
    mine = 0
    while mine <= self.n:
      rand_index = (random.randint(0, self.x-1), random.randint(0, self.y-1))
           
      if self.is_mine(rand_index):
        continue
        
      ok = True
      for direction in pypower.direction.DIRECTIONS8:
        if index+direction == rand_index:
          ok = False
        
      if ok:
        self._get(rand_index).mine = True
        mine += 1
        for direction in pypower.direction.DIRECTIONS8:
          if self.is_vaild(rand_index+direction):
            self._get(rand_index+direction).number += 1
          
  def open(self, index):
    if not self.is_vaild(index) or self.is_flaged(index):
      return

    if not self._initialized:
      self.init(index)
    
    self._get(index).open()
    
    if self.is_mine(index):
      self.game_over = True
      
    if self._get(index).number == 0:
      for direction in pypower.direction.DIRECTIONS8:
        if self.is_vaild(index+direction) and not self.is_opened(index+direction) and not self.is_flaged(index+direction):
          self.open(index+direction)


class Box(pypower.sprite.Composite):
  def __init__(self, x, y):
    super().__init__(x*32, y*32, 32, 32)

    self.mine = False
    self.opened = False
    self.flaged = False
    self.number = 0

    self.bgd.fill(pypower.color.GRAY)

  def open(self):
    if self.opened or self.flaged:
      return
    
    self.opened = True
    self.set_dirty()

    if self.mine:
      self.bgd.fill(pypower.color.RED)
      self.image.fill(pypower.color.RED)
    else:
      self.bgd.fill(pypower.color.WHITEGRAY)
      self.image.fill(pypower.color.WHITEGRAY)
      if self.number:
        self.add(pypower.sprite.Text(str(self.number), (15,15), 30, alignment=(0,0), color=pypower.color.BLACK))

  def toggle_flag(self):
    self.flaged = not self.flaged
    
    if self.flaged:
      self.bgd.fill(pypower.color.YELLOW)
      self.image.fill(pypower.color.YELLOW)
    else:
      self.bgd.fill(pypower.color.GRAY)
      self.image.fill(pypower.color.GRAY)

    self.set_dirty()

    
if __name__ == "__main__":
  minesweeper = Minesweeper()
  minesweeper.run()