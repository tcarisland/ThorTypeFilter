# encoding: utf-8

###########################################################################################################
#
#
#	Filter with dialog Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Filter%20with%20Dialog
#
#	For help on the use of Interface Builder:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
import objc
import copy
from GlyphsApp import *
from GlyphsApp.plugins import *
from Foundation import NSClassFromString
from filterutils import FilterHelper
from shadoweffect import ShadowEffect
from circleeffect import CircleEffect

class ThorTypeFilter(FilterWithDialog):

	prefID= "com.tcarisland.ThorTypeFilter"
	if Glyphs.versionNumber < 3:
		# GLYPHS 2
		pathOperator = NSClassFromString("GSPathOperator").alloc().init() # needs to be initialized only once

	# Definitions of IBOutlets
	# The NSView object from the User Interface. Keep this here!
	dialog = objc.IBOutlet()
	# Text field in dialog
	strokeWidthTextField = objc.IBOutlet()
	insetWidthTextField = objc.IBOutlet()
	hatchAngleTextField = objc.IBOutlet()
	hatchStepTextField = objc.IBOutlet()
	hatchStartYTextField = objc.IBOutlet()
	hatchStrokeTextField = objc.IBOutlet()
	shadowOffsetTextField = objc.IBOutlet()
	shadowAngleTextField = objc.IBOutlet()
	hatchOriginTextField = objc.IBOutlet()
	circlesAngleTextField = objc.IBOutlet()
	circlesDistanceTextField = objc.IBOutlet()
	circlesEndTextField = objc.IBOutlet()
	circlesOriginTextField = objc.IBOutlet()
	circlesRadiusTextField = objc.IBOutlet()
	circlesStartTextField = objc.IBOutlet()
	circlesCheckbox = objc.IBOutlet()
	aShadowColorComboBox = objc.IBOutlet()
	palette = objc.IBOutlet()
	paletteLength = objc.IBOutlet()

	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'ThorType Filter',
			'de': 'ThorType Filter',
			'fr': 'ThorType filtre',
			'es': 'ThorType filtro',
			'pt': 'ThorType filtro',
			})
		
		# Word on Run Button (default: Apply)
		self.actionButtonLabel = Glyphs.localize({
			'en': 'Apply',
			'de': 'Anwenden',
			'fr': 'Appliquer',
			'es': 'Aplicar',
			'pt': 'Aplique',
			})
		# Load dialog from .nib (without .extension)
		self.loadNib('IBdialog', __file__)

	# On dialog show
	@objc.python_method
	def start(self):
		# Set default value
		self.registerDefaults()
		# Set value of text field
		self.strokeWidthTextField.setStringValue_(self.pref('strokeWidth'))
		self.insetWidthTextField.setStringValue_(self.pref('insetWidth'))
		self.hatchAngleTextField.setStringValue_(self.pref('hatchAngle'))
		self.hatchStepTextField.setStringValue_(self.pref('hatchStep'))
		self.hatchStartYTextField.setStringValue_(self.pref('hatchStartY'))
		self.hatchStrokeTextField.setStringValue_(self.pref('hatchStroke'))
		self.shadowOffsetTextField.setStringValue_(self.pref('shadowOffset'))
		self.shadowAngleTextField.setStringValue_(self.pref('shadowAngle'))
		self.hatchOriginTextField.setStringValue_(self.pref('hatchOrigin'))
		self.circlesAngleTextField.setStringValue_(self.pref('circlesAngle'))
		self.circlesDistanceTextField.setStringValue_(self.pref('circlesDistance'))
		self.circlesEndTextField.setStringValue_(self.pref('circlesEnd'))
		self.circlesOriginTextField.setStringValue_(self.pref('circlesOrigin'))
		self.circlesRadiusTextField.setStringValue_(self.pref('circlesRadius'))
		self.circlesEndTextField.setStringValue_(self.pref('circlesEnd'))
		self.circlesStartTextField.setStringValue_(self.pref('circlesStart'))
		self.aShadowColorComboBox.setStringValue_(self.pref('aShadowColor'))
		self.circlesCheckbox.setState_(self.pref('circles'))

		#self.palette.setStringValue_(palette)
		#self.paletteLength.setIntegerValue_(len(palette))
		# Set focus to text field
		self.strokeWidthTextField.becomeFirstResponder()
		font = Glyphs.fonts[0]
		palette = font.customParameters['Color Palettes'][0]
		print(str(palette))
		print(str(len(palette)))
		self.update()

	@objc.python_method
	def registerDefaults(self, sender=None):
		Glyphs.registerDefault(self.domain('strokeWidth'), 10.0)
		Glyphs.registerDefault(self.domain('insetWidth'), 30.0)
		Glyphs.registerDefault(self.domain('hatchAngle'), 45.0)
		Glyphs.registerDefault(self.domain('hatchStep'), 20.0)
		Glyphs.registerDefault(self.domain('hatchStartY'), 189.0)
		Glyphs.registerDefault(self.domain('hatchStroke'), 10.0)
		Glyphs.registerDefault(self.domain('shadowOffset'), 45.0)
		Glyphs.registerDefault(self.domain('shadowAngle'), 315.0)
		Glyphs.registerDefault(self.domain('hatchOrigin'), 10.0)
		Glyphs.registerDefault(self.domain('circlesAngle'), 180.0)
		Glyphs.registerDefault(self.domain('circlesDistance'), 50.0)
		Glyphs.registerDefault(self.domain('circlesEnd'), 1)
		Glyphs.registerDefault(self.domain('circlesOrigin'), 0)
		Glyphs.registerDefault(self.domain('circlesRadius'), 30)
		Glyphs.registerDefault(self.domain('circlesStart'), 1)
		Glyphs.registerDefault(self.domain('circles'), 1)
		Glyphs.registerDefault(self.domain('aShadowColor'), "")


	@objc.python_method
	def domain(self, prefName):
		prefName = prefName.strip().strip(".")
		return self.prefID + "." + prefName.strip()

	@objc.python_method
	def pref(self, prefName):
		prefDomain = self.domain(prefName)
		return Glyphs.defaults[prefDomain]
	
	@objc.IBAction
	def setStrokeWidth_( self, sender ):
		Glyphs.defaults[self.domain('strokeWidth')] = sender.floatValue()
		self.update()

	@objc.IBAction
	def setInsetWidth_( self, sender):
		Glyphs.defaults[self.domain('insetWidth')] = sender.floatValue()
		self.update()

	@objc.IBAction
	def setHatchAngle_( self, sender):
		Glyphs.defaults[self.domain('hatchAngle')] = sender.floatValue()
		self.update()

	@objc.IBAction
	def setHatchStep_( self, sender):
		Glyphs.defaults[self.domain('hatchStep')] = sender.floatValue()
		self.update()

	@objc.IBAction
	def setHatchStartY_( self, sender):
		Glyphs.defaults[self.domain('hatchStartY')] = sender.floatValue()
		self.update()

	@objc.IBAction
	def setHatchStroke_( self, sender):
		Glyphs.defaults[self.domain('hatchStroke')] = sender.floatValue()
		self.update()

	@objc.IBAction
	def setShadowOffset_( self, sender):
		Glyphs.defaults[self.domain('shadowOffset')] = sender.floatValue()
		self.update()
		
	@objc.IBAction
	def setShadowAngle_( self, sender):
		Glyphs.defaults[self.domain('shadowAngle')] = sender.floatValue()
		self.update()

	@objc.IBAction
	def setHatchOrigin_( self, sender):
		Glyphs.defaults[self.domain('hatchOrigin')] = sender.floatValue()
		self.update()


	@objc.IBAction
	def setCirclesAngle_( self, sender):
		Glyphs.defaults[self.domain('circlesAngle')] = sender.floatValue()
		self.update()

	@objc.IBAction
	def setCirclesDistance_( self, sender):
		Glyphs.defaults[self.domain('circlesDistance')] = sender.floatValue()
		self.update()

	@objc.IBAction
	def setCirclesEnd_( self, sender):
		Glyphs.defaults[self.domain('circlesEnd')] = sender.floatValue()
		self.update()

	@objc.IBAction
	def setCirclesOrigin_( self, sender):
		Glyphs.defaults[self.domain('circlesOrigin')] = sender.floatValue()
		self.update()

	@objc.IBAction
	def setCirclesRadius_( self, sender):
		Glyphs.defaults[self.domain('circlesRadius')] = sender.floatValue()
		self.update()

	@objc.IBAction
	def setCirclesStart_( self, sender):
		Glyphs.defaults[self.domain('circlesStart')] = sender.floatValue()
		self.update()

	@objc.IBAction
	def setCircles_( self, sender):
		Glyphs.defaults[self.domain('circles')] = sender.state()
		self.enableCircleTextFields(bool(sender.state()))
		self.update()

	@objc.IBAction
	def setAShadowColor_( self, sender):
		Glyphs.defaults[self.domain('aShadowColor')] = sender.stringValue()
		print(str(sender.stringValue()))
		self.update()

	@objc.python_method
	def enableCircleTextFields( self, areCheckboxesEnabled ):
		self.circlesOriginTextField.setEnabled_(areCheckboxesEnabled)
		self.circlesRadiusTextField.setEnabled_(areCheckboxesEnabled)
		self.circlesDistanceTextField.setEnabled_(areCheckboxesEnabled)
		self.circlesAngleTextField.setEnabled_(areCheckboxesEnabled)
		self.circlesStartTextField.setEnabled_(areCheckboxesEnabled)
		self.circlesEndTextField.setEnabled_(areCheckboxesEnabled)

	# Actual filter
	@objc.python_method
	def filter(self, layer, inEditView, customParameters):
		layer.removeOverlap()
		#print(str(layer.parent.parent.customParameters['Color Palettes'][0]))
		if len(customParameters) > 0:
			if 'strokeWidth' in customParameters:
				print("strokeWidth " + customParameters['strokeWidth'])
			if 'insetWidth' in customParameters:
				print("insetWidth " + customParameters['insetWidth'])
			if 'hatchAngle' in customParameters:
				print("hatchAngle " + customParameters['hatchAngle'])
			if 'hatchStep' in customParameters:
				print("hatchStep " + customParameters['hatchStep'])
			if 'hatchStartY' in customParameters:
				print("hatchStartY " + customParameters['hatchStartY'])
			if 'hatchStroke' in customParameters:
				print("hatchStroke " + customParameters['hatchStroke'])
			if 'shadowOffset' in customParameters:
				print("shadowOffset " + customParameters['shadowOffset'])
			if 'shadowAngle' in customParameters:
				print("shadowAngle " + customParameters['shadowAngle'])
			if 'hatchOrigin' in customParameters:
				print("hatchOrigin " + customParameters['hatchOrigin'])
			if 'circlesAngle' in customParameters:
				print("circlesAngle " + customParameters['circlesAngle'])
			if 'circlesDistance' in customParameters:
				print("circlesDistance " + customParameters['circlesDistance'])
			if 'circlesEnd' in customParameters:
				print("circlesEnd " + customParameters['circlesEnd'])
			if 'circlesOrigin' in customParameters:
				print("circlesOrigin " + customParameters['circlesOrigin'])
			if 'circlesRadius' in customParameters:
				print("circlesRadius " + customParameters['circlesRadius'])
			if 'circlesStart' in customParameters:
				print("circlesStart " + customParameters['circlesStart'])
			if 'circles' in customParameters:
				print("circles " + customParameters['circles'])
			if 'aShadowColor' in customParameters:
				print("aShadowColor" + customParameters['aShadowColor'])
		else: 
			strokeWidth = float(self.pref('strokeWidth'))
			insetWidth = float(self.pref('insetWidth'))
			hatchAngle = float(self.pref('hatchAngle'))
			hatchStep = float(self.pref('hatchStep'))
			hatchStartY = float(self.pref('hatchStartY'))
			hatchStroke = float(self.pref('hatchStroke'))
			hatchOrigin = float(self.pref('hatchOrigin'))
			shadowOffset = float(self.pref('shadowOffset'))
			shadowAngle = float(self.pref('shadowAngle'))
			circlesAngle = float(self.pref('circlesAngle'))
			circlesDistance = float(self.pref('circlesDistance'))
			circlesEnd = float(self.pref('circlesEnd'))
			circlesOrigin = float(self.pref('circlesOrigin'))
			circlesRadius = float(self.pref('circlesRadius'))
			circlesStart = float(self.pref('circlesStart'))
			aShadowColor = str(self.pref('aShadowColor'))
			circles = bool(self.pref('circles'))

		filterHelper = FilterHelper(outlineStrokeWidth=strokeWidth, insetWidth=insetWidth, thisLayer=layer)
		outlineLayer = filterHelper.createOutlineGlyphCopy(layer)
		insetLayer = filterHelper.createInsetGlyphCopy(layer)
		splitLayers = filterHelper.splitAndHatch(insetLayer, hatchStartY, hatchAngle, 2000, hatchStroke, hatchStep, hatchOrigin)

		circleEffect = CircleEffect()
		circleShapes = []
		if(circles):
			circleLayer = circleEffect.drawCircleColumn(splitLayers[1], circlesOrigin, circlesRadius, circlesDistance, circlesAngle, circlesStart, circlesEnd)
			circleShapes = circleLayer.shapes.values()

		shadowEffect = ShadowEffect(outlineStrokeWidth=strokeWidth)
		shadowBaseLayer = shadowEffect.prepareOutlineForShadow(layer)
		shadowLayer = shadowEffect.applyShadow(shadowBaseLayer, shadowOffset, shadowAngle)

		layer.shapes = outlineLayer.shapes + splitLayers[0].shapes.values() + splitLayers[1].shapes.values() + shadowLayer.shapes.values() + circleShapes
	
	@objc.python_method
	def generateCustomParameter( self ):
		self.registerDefaults()
		return "%s; strokeWidth:%s insetWidth:%s hatchAngle:%s hatchStep:%s hatchStartY:%s hatchStroke:%s shadowOffset:%s shadowAngle:%s hatchOrigin:%s circlesAngle:%s circlesDistance:%s circlesEnd:%s circlesOrigin:%s circlesRadius:%s circlesStart:%s circles:%i, aShadowColor:%s" % (
			self.__class__.__name__,
			self.pref('strokeWidth'),
			self.pref('insetWidth'),
			self.pref('hatchAngle'),
			self.pref('hatchStep'),
			self.pref('hatchStartY'),
			self.pref('hatchStroke'),
			self.pref('shadowOffset'),
			self.pref('shadowAngle'),
			self.pref('hatchOrigin'),
			self.pref('circlesAngle'),
			self.pref('circlesDistance'),
			self.pref('circlesEnd'),
			self.pref('circlesOrigin'),
			self.pref('circlesRadius'),
			self.pref('circlesStart'),
			self.pref('circles'),
			self.pref('aShadowColor')
			)

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
