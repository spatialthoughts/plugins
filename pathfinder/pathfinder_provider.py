import os
import inspect
from PyQt5.QtGui import QIcon

from qgis.core import QgsProcessingProvider
from .least_cost_path import LeastCostPathAlgorithm


class PathFinderProvider(QgsProcessingProvider):

    def __init__(self):
        QgsProcessingProvider.__init__(self)

    def unload(self):
        pass

    def loadAlgorithms(self):
        self.addAlgorithm(LeastCostPathAlgorithm())

    def id(self):
        return 'pathfinder'

    def name(self):
        return self.tr('Path Finder')

    def icon(self):
        cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        icon = QIcon(os.path.join(os.path.join(cmd_folder, 'deer.svg')))
        return icon

    def longName(self):
        return self.name()