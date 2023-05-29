import copy
import math
import objc
from Foundation import NSPoint
from Foundation import NSClassFromString

class FilterHelper():

	def __init__(self, outlineStrokeWidth, insetWidth, thisLayer) -> None:
		super().__init__()
		self.sourceLayer = thisLayer
		self.outlineStrokeWidth = outlineStrokeWidth
		self.outlineLayer = copy.deepcopy(thisLayer)
		self.insetWidth = insetWidth
		self.insetLayer = copy.deepcopy(thisLayer)

	@objc.python_method
	def createOutlineGlyphCopy(self):
		for newPath in self.outlineLayer.shapes:
			newPath.setAttribute_forKey_(self.outlineStrokeWidth, "strokeWidth")
		self.outlineLayer.flattenOutlinesRemoveOverlap_origHints_secondaryPath_extraHandles_error_(False,None,None,None,None)
		return self.outlineLayer.shapes
		
	@objc.python_method
	def createInsetGlyphCopy(self):
		for newPath in self.insetLayer.shapes:
			newPath.setAttribute_forKey_(self.insetWidth, "strokeWidth")
		self.insetLayer.flattenOutlinesRemoveOverlap_origHints_secondaryPath_extraHandles_error_(False,None,None,None,None)
		self.insetLayer.removeOverlap()
		self.insetLayer.shapes = self.removeOuter(self.insetLayer)
		if len(self.insetLayer.shapes) > 1:
			self.insetLayer.shapes = self.removeCounter(self.insetLayer)
		self.insetLayer.cutBetweenPoints(NSPoint(0, 189), NSPoint(500, self.getAngleEndCoordinates(500, 189, 45)))
		shapes = self.removeUpper(self.insetLayer, 189, 45)
		return shapes[0] + shapes[1]
	
	@objc.python_method
	def removeUpper(self, layer, yInitial, theta):
		lower = []
		upper = []
		errormargin = 1
		print("running removeUpper " + str(len(layer.shapes)))
		for myShape in layer.shapes:			
			isBelow = True
			for node in myShape.nodes:
				y_final = self.getAngleEndCoordinates(node.position.x, yInitial, theta)
				if (node.position.y - errormargin) >= y_final:
					isBelow = False
			if isBelow:
				print("adding shape : " + str(myShape))
				lower.append(myShape)
			else:
				upper.append(myShape)
		layerCopy = copy.deepcopy(layer)
		layerCopy.shapes = lower
		lower = self.hatchLayer(layerCopy, theta)
		return [lower, upper]

	@objc.python_method
	def hatchLayer(self, layer, theta):
		HatchOutlineFilter = NSClassFromString("HatchOutlineFilter")
		HatchOutlineFilter.hatchLayer_origin_stepWidth_angle_offset_checkSelection_shadowLayer_(layer, (10, 10), 20, theta, 0, False, None)
		return layer.shapes
				
	@objc.python_method
	def getAngleEndCoordinates(self, x, y, theta):
		theta_rad = math.radians(theta)
		delta_y = math.tan(theta_rad) * x
		y_final = y + delta_y
		return round(y_final)
	
	@objc.python_method
	def findMinMax(self, thisLayer):
		minx = -1 
		miny = -1
		maxx = -1
		maxy = -1
		for shape in thisLayer.shapes:
			for node in shape.nodes:
				if(minx > node.position.x or minx == -1):
					minx = node.position.x
				if(miny > node.position.y or miny == -1):
					miny = node.position.y
				if(maxx < node.position.x or maxx == -1):
					maxx = node.position.x
				if(maxy < node.position.y or maxy == -1):
					maxy = node.position.y
		return [minx, miny, maxx, maxy]

	@objc.python_method
	def removeCounter(self, thisLayer):
		shapes = []
		minMax = self.findMinMax(thisLayer)
		for myShape in thisLayer.shapes:
			addShape = False
			for node in myShape.nodes:
				if(node.position.x == minMax[0]):
					addShape = True
				if(node.position.y == minMax[1]):
					addShape = True
				if(node.position.x == minMax[2]):
					addShape = True
				if(node.position.y == minMax[3]):
					addShape = True
			if addShape == True:
				shapes.append(myShape)
		return shapes

	@objc.python_method
	def removeOuter(self, thisLayer):
		shapes = []
		minMax = self.findMinMax(thisLayer)
		for myShape in thisLayer.shapes:
			if(self.isShapeOuter(myShape, minMax) == False):
				shapes.append(myShape)
		return shapes

	@objc.python_method
	def isShapeOuter(self, myShape, minMax):
		minx = False
		miny = False
		maxx = False
		maxy = False
		for node in myShape.nodes:
			if(node.position.x == minMax[0]):
				minx = True
			if(node.position.y == minMax[1]):
				miny = True
			if(node.position.x == minMax[2]):
				maxx = True
			if(node.position.y == minMax[3]):
				maxy = True
		return minx and miny and maxx and maxy

