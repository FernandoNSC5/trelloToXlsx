from openpyxl import load_workbook
from datetime import datetime
import printDataStructure

class XLSX:

	def __init__self(self, prazos, audiencias, acompanhamentos):
		# Basic variables
		self.prazos = prazos
		self.audiencias = audiencias
		self.acompanhamentos = acompanhamentos
		self.max_rows = 100 #Defoult. Maybe change at load_data func
		self.advogados = ["Cabral", "Vitória Tiannamen", "Raul Lobato", "Paulo Toledo"]

		# Variables used to append secion indexes
		self.prazos_rows = list()	#Two indexes (init, end)
		self.audiencias_rows = list()	#Two indexes (init, end)
		self.acompanhamentos_rows = list()	#One index (init)

		#Print structures
		self.print_prazos = printDataStructure.PrintDataStructure(1)
		self.print_audiencias_prazos = printDataStructure.PrintDataStructure(2)
		self.print_acompanhamento_prazos = printDataStructure.PrintDataStructure(3)

		# Elements
		self.load_and_write_data()
	

	def load_and_write_data(self):

		#Types
		plan = list()
		tipo = ["CLIENTE", "ESTUDOS E ACOMPANHAMENTOS", "AUDIÊNCIAS E JULGAMENTOS"]

		wb = load_workbook("src/planilha.xlsx")
		ws = wb.worksheets[0]

		try:
			self.max_rows = ws.max_row
		except:
			print("[XLSX] Impossible to use dynamic rows into file. Using default 100 rows counter")

		for row in ws.iter_rows(min_row=1, max_col=9 , max_row=self.max_rows):
			aux = list()
			for cell in row:
				aux.append(cell.value)
			plan.append(aux)


		# searching for indexes
		# Will be used later in order to define how much lines
		# Each secion will use (Prazos, Audiencias and Acompanhamentos)
		index = 0
		for i in plan:
			index += 1
			for j in i:
				if tipo[0] == str(j).strip():
					self.prazos_rows.append(index+2)
				if tipo[1] == str(j).strip():
					self.prazos_rows.append(index-1)
					self.acompanhamentos_rows.append(index+1)
				if tipo[2] == str(j).strip():
					self.acompanhamentos_rows.append(index-1)
					self.audiencias_rows.append(index+1)

		# Adding to Data structures that will be used later
		# in order to build new xlsx
		index = 0
		for i in plan:
			if index >= self.prazos_rows[0]-1 and index < self.prazos_rows[1]:
				self.add_to_prazos(i)
			elif index >= self.acompanhamentos_rows[0]-1 and index < self.acompanhamentos_rows[1]:
				self.add_to_julgamentos(i)
			elif index >= self.audiencias_rows[0]-1:
				self.add_to_audiencias(i)
			index += 1

		# Sorting data before assingment
		self.prazos.sort()
		self.acompanhamentos.sort()
		self.audiencias.sort()

		# Indexing insto print_data_structure
		# For Prazos
		for user in self.prazos.keys():
			for data in self.prazos[user]:
				if user == self.advogados[0]:
					self.print_prazos.add_to_cabral(data)
				elif user == self.advogados[1]:
					self.print_prazos.add_to_vitoria(data)
				elif user == self.advogados[2]:
					self.print_prazos.add_to_raul(data)
				elif user == self.advogados[3]:
					self.print_prazos.add_to_paulo(data)

		# For Audiencias
		for user in self.audiencias.keys():
			for data in self.audiencias[user]:
				if user == self.advogados[0]:
					self.print_audiencias_prazos.add_to_cabral(data)
				elif user == self.advogados[1]:
					self.print_audiencias_prazos.add_to_vitoria(data)
				elif user == self.advogados[2]:
					self.print_audiencias_prazos.add_to_raul(data)
				elif user == self.advogados[3]:
					self.print_audiencias_prazos.add_to_paulo(data)

		# For Acompanhamentos
		for user in self.acompanhamentos.keys():
			for data in self.acompanhamentos[user]:
				if user == self.advogados[0]:
					self.print_acompanhamento_prazos.add_to_cabral(data)
				elif user == self.advogados[1]:
					self.print_acompanhamento_prazos.add_to_vitoria(data)
				elif user == self.advogados[2]:
					self.print_acompanhamento_prazos.add_to_raul(data)
				elif user == self.advogados[3]:
					self.print_acompanhamento_prazos.add_to_paulo(data)

		# Agrouping at print_data_structe
		self.agroup()

		#Gets structure to be written
		written_prazos = self.print_prazos.get_main_structure()
		written_audiencias = self.print_audiencias_prazos.get_main_structure()
		written_acompanhamentos = self.print_acompanhamento_prazos.get_main_structure()

		written_all = list()
		for i in written_prazos:
			written_all.append(i)
		for i in written_audiencias:
			written_all.append(i)
		for i in written_acompanhamentos:
			written_all.append(i)

		#Creating new sheet in order to append new data
		ws = wb.create_sheet("Planilha atualizada", 0)
		for i in written_all:
			ws.append(i)

		# Escrevendo
		wb.save("src/planilha_updated.xlsx")

	def agroup(self):
		self.print_prazos.set_main_structure()
		self.print_audiencias_prazos.set_main_structure()
		self.print_acompanhamento_prazos.set_main_structure()

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
			data['Prazo Fatal'] = lista[7].strftime("%d/%m/%Y")
		except:
			data['Prazo Fatal'] = None
		try:
			data['Prazo'] = lista[8].strftime("%d/%m/%Y")
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
			data['Prazo Fatal'] = lista[7].strftime("%d/%m/%Y")
		except:
			data['Prazo Fatal'] = None
		try:
			data['Prazo'] = lista[8].strftime("%d/%m/%Y")
		except:
			data['Prazo'] = None
		data['Advogado'] = lista[4]

		self.julgamentos[lista[4]].append(data)
		self.prazos[lista[4]].append(data)

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
			data['Prazo Fatal'] = lista[7].strftime("%d/%m/%Y")
		except:
			data['Prazo Fatal'] = None
		try:
			data['Prazo'] = lista[8].strftime("%d/%m/%Y")
		except:
			data['Prazo'] = None
		data['Advogado'] = lista[4]

		self.audiencias[lista[4]].append(data)
		self.prazos[lista[4]].append(data)	