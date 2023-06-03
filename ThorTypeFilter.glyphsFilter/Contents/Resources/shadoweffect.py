import copy
import math
import objc
from Foundation import NSPoint
from Foundation import NSClassFromString

from GlyphsApp import *
from GlyphsApp.plugins import *
from GlyphsApp import subtractPaths as subtractPaths

from AppKit import NSAffineTransform, NSAffineTransformStruct
from Foundation import NSClassFromString


class ShadowEffect():
	
	def __init__(self, outlineStrokeWidth) -> None:
		super().__init__()
		self.outlineStrokeWidth = outlineStrokeWidth
		self.extrudeFilter = NSClassFromString("Extrude").new()
	
	@objc.python_method
	def prepareOutlineForShadow(self, sourceLayer):
		layer = copy.deepcopy(sourceLayer)
		for newPath in layer.shapes:
			newPath.setAttribute_forKey_(self.outlineStrokeWidth, "strokeWidth")
		layer.flattenOutlinesRemoveOverlap_origHints_secondaryPath_extraHandles_error_(False,None,None,None,None)
		layer.shapes = layer.shapes + sourceLayer.shapes
		layer.removeOverlap()
		return layer

	# Actual filter
	@objc.python_method
	def filter(self, thisLayer):
		self.extrudeFilter.setOffset_(60)
		self.extrudeFilter.setAngle_(-45)
		layer = copy.deepcopy(thisLayer)
		self.extrudeFilter.processLayer_(layer)
		return layer

