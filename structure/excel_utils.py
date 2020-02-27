from openpyxl import load_workbook
from datetime import datetime

class XLSX:

	def __init__(self, prazos, julgamentos, audiencias, users):
		self.prazos = prazos
		self.julgamentos = julgamentos
		self.audiencias = audiencias
		self.users = users
		
		#Data
		self.max_rows = 100
		self.prazo_rows = []
		self.estudos_acompanhamentos = []
		self.audiencias_julgamentos = []

		#Debug
		self.load_data()

	def load_data(self):
		plan = list()

		tipo = ['CLIENTE', 'ESTUDOS E ACOMPANHAMENTOS', 'AUDIÊNCIAS E JULGAMENTOS']

		wb = load_workbook("src/planilha.xlsx")
		ws = wb.worksheets[0]

		for row in ws.iter_rows(min_row=1, max_col=10 , max_row=self.max_rows):
			aux = list()
			for cell in row:
				aux.append(cell.value)
			plan.append(aux)

		# searching for indexes
		index = 0
		for i in plan:
			index += 1
			for j in i:
				if tipo[0] == str(j).strip():
					self.prazo_rows.append(index+1)
				if tipo[1] == str(j).strip():
					self.prazo_rows.append(index-1)
					self.estudos_acompanhamentos.append(index+1)
				if tipo[2] == str(j).strip():
					self.estudos_acompanhamentos.append(index-1)
					self.audiencias_julgamentos.append(index+1)

		print(self.prazo_rows)
		print(self.estudos_acompanhamentos)
		print(self.audiencias_julgamentos)

		#Adding to Data structures
		index = 0
		for i in plan:
			if index >= self.prazo_rows[0]-1 and index < self.prazo_rows[1]:
				self.add_to_prazos(i)
			elif index >= self.estudos_acompanhamentos[0]-1 and index < self.estudos_acompanhamentos[1]:
				self.add_to_julgamentos(i)
			elif index >= self.audiencias_julgamentos[0]-1:
				self.add_to_audiencias(i)
			index += 1

		

		#wb.save("src/planilha.xlsx")

	#########################################
	##	Appends
	def add_to_prazos(self, lista):
		if lista[4] == None:
			return

		#Dict Structure
		data = {
			"processo":None,
			"descricao":None,
			"Tarefa":None,
			"Cliente":None,
			"Criado em":None,
			"Prazo Fatal":None,
			"Prazo":None,
			"Realizado em":None,
			"Advogado":None
		}

		data['processo'] = lista[3]
		data['descricao'] = lista[6]
		data['Tarefa'] = lista[5]
		data['Cliente'] = lista[2]
		try:
			data['Criado em'] = lista[1].strftime("%d/%m/%Y")
		except:
			data['Criado em'] = None
		try:
			data['Prazo Fatal'] = lista[8].strftime("%d/%m/%Y")
		except:
			data['Prazo Fatal'] = None
		try:
			data['Prazo'] = lista[9].strftime("%d/%m/%Y")
		except:
			data['Prazo'] = None
		data['Advogado'] = lista[4]

		self.prazos[lista[4]].append(data)

	def add_to_julgamentos(self, lista):
		if lista[4] == None:
			return

		#Dict Structure
		data = {
			"processo":None,
			"descricao":None,
			"Tarefa":None,
			"Cliente":None,
			"Criado em":None,
			"Prazo Fatal":None,
			"Prazo":None,
			"Realizado em":None,
			"Advogado":None
		}

		data['processo'] = lista[3]
		data['descricao'] = lista[6]
		data['Tarefa'] = lista[5]
		data['Cliente'] = lista[2]
		try:
			data['Criado em'] = lista[1].strftime("%d/%m/%Y")
		except:
			data['Criado em'] = None
		try:
			data['Prazo Fatal'] = lista[8].strftime("%d/%m/%Y")
		except:
			data['Prazo Fatal'] = None
		try:
			data['Prazo'] = lista[9].strftime("%d/%m/%Y")
		except:
			data['Prazo'] = None
		data['Advogado'] = lista[4]

		self.julgamentos[lista[4]].append(data)

	def add_to_audiencias(self, lista):
		if lista[4] == None:
			return

		#Dict Structure
		data = {
			"processo":None,
			"descricao":None,
			"Tarefa":None,
			"Cliente":None,
			"Criado em":None,
			"Prazo Fatal":None,
			"Prazo":None,
			"Realizado em":None,
			"Advogado":None
		}

		data['processo'] = lista[3]
		data['descricao'] = lista[6]
		data['Tarefa'] = lista[5]
		data['Cliente'] = lista[2]
		try:
			data['Criado em'] = lista[1].strftime("%d/%m/%Y")
		except:
			data['Criado em'] = None
		try:
			data['Prazo Fatal'] = lista[8].strftime("%d/%m/%Y")
		except:
			data['Prazo Fatal'] = None
		try:
			data['Prazo'] = lista[9].strftime("%d/%m/%Y")
		except:
			data['Prazo'] = None
		data['Advogado'] = lista[4]

		self.audiencias[lista[4]].append(data)	