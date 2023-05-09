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
from GlyphsApp import *
from GlyphsApp.plugins import *
from Foundation import NSClassFromString
from filterutils import FilterHelper

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

	# Actual filter
	@objc.python_method
	def filter(self, layer, inEditView, customParameters):
		#print("ThorType Filter apply clicked - inEditView - " + str(inEditView))
		if len(customParameters) > 0:
			if 'strokeWidth' in customParameters:
				print("FIRST VALUE " + customParameters['strokeWidth'])
			if 'insetWidth' in customParameters:
				print("SECOND VALUE" + customParameters['insetWidth'])
		else: 
			strokeWidth = float(self.pref('strokeWidth'))
			insetWidth = float(self.pref('insetWidth'))
		filterHelper = FilterHelper(outlineStrokeWidth=strokeWidth, insetWidth=insetWidth, thisLayer=layer)
		filterHelper.runFilter()
	
	@objc.python_method
	def generateCustomParameter( self ):
		self.registerDefaults()
		return "%s; strokeWidth:%s insetWidth:%s" % (
			self.__class__.__name__,
			self.pref('strokeWidth'),
			self.pref('insetWidth'),
			)

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
