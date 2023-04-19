import copy
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
from GlyphsApp import subtractPaths as subtractPaths

@objc.python_method
def createOutlineGlyphCopy(myGlyph, thisLayer, strokeWidth):
	print("createOutlineGlyphCopy")
	newGlyph = GSGlyph()
	newGlyph.name = myGlyph.name + ".0001"
	newGlyph.layers = copy.deepcopy(myGlyph.layers)
	for newPath in thisLayer.paths:
		newPath.setAttribute_forKey_(strokeWidth, "strokeWidth")
		
	newGlyph.layers[0].flattenOutlinesRemoveOverlap_origHints_secondaryPath_extraHandles_error_(False,None,None,None,None)
	Glyphs.font.glyphs[newGlyph.name] = newGlyph
	
@objc.python_method
def createInsetGlyphCopy(myGlyph, thisLayer, strokeWidth):
	newGlyph = GSGlyph()
	newGlyph.name = myGlyph.name + ".0002"
	newGlyph.layers = copy.deepcopy(myGlyph.layers)	
	for newPath in newGlyph.layers[0].paths:
		newPath.setAttribute_forKey_(strokeWidth, "strokeWidth")
		
	newGlyph.layers[0].flattenOutlinesRemoveOverlap_origHints_secondaryPath_extraHandles_error_(False,None,None,None,None)
	newGlyph.layers[0].removeOverlap()
	newGlyph = removeOuter(newGlyph, newGlyph.layers[0])
	if len(thisLayer.shapes) > 1:
		newGlyph = removeCounter(newGlyph)
	Glyphs.font.glyphs[newGlyph.name] = newGlyph
	
@objc.python_method
def findMinMax(myGlyph, thisLayer):
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
def removeCounter(myGlyph, thisLayer):
	shapes = []
	minMax = findMinMax(myGlyph, thisLayer)
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
	thisLayer.shapes = shapes
	return myGlyph

@objc.python_method
def removeOuter(myGlyph, thisLayer):
	shapes = []
	minMax = findMinMax(myGlyph, thisLayer)
	for myShape in thisLayer.shapes:
		if(isShapeOuter(myShape, minMax) == False):
			shapes.append(myShape)
	thisLayer.shapes = shapes
	return myGlyph

@objc.python_method
def isShapeOuter(myShape, minMax):
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
def runFilter(glyph, thisLayer):
	createOutlineGlyphCopy(glyph, thisLayer, 10)
	createInsetGlyphCopy(glyph, thisLayer, 30)

