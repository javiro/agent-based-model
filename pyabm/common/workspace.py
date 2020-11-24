from os import path

from pyabm.common.conf import Conf
from pyabm.common.singleton import Singleton


class Workspace(metaclass=Singleton):

    def __init__(self):
        """Workspace."""
        self.pyabm_conf_path = path.join("resources", "conf", "pyabm.json")
        self.conf = Conf(self.pyabm_conf_path)
