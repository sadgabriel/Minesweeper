import pygame
from . import sprite

class Scene:
  def __init__(self, game):
    self.game = game
    
    # the Group to hold all sprites
    #self.all_sprites = sprite.Group()
    self.all_sprites = sprite.Group()
  
  def handle_events(self, events): # handle unhandled events by Game
    pass
  
  def update(self): # update all the things
    self.all_sprites.update()
  
  def render(self): # render the scene to self.game.screen. flip is not necessary
    self.all_sprites.draw(self.game.screen)



##########TESTING
class TestScene(Scene):
  def __init__(self, game):
    super().__init__(game)
    self.text1 = sprite.Text("Text1", (120, 120), 60)
    self.text2 = sprite.Text("Text2", (120, 130), 40)
    self.all_sprites.add(self.text1)
    self.all_sprites.add(self.text2)

    self.bgd = self.game.screen.copy()
    self.bgd.fill((0, 0, 0))

  def handle_events(self, events):
    for event in events:
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_1:
          self.game.screen.fill((255, 0, 0))
        elif event.key == pygame.K_2:
          self.text1.dirty = 1
        elif event.key == pygame.K_3:
          self.text1.rect.x = self.text1.rect.x + 30
        elif event.key == pygame.K_4:
          self.text2.kill()
        elif event.key == pygame.K_5:
          self.all_sprites.clear(self.game.screen, self.bgd)
          
  def render(self):
    self.all_sprites.draw(self.game.screen, self.bgd)