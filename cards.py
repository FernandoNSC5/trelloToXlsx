class Card:

	def __init__(self):
		self.vitoria = list()
		self.paulo = list()
		self.raul = list()
		self.cabral = list()

	##############################
	##	Addons
	def addVitoria(self, card):
		self.vitoria.append(card)

	def addPaulo(self, card):
		self.paulo.append(card)

	def addRaul(self, card):
		self.raul.append(card)

	def addCabral(self, card):
		self.cabral.append(card)

	##############################
	##	Gets
	def getVitoria(self):
		return self.vitoria

	def getPaulo(self):
		return self.paulo

	def getRaul(self):
		return self.raul

	def getCabral(self):
		return self.cabral

	def getAll(self):
		return [self.vitoria, self.paulo, self.raul, self.cabral]