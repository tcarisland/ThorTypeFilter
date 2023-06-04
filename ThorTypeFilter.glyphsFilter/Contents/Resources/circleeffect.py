import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
from Foundation import NSMakePoint

class CircleEffect():

	def __init__(self) -> None:
		super().__init__()

	@objc.python_method
	def drawCircle(origin, radius):
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