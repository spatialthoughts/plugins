import os
import tempfile
from PyQt5.QtCore import QCoreApplication
from qgis.core import (QgsRasterLayer, QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterPoint,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterVectorDestination,
                       QgsProcessingParameterRasterDestination)
import processing


class LeastCostPathAlgorithm(QgsProcessingAlgorithm):
    """Finds least cost path between points."""
    DEM = 'DEM'
    FRICTION = 'FRICTION'
    OUTPUT = 'OUTPUT'
    SOURCE = 'SOURCE'
    DESTINATION = 'DESTINATION'

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.DEM,
                self.tr('DEM'),
                [QgsProcessing.TypeRaster]
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.FRICTION,
                self.tr('Friction Costs'),
                [QgsProcessing.TypeRaster]
            )
        )
        
        self.addParameter(
            QgsProcessingParameterPoint(
                self.SOURCE,
                self.tr('Source Point'),
                '235564.498984,2925756.770703'
            )
        )
        
        self.addParameter(
            QgsProcessingParameterPoint(
                self.DESTINATION,
                self.tr('Destination Point'),
                '252452.475080,2928656.726195',
            )
        )
        
        
        self.addParameter(
            QgsProcessingParameterVectorDestination(
                self.OUTPUT,
                self.tr('Least Cost Path'),
            )
        )

     
        
        
    def processAlgorithm(self, parameters, context, feedback):
        dem = self.parameterAsRasterLayer(parameters, self.DEM, context)
        friction = self.parameterAsRasterLayer(parameters, self.FRICTION, context)
        source_point = 	self.parameterAsPoint(parameters, self.SOURCE, context)
        dest_point = self.parameterAsPoint(parameters, self.DESTINATION, context)
        source_x, source_y = source_point.x(), source_point.y()
        dest_x, dest_y = dest_point.x(), dest_point.y()
        output_file = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)
    
        tf = tempfile.TemporaryDirectory()
        direction = os.path.join(tf.name, 'direction.tif')

        params = {
            'elevation': dem,
            'friction': friction,
            'start_coordinates':'{},{}'.format(source_x, source_y),
            'stop_coordinates': '{},{}'.format(dest_x, dest_y),
            'output': 'TEMPORARY_OUTPUT',
            'outdir': direction,
            }
            
         
        output = processing.run("grass7:r.walk.coords", params)
        print(output)
        
        params = {
            'input':dem,
            'direction':output['outdir'],
            'start_coordinates':'{},{}'.format(dest_x, dest_y),
            'output':'TEMPORARY_OUTPUT',
            'drain': output_file,
            'GRASS_OUTPUT_TYPE_PARAMETER':2
            }
            
        results = processing.run("grass7:r.drain", params)
        
        return { self.OUTPUT: results['drain']}

    def name(self):
        return 'least_cost_path'

    def displayName(self):
        return self.tr('Least Cost Path')

    def group(self):
        return self.tr(self.groupId())

    def groupId(self):
        return ''

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return LeastCostPathAlgorithm()