import pygame, sys
from . import scene_manager
from . import scene

class Game:
  """Main Game Class"""
  def __init__(self, screen_width, screen_height, fps):
    if (pygame.init()[1]): # initialize pygame
      print("Some Errors Occur on initializing pygame")
      sys.exit(-1)

    # set clock and fps
    self._main_clock = pygame.time.Clock()
    self._fps = fps

    # flag to terminate the game
    self._running = False

    # make screen and set caption
    self.screen = pygame.display.set_mode((screen_width, screen_height))

    # set SceneManager and current scene
    self.scene_manager = scene_manager.SceneManager()

  def init(self, starting_scene_name, starting_scene):
    self.scene_manager.init(starting_scene_name, starting_scene)
  
  def terminate(self):
    self._running = False

  def _handle_events(self):
    raw_events = pygame.event.get()
    events = list()
    for event in raw_events:
      # preprocessing events
      if event.type == pygame.QUIT:
        self.terminate()
      else:
        events.append(event)
    self.scene_manager.current.handle_events(events)  # throw left events to current scene

  def _update(self):
    # update scene and set next scene if exists
    self.scene_manager.current.update()

  def _render(self):
    self.scene_manager.current.render()
    pygame.display.flip()

  def run(self):
    self._running = True

    while (self._running):  # if self.running is false, the game terminates
      self._main_clock.tick(self._fps)  # FPS control

      self._handle_events()

      self._update()

      self._render()

      self.scene_manager.update()

    pygame.quit()


##########TESTING
if __name__ == "__main__":
  game = Game(1080, 720, 60)
  game.init("TestScene", scene.TestScene(game))
  game.run()