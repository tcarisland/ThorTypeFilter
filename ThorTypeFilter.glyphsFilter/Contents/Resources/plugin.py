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
from effects import ThorTypeEffects

class ThorTypeFilter(FilterWithDialog):

	prefID= "com.tcarisland.ThorTypeFilter"
	if Glyphs.versionNumber < 3:
		# GLYPHS 2
		pathOperator = NSClassFromString("GSPathOperator").alloc().init() # needs to be initialized only once

	# Definitions of IBOutlets
	# The NSView object from the User Interface. Keep this here!
	dialog = objc.IBOutlet()
	# Text field in dialog
	myTextField = objc.IBOutlet()
	myOtherTextField = objc.IBOutlet()

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
		self.myTextField.setStringValue_(self.pref('strokeWidth'))
		self.myOtherTextField.setStringValue_(self.pref('insetWidth'))
		# Set focus to text field
		self.myTextField.becomeFirstResponder()
		self.update()

	@objc.python_method
	def registerDefaults(self, sender=None):
		Glyphs.registerDefault(self.domain('strokeWidth'), 10.0)
		Glyphs.registerDefault(self.domain('insetWidth'), 30.0)

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
	def setHatchStep( self, sender):
		Glyphs.defaults[self.domain('hatchStep')] = sender.floatValue()
		self.update()

	@objc.IBAction
	def setHatchStartY( self, sender):
		Glyphs.defaults[self.domain('hatchStartY')] = sender.floatValue()
		self.update()

	@objc.IBAction
	def setHatchStroke( self, sender):
		Glyphs.defaults[self.domain('hatchStroke')] = sender.floatValue()
		self.update()

	# Actual filter
	@objc.python_method
	def filter(self, layer, inEditView, customParameters):
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
		else: 
			strokeWidth = float(self.pref('strokeWidth'))
			insetWidth = float(self.pref('insetWidth'))
			strokeWidth = float(self.pref('hatchAngle'))
			insetWidth = float(self.pref('hatchStep'))
			strokeWidth = float(self.pref('hatchStartY'))
			insetWidth = float(self.pref('hatchStroke'))
		filterHelper = FilterHelper(outlineStrokeWidth=strokeWidth, insetWidth=insetWidth, thisLayer=layer)
		outlineLayer = filterHelper.createOutlineGlyphCopy(layer)
		insetLayer = filterHelper.createInsetGlyphCopy(layer)
		splitLayer = filterHelper.splitAndHatch(insetLayer, 189, 45, 500)

		shadowEffect = ShadowEffect(outlineStrokeWidth=strokeWidth)
		shadowBaseLayer = shadowEffect.prepareOutlineForShadow(layer)

		layer.shapes = outlineLayer.shapes + splitLayer.shapes + shadowEffect.filter(shadowBaseLayer)
	
	@objc.python_method
	def generateCustomParameter( self ):
		self.registerDefaults()
		return "%s; strokeWidth:%s insetWidth:%s" % (
			self.__class__.__name__,
			self.pref('strokeWidth'),
			self.pref('insetWidth'),
			self.pref('hatchAngle'),
			self.pref('hatchStep'),
			self.pref('hatchStartY'),
			self.pref('hatchStroke'),
			)

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
