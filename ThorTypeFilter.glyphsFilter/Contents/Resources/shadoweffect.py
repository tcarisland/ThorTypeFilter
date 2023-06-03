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

@objc.python_method
def offsetTheLayer( thisLayer, offsetX, offsetY, makeStroke=False, position=0.5, autoStroke=False ):
	offsetFilter = NSClassFromString("GlyphsFilterOffsetCurve")
	try:
		# GLYPHS 3:	
		offsetFilter.offsetLayer_offsetX_offsetY_makeStroke_autoStroke_position_metrics_error_shadow_capStyleStart_capStyleEnd_keepCompatibleOutlines_(
			thisLayer,
			offsetX, offsetY, # horizontal and vertical offset
			makeStroke,     # if True, creates a stroke
			autoStroke,     # if True, distorts resulting shape to vertical metrics
			position,       # stroke distribution to the left and right, 0.5 = middle
			None, None, None, 0, 0, False )
	except:
		# GLYPHS 2:
		offsetFilter.offsetLayer_offsetX_offsetY_makeStroke_autoStroke_position_error_shadow_(
			thisLayer,
			offsetX, offsetY, # horizontal and vertical offset
			makeStroke,     # if True, creates a stroke
			autoStroke,     # if True, distorts resulting shape to vertical metrics
			position,       # stroke distribution to the left and right, 0.5 = middle
			None, None )


@objc.python_method
def transform(shiftX=0.0, shiftY=0.0, rotate=0.0, skew=0.0, scale=1.0):
	myTransform = NSAffineTransform.transform()
	if rotate:
		myTransform.rotateByDegrees_(rotate)
	if scale != 1.0:
		myTransform.scaleBy_(scale)
	if not (shiftX == 0.0 and shiftY == 0.0):
		myTransform.translateXBy_yBy_(shiftX,shiftY)
	if skew:
		skewStruct = NSAffineTransformStruct()
		skewStruct.m11 = 1.0
		skewStruct.m22 = 1.0
		skewStruct.m21 = math.tan(math.radians(skew))
		skewTransform = NSAffineTransform.transform()
		skewTransform.setTransformStruct_(skewStruct)
		myTransform.appendTransform_(skewTransform)
	return myTransform

class ShadowEffect():
	
	def __init__(self, outlineStrokeWidth) -> None:
		super().__init__()
		self.outlineStrokeWidth = outlineStrokeWidth
	
	@objc.python_method
	def prepareOutlineForShadow(self, sourceLayer):
		layer = copy.deepcopy(sourceLayer)
		for newPath in layer.shapes:
			newPath.setAttribute_forKey_(self.outlineStrokeWidth, "strokeWidth")
		layer.flattenOutlinesRemoveOverlap_origHints_secondaryPath_extraHandles_error_(False,None,None,None,None)
		layer.shapes = layer.shapes + sourceLayer.shapes
		layer.removeOverlap()
		return layer
	
	@objc.python_method
	def mergeLayerIntoLayer(self, sourceLayer, targetLayer):
		for p in sourceLayer.paths:
			try:
				targetLayer.shapes.append(p.copy())
			except:
				targetLayer.paths.append(p.copy())

		# Actual filter
	@objc.python_method
	def filter(self, thisLayer):
		if not thisLayer is None: # circumvents a bug in 2.5b
			# fallback values:
			offset, offsetY, distanceX, distanceY = 15, 15, 15, 15
			
			offset = 0
			offsetY = 0
			distanceX = 45
			distanceY = 45
			
			thisLayer.decomposeComponents()
			offsetLayer = thisLayer.copy()
		
			# Create offset rim:
			if offset != 0.0:
				offsetTheLayer( offsetLayer, offset, offsetY, makeStroke=False, position=0.5, autoStroke=False )

			# Create and offset Shadow only if it has a distance:
			if distanceX != 0.0 or distanceY != 0.0:
				offsetMatrix = (1,0,0,1,distanceX,-distanceY)
				shadowLayer = offsetLayer.copy()
				shadowLayer.applyTransform( offsetMatrix )
				
				# only create shadow if there is no offset rim:
				if offset == 0.0:
					# prepare thisLayers for subtraction:
					thisLayer.removeOverlap()
					shadowLayer.removeOverlap()
					
					paths = shadowLayer.paths # list of original paths
					subPaths = thisLayer.paths # list of paths to be subtracted from original paths
					
					# transfer the subtraction result into the main thisLayer, and we are done:
					thesePaths = subtractPaths(list(paths), list(subPaths))
					if thesePaths:
						thisLayer.shapes = thesePaths
					
				# if there is an offset, merge rim and shadow thisLayers:
				else:
					try:
						offsetLayer.appendLayer_(shadowLayer)
					except:
						self.mergeLayerIntoLayer(shadowLayer,offsetLayer)
			thisLayer.removeOverlap()
			
			# if there is an offset, merge original paths with merged rim+shadow paths:
			if offset != 0.0:
				offsetLayer.removeOverlap()
				try:
					thisLayer.appendLayer_(offsetLayer)
				except:
					self.mergeLayerIntoLayer(offsetLayer,thisLayer)
			
			thisLayer.cleanUpPaths()
			thisLayer.correctPathDirection()
			return thisLayer.shapes.values()
	
