from Foundation import NSMakePoint

def drawCircle(origin, radius):
	circle = GSPath()
	half = (radius * 0.55)
	at = [0, half, radius, -half, -radius]
	nodes = [None] * 12

	nodes[0] = GSNode()
	nodes[0].type = "offcurve"
	nodes[0].position = NSMakePoint(origin[0] + at[1], origin[1] + at[4])

	nodes[1] = GSNode()
	nodes[1].type = "offcurve"
	nodes[1].position = NSMakePoint(origin[0] + at[2], origin[1] + at[3])

	nodes[2] = GSNode()
	nodes[2].type = "curve"
	nodes[2].position = NSMakePoint(origin[0] + at[2], origin[1] + at[0])
	nodes[2].smooth = True

	nodes[3] = GSNode()
	nodes[3].type = "offcurve"
	nodes[3].position = NSMakePoint(origin[0] + at[2], origin[1] + at[1])

	nodes[4] = GSNode()
	nodes[4].type = "offcurve"
	nodes[4].position = NSMakePoint(origin[0] + at[1], origin[1] + at[2])

	nodes[5] = GSNode()
	nodes[5].type = "curve"
	nodes[5].position = NSMakePoint(origin[0] + at[0], origin[1] + at[2])
	nodes[5].smooth = True

	nodes[6] = GSNode()
	nodes[6].type = "offcurve"
	nodes[6].position = NSMakePoint(origin[0] + at[3], origin[1] + at[2])

	nodes[7] = GSNode()
	nodes[7].type = "offcurve"
	nodes[7].position = NSMakePoint(origin[0] + at[4], origin[1] + at[1])

	nodes[8] = GSNode()
	nodes[8].type = "curve"
	nodes[8].position = NSMakePoint(origin[0] + at[4], origin[1] + at[0])
	nodes[8].smooth = True

	nodes[9] = GSNode()
	nodes[9].type = "offcurve"
	nodes[9].position = NSMakePoint(origin[0] + at[4], origin[1] + at[3])

	nodes[10] = GSNode()
	nodes[10].type = "offcurve"
	nodes[10].position = NSMakePoint(origin[0] + at[3], origin[1] + at[4])

	nodes[11] = GSNode()
	nodes[11].type = "curve"
	nodes[11].position = NSMakePoint(origin[0] + at[0], origin[1] + at[4])
	nodes[11].smooth = True

	circle.nodes = nodes
	circle.closed = True
	return circle