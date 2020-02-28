class PrintDataStructure:

		def __init__(self):

			# Order as set in set_main_structure()
			self.main_structure = list()

			self.vitoria = list()
			self.paulo = list()
			self.raul = list()
			self.cabral = list()

		def set_main_structure(self):

			for i in self.vitoria:
				self.main_structure.append(i)

			for i in self.paulo:
				self.main_structure.append(i)

			for i in self.raul:
				self.main_structure.append(i)

			for i in self.cabral:
				self.main_structure.append(i)

		def add_to_vitoria(self, data):
			data = self.convert(data)
			self.vitoria.append(data)

		def add_to_paulo(self, data):
			data = self.convert(data)
			self.paulo.append(data)

		def add_to_raul(self, data):
			data = self.convert(data)
			self.raul.convert(data)

		def add_to_cabral(self, data):
			data = self.convert(data):

		def get_vitoria(self):
			return self.vitoria

		def get_cabral(self):
			return self.cabral

		def get_raul(self):
			return self.raul

		def get_paulo(self):
			return self.paulo