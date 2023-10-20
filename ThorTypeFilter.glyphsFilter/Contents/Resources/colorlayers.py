palettes = [3, 1, 2, 0, 4, 1]
#masterID = Font.masters[0].id

def addColorLayers(glyph, palettes, masterID):
	for c in palettes:
		# noinspection PyUnresolvedReferences
		layer = GSLayer()
		layer.associatedMasterId = masterID
		layer.attributes['colorPalette'] = c
		glyph.layers.append(layer)
