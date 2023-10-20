import copy
# noinspection PyUnresolvedReferences
import objc
# noinspection PyUnresolvedReferences
from Foundation import NSPoint
# noinspection PyUnresolvedReferences
from Foundation import NSClassFromString

# noinspection PyUnresolvedReferences
from GlyphsApp import *
# noinspection PyUnresolvedReferences
from GlyphsApp.plugins import *
# noinspection PyUnresolvedReferences
from GlyphsApp import subtractPaths as subtractPaths

# noinspection PyUnresolvedReferences
from AppKit import NSAffineTransform, NSAffineTransformStruct
# noinspection PyUnresolvedReferences
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
	def applyShadow(self, thisLayer, shadowOffset, shadowAngle):
		self.extrudeFilter.setOffset_(shadowOffset)
		self.extrudeFilter.setAngle_(shadowAngle)
		layer = copy.deepcopy(thisLayer)
		self.extrudeFilter.processLayer_(layer)
		return layer

