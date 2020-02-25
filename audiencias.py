class Audiencias:

	def __init__(self):
		self.vitoria = list()
		self.raul = list()
		self.paulo = list()
		self.cabral = list()

	##########################
	##	Addons
	def addVitoria(self, card):
		self.vitoria.append(card)

	def addRaul(self, card):
		self.raul.append(card)

	def addPaulo(self, card):
		self.paulo.append(card)

	def addCabral(self, card):
		self.cabral.append(card)

	##########################
	##	Getters
	def getVitoria(self):
		return self.vitoria

	def getRaul(self):
		return self.Raul

	def getPaulo(self):
		return self.Paulo

	def getCabral(self):
		return self.cabral