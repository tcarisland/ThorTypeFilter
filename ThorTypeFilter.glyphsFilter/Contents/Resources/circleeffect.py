# noinspection PyUnresolvedReferences
import objc
import copy
# noinspection PyUnresolvedReferences
from GlyphsApp import *
# noinspection PyUnresolvedReferences
from GlyphsApp.plugins import *
# noinspection PyUnresolvedReferences
from Foundation import NSMakePoint
from effects import ThorTypeEffects

class CircleEffect():

	def __init__(self) -> None:
		super().__init__()

	@objc.python_method
	def drawCircleColumn(self, originLayer, circlesOrigin, circlesRadius, circlesDistance, circlesAngle, circlesStart, circlesEnd):
		shapes = []
		layers = self.splitByShapesAndHatchIndividually(originLayer, circlesOrigin, circlesDistance, circlesAngle)
		for layer in layers: 
			for myShape in layer.shapes.values()[(int(circlesStart)):-(int(circlesEnd))]:
				x = round((myShape.nodes[0].position.x + myShape.nodes[1].position.x) / 2, 1)
				y = round((myShape.nodes[0].position.y + myShape.nodes[1].position.y) / 2, 1)
				circle = self.drawCircle([x, y], circlesRadius)
				shapes.append(circle)
		resultLayer = copy.deepcopy(originLayer)
		resultLayer.shapes = shapes
		return resultLayer
	
	@objc.python_method
	def splitByShapesAndHatchIndividually(self, originLayer, circlesOrigin, circlesDistance, circlesAngle):
		hatchLayers = []
		effects = ThorTypeEffects()
		for myLayer in self.splitLayer(originLayer):
			myLayer = effects.hatchLayerWithOrigin(copy.deepcopy(myLayer), circlesAngle, 0, circlesDistance, circlesOrigin)
			hatchLayers.append(myLayer)
		return hatchLayers
	
	@objc.python_method
	def splitLayer(self, originLayer):
		layers = []
		for myShape in originLayer.shapes.values():
			layer = copy.deepcopy(originLayer)
			layer.shapes = [myShape]
			layers.append(layer)
		return layers

	@objc.python_method
	def drawCircle(self, origin, radius):
		# noinspection PyUnresolvedReferences
		circle = GSPath()
		half = radius * 0.55
		at = [0, half, radius, -half, -radius]
		table = [(1, 4), (2, 3), (2, 0), (2, 1), (1, 2), (0, 2), (3, 2), (4, 1), (4, 0), (4, 3), (3, 4), (0, 4)]
		nodes = []
		for i, (x_index, y_index) in enumerate(table):
			# noinspection PyUnresolvedReferences
			node = GSNode()
			if (i + 1) % 3 == 0:
				node.type = "curve"
				node.smooth = True
			else:
				node.type = "offcurve"
			node.position = NSMakePoint(origin[0] + at[x_index], origin[1] + at[y_index])
			nodes.append(node)
		circle.nodes = nodes
		circle.closed = True
		return circle
