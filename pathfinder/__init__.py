from .pathfinder import PathFinderPlugin

def classFactory(iface):
    return PathFinderPlugin(iface)