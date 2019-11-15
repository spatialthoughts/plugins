from qgis.gui import QgsMapTool, QgsRubberBand, QgsMapToolEmitPoint
from qgis.core import QgsWkbTypes

from qgis.PyQt.QtCore import Qt, pyqtSignal
from qgis.PyQt.QtWidgets import QDialog, QLineEdit, QDialogButtonBox, \
    QGridLayout, QLabel, QGroupBox, QVBoxLayout, QComboBox, QPushButton, \
    QInputDialog
from qgis.PyQt.QtGui import QKeySequence

from math import sqrt, pi, cos, sin

class DrawLine(QgsMapTool):
    selectionDone = pyqtSignal()
    move = pyqtSignal()

    def __init__(self, iface, color):
        canvas = iface.mapCanvas()
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.iface = iface
        self.status = 0
        self.rb = QgsRubberBand(self.canvas, QgsWkbTypes.LineGeometry)
        self.rb.setColor(color)
        return None

    def keyPressEvent(self, e):
        if e.matches(QKeySequence.Undo):
            if self.rb.numberOfVertices() > 1:
                self.rb.removeLastPoint()

    def canvasPressEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self.status == 0:
                self.rb.reset(QgsWkbTypes.LineGeometry)
                self.status = 1
            self.rb.addPoint(self.toMapCoordinates(e.pos()))
        else:
            if self.rb.numberOfVertices() > 2:
                self.status = 0
                self.selectionDone.emit()
            else:
                self.reset()
        return None

    def canvasMoveEvent(self, e):
        if self.rb.numberOfVertices() > 0 and self.status == 1:
            self.rb.removeLastPoint(0)
            self.rb.addPoint(self.toMapCoordinates(e.pos()))
        self.move.emit()
        return None

    def reset(self):
        self.status = 0
        self.rb.reset(QgsWkbTypes.LineGeometry)

    def deactivate(self):
        self.rb.reset(QgsWkbTypes.LineGeometry)
        QgsMapTool.deactivate(self)

