import objc
import copy
from GlyphsApp import *
from GlyphsApp.plugins import *
from Foundation import NSMakePoint
from effects import ThorTypeEffects

class CircleEffect():

	def __init__(self) -> None:
		super().__init__()

	@objc.python_method
	def drawCircleColumn(self, originLayer, circlesOrigin, circlesRadius, circlesDistance, circlesAngle, circlesStart, circlesEnd):
		effects = ThorTypeEffects()
		layer = effects.hatchLayerWithOrigin(copy.deepcopy(originLayer), circlesAngle, 0, circlesDistance, circlesOrigin)
		shapes = []
		for myShape in layer.shapes.values()[(int(circlesStart)):-(int(circlesEnd))]:
			x = round((myShape.nodes[0].position.x + myShape.nodes[1].position.x) / 2, 1)
			y = round((myShape.nodes[0].position.y + myShape.nodes[1].position.y) / 2, 1)
			circle = self.drawCircle([x, y], circlesRadius)
			shapes.append(circle)
		layer.shapes = shapes
		return layer

	@objc.python_method
	def drawCircle(self, origin, radius):
		circle = GSPath()
		half = radius * 0.55
		at = [0, half, radius, -half, -radius]
		table = [(1, 4), (2, 3), (2, 0), (2, 1), (1, 2), (0, 2), (3, 2), (4, 1), (4, 0), (4, 3), (3, 4), (0, 4)]
		nodes = []
		for i, (x_index, y_index) in enumerate(table):
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