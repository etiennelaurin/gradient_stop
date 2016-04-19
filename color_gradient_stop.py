debug = False

import inkex
import sys
import copy
import simplestyle

class GradientStop(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)
		self.OptionParser.add_option("-s", "--stop",
						action="store", type="float",
						dest="stop", default=38.2,
						help="Gradient stop")
	def getID(self, first):
		docIdNodes = self.document.xpath('//@id',namespaces=inkex.NSS)
		for m in range(1, 9999):
			if not first + str(m) in docIdNodes:
				return first + str(m)
	def effect(self):
		defs = self.xpathSingle('/svg:svg//svg:defs')
		if defs == None:
			defs = inkex.etree.SubElement(self.document.getroot(),inkex.addNS('defs','svg'))
		for id in self.options.ids:
			current = self.xpathSingle('//svg:*[@id="' + id + '"]')
			curStyle = simplestyle.parseStyle(current.get('style'))
			curFill = curStyle["fill"]
			if curFill[:3] == 'url':
				curGradient = self.xpathSingle('//svg:*[@id="' + curFill[5:-1] + '"]')
				sourceGradientId = self.xpathSingle('//svg:*[@id="' + curFill[5:-1] + '"]/@xlink:href')
				sourceGradient = self.xpathSingle('//svg:*[@id="' + sourceGradientId[1:] + '"]')
				stops = sourceGradient.xpath('//svg:*[@id="' + sourceGradientId[1:] + '"]/svg:stop',namespaces=inkex.NSS)
				if len(stops) != 2:
					exit()
				newGradient = copy.deepcopy(curGradient)
				newSourceGradient = copy.deepcopy(sourceGradient)
				newStop0 = copy.deepcopy(stops[0])
				newStop1 = copy.deepcopy(stops[1])
				newStop0.set('offset', "{0:.2f}".format((self.options.stop / 100) - 0.01))
				newStop1.set('offset', "{0:.2f}".format(self.options.stop / 100))
				newSourceGradient.append(newStop0)
				newSourceGradient.append(newStop1)
				newStops = newSourceGradient.xpath('//svg:*[@id="' + newSourceGradient.get('id') + '"]/svg:stop',namespaces=inkex.NSS)
				data = []
				for elem in newStops:
					key = float(elem.get("offset"))
					data.append((key, elem))
					data.sort()
				newStops[:] = [item[-1] for item in data]
				newSourceGradient.clear()
				for elem in newStops:
					newSourceGradient.append(elem)
				newId = str(e.getID(newSourceGradient.tag.split('}', 1)[1]))
				newSourceGradient.set('id', newId)
				defs.append(newSourceGradient)
				newGradient.set(inkex.addNS('href','xlink'), '#' + newSourceGradient.get('id'))
				newId = str(e.getID(newSourceGradient.tag.split('}', 1)[1]))
				newGradient.set('id', newId)
				defs.append(newGradient)
				curStyle["fill"] = 'url(#' + newId + ')'
				current.set('style',simplestyle.formatStyle(curStyle))
				
	
if __name__ == '__main__':
        e = GradientStop()
        e.affect()
