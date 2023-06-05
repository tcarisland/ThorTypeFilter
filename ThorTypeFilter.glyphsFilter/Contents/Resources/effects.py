import copy
import math
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
from Foundation import NSMakePoint
from Foundation import NSClassFromString

class ThorTypeEffects():

	def __init__(self) -> None:
		super().__init__()

	@objc.python_method
	def getAngleEndCoordinates(self, x, y, theta):
		theta_rad = math.radians(theta)
		delta_y = math.tan(theta_rad) * x
		y_final = y + delta_y
		return round(y_final)

	@objc.python_method
	def hatchLayer(self, layer, theta, hatchStroke, hatchStep):
		HatchOutlineFilter = NSClassFromString("HatchOutlineFilter")
		HatchOutlineFilter.hatchLayer_origin_stepWidth_angle_offset_checkSelection_shadowLayer_(layer, (0, 0), hatchStep, theta, 0, False, None)
		for myShape in layer.shapes:
			myShape.setAttribute_forKey_(hatchStroke, "strokeWidth")
			myShape.setAttribute_forKey_(2, "lineCapEnd")
			myShape.setAttribute_forKey_(2, "lineCapStart")
		return layer
	
	@objc.python_method
	def hatchLayerWithOrigin(self, layer, theta, hatchStroke, hatchStep, hatchOrigin):
		HatchOutlineFilter = NSClassFromString("HatchOutlineFilter")
		HatchOutlineFilter.hatchLayer_origin_stepWidth_angle_offset_checkSelection_shadowLayer_(layer, (0, int(hatchOrigin)), hatchStep, theta, 0, False, None)
		for myShape in layer.shapes:
			myShape.setAttribute_forKey_(hatchStroke, "strokeWidth")
			myShape.setAttribute_forKey_(2, "lineCapEnd")
			myShape.setAttribute_forKey_(2, "lineCapStart")
		return layer