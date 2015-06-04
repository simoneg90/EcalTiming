class Crystal:
	def __init__(self, x, y, det, calib, error):
		self.det = det
		if det == 0:
			self.ieta = x
			self.iphi = y
			self.ix = None
			self.iy = None
		else:
			self.ix = x
			self.iy = y
			self.ieta = None
			self.iphi = None
		self.calib = calib
		self.error = error

	def xmlConstant(self):
		if self.det == 0:
			s = '\t<cell iEta="%d" iPhi="%d">\n' % (self.ieta, self.iphi)
		else:
			s = '\t<cell ix="%d" iy="%d" zside="%d">\n' % (self.ix, self.iy, self.det)
		s += '\t\t<Value>%.6f</Value>\n' % self.calib
		s += '\t</cell>\n\n'
		return s

	def xmlError(self):
		if self.det == 0:
			s = '\t<cell iEta="%d" iPhi="%d">\n' % (self.ieta, self.iphi)
		else:
			s = '\t<cell ix="%d" iy="%d" zside="%d">\n' % (self.ix, self.iy, self.det)
		s += '\t\t<Value>%.6f</Value>\n' % self.error
		s += '\t</cell>\n\n'
		return s
	
	def __lt__(self, other):
		if self.det != other.det:
			if self.det == 0:
				return True
			elif other.det == 0:
				return False
			else:
				return self.det < other.det
		elif self.det == 0:
			if self.ieta == other.ieta:
				return self.iphi < other.iphi
			else:
				return self.ieta < other.ieta
		else:
			if self.iy == other.iy:
				return self.ix < other.ix
			else:
				return self.iy < other.iy

	def __repr__(self):
		if self.det == 0:
			return "Crystal(%d, %d, %d, %f, %f)"%(self.ieta,self.iphi,self.det,self.calib,self.error)
		else:
			return "Crystal(%d, %d, %d, %f, %f)"%(self.ix,self.iy,self.det,self.calib,self.error)

class CalibrationXML:
	def __init__(self):
		self.crystals = []
	def addCrystal(self,x, y, det, calib, error):
		self.crystals.append(Crystal(x,y,det,calib,error))
	def XMLHeader(self):
		s  = "\n<EcalFloatCondObjectContainer>\n\n"
		s += "\t<EcalCondHeader>\n"
		s += "\t\t<method>testmethod</method>\n"
		s += "\t\t<version>testversion</version>\n"
		s += "\t\t<datasource>testdata</datasource>\n"
		s += "\t\t<since>123</since>\n"
		s += "\t\t<tag>testtag</tag>\n"
		s += "\t\t<date>Mar 24 1973</date>\n"
		s += "\t</EcalCondHeader>\n\n"
		return s
	def XMLFooter(self):
		return "\n</EcalFloatCondObjectContainer>\n"
	def sort(self):
		self.crystals.sort()

	def writeConstant(self,filename):
		with open(filename,"w") as f:
			f.write(self.XMLHeader())
			for c in self.crystals:
				f.write(c.xmlConstant())
			f.write(self.XMLFooter())

	def writeErrors(self,filename):
		with open(filename,"w") as f:
			f.write(self.XMLHeader())
			for c in self.crystals:
				f.write(c.xmlError())
			f.write(self.XMLFooter())

