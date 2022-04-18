import pygame
import scene
import definition
import scene_manager
import sys

class Game:
  """Main Game Class"""
  def __init__(self):
    if (pygame.init()[1]): # initialize pygame
      print("An Error Occurs on initializing pygame")
      sys.exit(-1)

    # set clock
    self._main_clock = pygame.time.Clock()

    # flag to terminate the game
    self._running = False

    # make screen and set caption
    self.screen = pygame.display.set_mode((definition.WIDTH, definition.HEIGHT))
    self._set_caption()

    # set SceneManager
    self.scene_manager = scene_manager.SceneManager()
    self._init_scene_manager()

  def _set_caption(self):
    #pygame.display.set_caption("Caption")
    pass

  def _init_scene_manager(self):
    #self.scene_manager.init("default", scene.Scene(self))
    raise Exception("Scene Manager is not initialized")
  
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
    self.scene_manager.get_current_scene().handle_events(events)  # throw left events to current scene

  def _update(self):
    # update scene and set next scene if exists
    self.scene_manager.get_current_scene().update()

  def _render(self):
    self.scene_manager.get_current_scene().render()
    pygame.display.flip()

  def run(self):
    self._running = True

    while (self._running):  # if self.running is false, the game terminates
      self._main_clock.tick(definition.FPS)  # FPS control

      self._handle_events()

      self._update()

      self._render()

      self.scene_manager._update()

    pygame.quit()


class Minesweeper(Game):
  def _set_caption(self):
    pygame.display.set_caption("Minesweeper")

  def _init_scene_manager(self):
    self.scene_manager.init("main", scene.MainScene(self))

if __name__ == "__main__":
  game = Minesweeper()
  game.run()
