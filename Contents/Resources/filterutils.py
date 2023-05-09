import copy
import objc
from effects import ThorTypeEffects

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

		thorTypeEffects = ThorTypeEffects()
		hatchShapes = thorTypeEffects.hatchOutline(self.insetLayer, 10, 30, 45, 100, -200, 800)
		return hatchShapes
		
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

	@objc.python_method
	def runFilter(self):
		outlineShapes = self.createOutlineGlyphCopy()
		insetShapes = self.createInsetGlyphCopy()
		self.sourceLayer.shapes = outlineShapes + insetShapes

