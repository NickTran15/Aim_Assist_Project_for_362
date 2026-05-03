"Manages scene transistions"

class SceneManager:

    def __init__(self, scenes_list=None):
        self._scenes = scenes_list

    def __iter__(self):
        return iter(self._scenes)

    def add(self, scene):
        self._scenes.append(scene)
