from datetime import datetime
from os import path

from pyabm.common.conf import Conf
from pyabm.common.singleton import Singleton


class Workspace(metaclass=Singleton):

    def __init__(self, root=None, execution_parameters=None):
        """Workspace.

        :param root: url path of the workspace
        :param execution_parameters: Dictionary with the execution parameters required only for some processes, for
        example, days_to_load_from_portfolio_catalog parameter.
        """
        self.root = root
        self.pyabm_conf_path = path.join(self.root, "setup", "pyabm.json")
        self.conf = Conf(self.pyabm_conf_path)
        self.execution_parameters = execution_parameters
