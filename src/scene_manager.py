class SceneManager:
  """Manage Scenes"""
  def __init__(self):
    self._scenes = dict()
    self._current_scene = None
    self._current_scene_name = None
    self._next_scene_name = None

  def init(self, scene_name, scene):
    self.add(scene_name, scene)
    self._current_scene = scene
    self._current_scene_name = scene_name

  def add(self, scene_name, scene):
    if scene_name and scene_name not in self._scenes:
      self._scenes[scene_name] = scene
    else:
      raise KeyError("Invaild Key")

  def remove(self, scene_name):
    if scene_name in self._scenes:
      self._scenes.pop(scene_name)
    else:
      raise KeyError("Invaild Key")

  def modify(self, scene_name, scene):
    self.remove(scene_name)
    self.add(scene_name, scene)

  def get_scene(self, scene_name):
    if scene_name in self._scenes:
      return self._scenes[scene_name]
    else:
      raise KeyError("Invaild Key")

  def get_current_name(self):
    return self._current_scene_name

  def get_next_name(self):
    return self._next_scene_name

  def set_next_scene(self, scene_name, scene=None):
    if scene_name in self._scenes:
      self._next_scene_name = scene_name
    elif scene:
      self.add(scene_name, scene)
      self._next_scene_name = scene_name
    else:
      raise KeyError("Invaild Key")

  def get_current_scene(self):
    return self._current_scene

  def _update(self):
    if self._next_scene_name and self._next_scene_name in self._scenes:
      self._current_scene_name = self._next_scene_name
      self._current_scene = self.get(self.get_current())
    self._next_scene_name = None
    