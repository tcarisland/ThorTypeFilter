import copy
import math
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
from Foundation import NSMakePoint

class ThorTypeEffects():

    def __init__(self) -> None:
        super().__init__()

    @objc.python_method
    def getAngleEndCoordinates(self, x, y, theta):
        theta_rad = math.radians(theta)
        delta_y = math.tan(theta_rad) * x
        y_final = y + delta_y
        return round(y_final)

    @objc.python_method
    def createOutlineHatch(self, sourceLayer, strokeWidth, hatchDistance, theta, yStart, descender, height):
        x = sourceLayer.width
        y = yStart + height
        y_final = self.getAngleEndCoordinates(x, y, theta)
        i = 0
        shapes = []	
        hatchLayer = copy.deepcopy(sourceLayer)
        while y_final > descender and abs(y_final) < 2000: 
            start = GSNode()
            end = GSNode()
            start.type = "LINE"
            end.type = "LINE"
            start.position = NSMakePoint(0, y)
            end.position = NSMakePoint(x, y_final)
            line = GSPath()
            line.setAttribute_forKey_(strokeWidth, "strokeWidth")
            line.closed = False
            line.nodes = [start, end]
            shapes.append(line)
            y -= hatchDistance
            y_final = self.getAngleEndCoordinates(x, y, theta)
        hatchLayer.shapes = shapes
        hatchLayer.flattenOutlinesRemoveOverlap_origHints_secondaryPath_extraHandles_error_(False,None,None,None,None)
        hatchLayer.cleanUpPaths()
        hatchLayer.removeOverlap()
        return hatchLayer.shapes