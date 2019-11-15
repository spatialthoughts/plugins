import os
import sys
import inspect
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon, QColor

from qgis.core import QgsProcessingAlgorithm, QgsApplication
import processing
from .pathfinder_provider import PathFinderProvider
from .drawline import DrawLine

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

class PathFinderPlugin:
    def __init__(self, iface):
        self.iface = iface

    def initProcessing(self):
      self.provider = PathFinderProvider()
      QgsApplication.processingRegistry().addProvider(self.provider)
        
    def initGui(self):
      self.initProcessing()
      icon = os.path.join(os.path.join(cmd_folder, 'deer.svg'))
      self.action = QAction(QIcon(icon), 'Find Least Cost Path', self.iface.mainWindow())
      self.action.triggered.connect(self.run)
      self.iface.addPluginToMenu('&PathFinder', self.action)
      self.iface.addToolBarIcon(self.action)


      draw_icon = os.path.join(os.path.join(cmd_folder, 'draw.png'))
      self.draw_action = QAction(QIcon(draw_icon), 'Draw Line', self.iface.mainWindow())
      self.draw_action.triggered.connect(self.draw_line)
      self.iface.addToolBarIcon(self.draw_action)


    def unload(self):
      QgsApplication.processingRegistry().removeProvider(self.provider)
      self.iface.removeToolBarIcon(self.action)
      self.iface.removeToolBarIcon(self.draw_action)

      self.iface.removePluginMenu('&PathFinder', self.action)  
      del self.action
      del self.draw_action

    def run(self):
      processing.execAlgorithmDialog('pathfinder:least_cost_path')
      
    def draw_line(self):
      color = QColor(60, 151, 255, 255)
      self.tool = DrawLine(self.iface, color)
      self.tool.setAction(self.draw_action)
      self.tool.selectionDone.connect(self.draw)
      self.iface.mapCanvas().setMapTool(self.tool)

      
    def draw(self):
      rb = self.tool.rb
      points = rb.asGeometry().asPolyline()
      start_point = points[0]
      end_point = points[-1]
      
      params = {
          'DEM': 'dem',
          'FRICTION': 'friction',
          'SOURCE': '{},{}'.format(start_point.x(), start_point.y()),
          'DESTINATION': '{},{}'.format(end_point.x(), end_point.y()),
          'OUTPUT':'TEMPORARY_OUTPUT'
          }
      processing.runAndLoadResults("pathfinder:least_cost_path", params) 
