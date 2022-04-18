import sprite
import pygame
import definition
import utility


class Scene:
  def __init__(self, game):
    self.game = game
    
    # the Group to hold all sprites
    self.sprites = pygame.sprite.LayeredDirty()
  
  def handle_events(self, events): # handle unhandled events by Vrow
    pass
  
  def update(self): # update all the things and return the next scene
    self.sprites.update()
  
  def render(self): # render the scene to self.game.screen. flip is not necessary
    self.sprites.draw(self.game.screen)

class MainScene(Scene):
  def __init__(self, game):
    super().__init__(game)

    self.board = sprite.Board(16, 16, 40)
    self.sprites.add(self.board)

  def handle_events(self, events):
    for event in events:
      if event.type == pygame.MOUSEBUTTONDOWN:
        for s in self.sprites:
          if s.rect.collidepoint(event.pos):
            if s == self.board:
              box_pos = self.board.find_collide(event.pos)
              if event.button == 1:
                # Open Box
                if not self.board.is_opened(box_pos) and not self.board.is_flaged(box_pos):          
                  if not self.board.is_initialized():
                    self.board.init(box_pos)
                  self.board.open(box_pos)
                  if self.board.is_mine(box_pos):
                    # Game Over
                    self.game.terminate()
                    pass
              elif event.button == 2:
                directions = ((-1,-1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
                flaged = 0
                for direction in directions:
                  if self.board.is_flaged((box_pos[0]+direction[0], box_pos[1]+direction[1])):
                    flaged = flaged + 1
                if self.board.is_opened(box_pos) and self.board.get_number(box_pos) == flaged:
                  for direction in directions:
                    self.board.open((box_pos[0]+direction[0], box_pos[1]+direction[1]))
                    if self.board.is_mine((box_pos[0]+direction[0], box_pos[1]+direction[1])) and not self.board.is_flaged((box_pos[0]+direction[0], box_pos[1]+direction[1])):
                      # Game Over
                      self.game.terminate()
              elif event.button == 3:
                # Set Flag
                if not self.board.is_opened(box_pos):
                  self.board.toggle_flag(box_pos)
              