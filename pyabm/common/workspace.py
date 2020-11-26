import os

from pyabm.common.conf import Conf
from pyabm.common.constants import WORKSPACE, OUTPUTS
from pyabm.common.singleton import Singleton


class Workspace(metaclass=Singleton):

    def __init__(self):
        """Workspace."""
        self.root = WORKSPACE
        if not os.path.exists(self.root):
            os.mkdir(self.root)
        if not os.path.exists(os.path.join(self.root, OUTPUTS)):
            os.mkdir(os.path.join(self.root, OUTPUTS))
        self.pyabm_conf_path = os.path.join("resources", "conf", "pyabm.json")
        self.conf = Conf(self.pyabm_conf_path)
