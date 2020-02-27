class Data:

	def __init__(self):
		self.buffer = list()
		self.load_data()
		self.clean_buffer()

	######################################################################
	##	METHODS
	def load_data(self):
		f = open('structure/dados.txt', 'r')
		for i in range(7):
			self.buffer.append(str(f.readline()))

	def clean_buffer(self):
		for i in range(len(self.buffer)-1):
			self.buffer[i] = self.buffer[i].replace(self.buffer[i][-1], "")
			
	#######################################################################
	##	GETTERS AND SETTERS
	def get_api_key(self):
		return self.buffer[0]

	def get_api_secret(self):
		return self.buffer[1]

	def get_token(self):
		return self.buffer[2]

	def get_board_name(self):
		return self.buffer[3]

	def get_list_feito(self):
		return self.buffer[4]

	def get_list_estudos_e_acompanhamentos(self):
		return self.buffer[5]

	def get_list_audiencias_e_julgamentos(self):
		return self.buffer[6]

	def get_list_cabral(self):
		return self.buffer[7]

	def get_list_paulo(self):
		return self.buffer[8]

	def get_list_raul(self):
		return self.buffer[9]

	def get_list_vitoria(self):
		return self.buffer[10]

	def get_list_fazendo(self):
		return self.buffer[11]

d = Data()