class PrintDataStructure:

	def __init__(self, flag_initial):
		# Order as set in set_main_structure()
		self.main_structure = list()

		#If first data to xlsx, adds cabeçalho
		#flag 1 -> Prazos
		#flag 2 -> Audiencias
		#flag 3 -> Acompanhamentos
		if flag_initial == 1:
			self.main_structure.append(["", "", "", "", "", "", "", ""])
			self.main_structure.append(["", "PRAZOS", "", "", "", "", "", ""])
			self.main_structure.append(["", "", "CLIENTE", "PROCESSO", "RESPONSÁVEL", "TAREFA", "OBSERVAÇÕES", "PRAZO FATAL", "PRAZO"])
		elif flag_initial == 2:
			self.main_structure.append(["", "Audiências e Julgamentos", "", "", "", "", "", "", ""])
		elif flag_initial == 3:
			self.main_structure.append(["", "Estudos e Acompanhamentos", "", "", "", "", "", ""])

		#Peoble hard coded (for now) structures
		self.vitoria = list()
		self.paulo = list()
		self.raul = list()
		self.cabral = list()

		#People hard coded(for now) first data flag
		#0 -> vitoria
		#1 -> cabral
		#2 -> raul
		#3 -> paulo
		self.flags = [1, 1, 1, 1]

	#######################################
	## Methods
	def set_main_structure(self):
		# CREATE ORDENATION HERE
		for i in self.vitoria:
			self.main_structure.append(i)

		for i in self.paulo:
			self.main_structure.append(i)

		for i in self.raul:
			self.main_structure.append(i)

		for i in self.cabral:
			self.main_structure.append(i)

	def convert(self, data, flag_index):
		#none
		#none, PRAZOS, none, none, none, none, none, none, none, none
		#none, ENTRADA, cliente, processo, responsável, tarefa, observações, prazo fatal, prazo
		#----,-----,--------,---------,------------,-------,------------,--------,------------,-------
		#none, Estudos e Acompanhamentos, none, none, none, none, none, none
		#----,-----,--------,---------,------------,-------,------------,--------,------------,-------
		#none, Audiência e Julgamentos, none, none, none, none, none, none
		#----,-----,--------,---------,------------,-------,------------,--------,------------,-------

		appender = list()
		ll = list()

		#Appending user name to first row
		if self.flags[flag_index]:
			appender.append("")
			appender.append("")
			appender.append("")
			appender.append("")
			appender.append(data['Advogado'])
			appender.append("")
			appender.append("")
			appender.append("")
			ll.append(appender)
			appender = list()
			self.flags[flag_index] = 0

		appender.append("")
		appender.append(data['Criado em'])
		appender.append(data['Cliente'])
		appender.append(data['processo'])
		appender.append(data['Advogado'])
		appender.append(data['Tarefa'])
		appender.append(data['descricao'])	#Observações
		appender.append(data['Prazo Fatal'])
		appender.append(data['Prazo'])
		ll.append(appender)

		return ll

	#######################################
	##	Gets and setters
	def add_to_vitoria(self, data): 
		data = self.convert(data, 0)
		self.vitoria.append(data[0])
		if len(data) > 1:
			self.vitoria.append(data[1])

	def add_to_cabral(self, data):
		data = self.convert(data, 1)
		self.cabral.append(data[0])
		if len(data) > 1:
			self.cabral.append(data[1])

	def add_to_raul(self, data):
		data = self.convert(data, 2)
		self.raul.append(data[0])
		if len(data) > 1:
			self.raul.append(data[1])

	def add_to_paulo(self, data):
		data = self.convert(data, 3)
		self.paulo.append(data[0])
		if len(data) > 1:
			self.paulo.append(data[1])

	def get_vitoria(self):
		return self.vitoria

	def get_cabral(self):
		return self.cabral

	def get_raul(self):
		return self.raul

	def get_paulo(self):
		return self.paulo

	def get_main_structure(self):
		return self.main_structure