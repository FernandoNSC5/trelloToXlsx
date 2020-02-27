from trello import TrelloClient, Member
import threading
import sys
sys.path.append("structure/")

import data as dt
import cards
import acompanhamentos
import audiencias
import excel_utils

class TrelloProcess:

	def __init__(self):
		#############################
		##	Setting variables
		self.data = dt.Data()
		self.CABRAL_BOARD = None
		self.USERS = list()

		##############################
		##	Starting
		self.connection()
		self.get_board()
		self.get_board_users()
		self.structure_classes()
		self.get_lists()
		self.process_data()

		# Debugger		
		'''
		print("--FROM TP---")
		print(self.CARDS.getDict())
		print(self.AUDIENCIAS)
		print(self.ESTUDOS_E_ACOMPANHAMENTOS)
		print("--END TP--")'''
		self.write_xlsx(self.CARDS.getDict(), self.AUDIENCIAS.getDict(), self.ACOMPANHAMENTOS.getDict(), self.USERS)

	###################################
	##	METHODS						  #
	###################################
	# Trello service connection
	def connection(self):
		try:
			self.client = TrelloClient(
			    api_key= self.data.get_api_key(),
			    api_secret= self.data.get_api_secret(),
			    token= self.data.get_token(),
			)
			print("[TRELLO] Connection stabilished")
		except:
			print("[TRELLO] An error ocurred while parsing api key")
			return

	#Searching for board
	def get_board(self):
		try:
			all_boards = self.client.list_boards()
			self.BOARD = None
			for i in all_boards:
				if i.name == self.data.get_board_name():
					self.BOARD = i
					break
			print("[TRELLO] Board found")
		except:
			print("[TRELLO] An error ocurred while trying to retrieve board")
			print("[TRELLO] Known boards:")
			for i in all_boards:
				print("\t"+str(i))
			return

	# Searching for lists into board
	def get_lists(self):
		self.get_list_feito()
		self.get_list_acompanhamentos()
		self.get_list_julgamentos()

	def process_data(self):
		self.process_feito_list()
		self.process_acompanhamento_list()
		self.process_julgamento_list()

	# Searching for board users
	def get_board_users(self):
		try:
			members = self.BOARD.all_members()
			for member in members:
				self.USERS.append(member.fetch().full_name)
		except:
			print("[TRELLO] An error ocurred while searching for users")
			return

	# Creating data structure classes
	def structure_classes(self):
		self.CARDS = cards.Card(self.USERS)
		self.ACOMPANHAMENTOS = acompanhamentos.Acompanhamentos(self.USERS)
		self.AUDIENCIAS = audiencias.Audiencias(self.USERS)

	# Process data retrieved from trello FINALIZADO list
	def process_feito_list(self):
		for card in self.DONE_LIST.list_cards():
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

			#Processing Dict
			data["processo"] = card.name #card name -> processo
			data["descricao"] = card.description #Description

			#Setting up custom fields
			for customField in card.customFields:
				data[customField.name] = customField.value

			#Setting up name
			try:
				user_id = card.member_id[0]
				user_id = Member(self.client, user_id)
				data["Advogado"] = user_id.fetch().full_name
			except:
				print("Advogado não atrelado ao card")
				continue

			#Dates
			data["Realizado em"] = self.clean_date(data["Realizado em"])
			data["Criado em"] = self.clean_date(data["Criado em"])
			data["Prazo Fatal"] = self.clean_date(data["Prazo Fatal"])
			data["Prazo"] = self.clean_date(data["Prazo"])

			self.CARDS.addCard(data['Advogado'], data)

	# Process data retrieved from trello ACOMPANHAMENTO list
	def process_acompanhamento_list(self):
		try:
			for card in self.ESTUDOS_E_ACOMPANHAMENTOS.list_cards():
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

				#Processing Dict
				data["processo"] = card.name #card name -> processo
				data["descricao"] = card.description #Description

				#Setting up custom fields
				for customField in card.customFields:
					data[customField.name] = customField.value

				#Setting up name
				try:
					user_id = card.member_id[0]
					user_id = Member(self.client, user_id)
					data["Advogado"] = user_id.fetch().full_name
				except:
					print("Advogado não atrelado ao card")
					continue

				#Dates
				data["Realizado em"] = self.clean_date(data["Realizado em"])
				data["Criado em"] = self.clean_date(data["Criado em"])
				data["Prazo Fatal"] = self.clean_date(data["Prazo Fatal"])
				data["Prazo"] = self.clean_date(data["Prazo"])

				self.ACOMPANHAMENTOS.addCard(data['Advogado'], data)
		except:
			print("[FAILURE] process_acompanhamento_list")

	# Process data retrieved from trello JULGAMENTO list
	def process_julgamento_list(self):
		try:
			for card in self.AUDIENCIAS_E_JULGAMENTOS.list_cards():
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

				#Processing Dict
				data["processo"] = card.name #card name -> processo
				data["descricao"] = card.description #Description

				#Setting up custom fields
				for customField in card.customFields:
					data[customField.name] = customField.value

				#Setting up name
				try:
					user_id = card.member_id[0]
					user_id = Member(self.client, user_id)
					data["Advogado"] = user_id.fetch().full_name
				except:
					print("Advogado não atrelado ao card")
					continue

				#Dates
				data["Realizado em"] = self.clean_date(data["Realizado em"])
				data["Criado em"] = self.clean_date(data["Criado em"])
				data["Prazo Fatal"] = self.clean_date(data["Prazo Fatal"])
				data["Prazo"] = self.clean_date(data["Prazo"])

				self.AUDIENCIAS.addCard(data['Advogado'], data)
		except:
			print("[FAILURE] process_julgamento_list")

	def clean_date(self, date_str):
		if date_str == None:
			return None
		new_date = date_str[0:10].split("-")
		return new_date[2]+"/"+new_date[1]+"/"+new_date[0]

	def write_xlsx(self, prazo, julgamento, audiencia, usuario):
		xlsx = excel_utils.XLSX(prazo, julgamento, audiencia, usuario)

	######################################################################
	###	CREATING LISTS

	# Searching for list 'feito'
	def get_list_feito(self):
		try:
			self.DONE_LIST = None
			for i in self.BOARD.list_lists():
				if i.name == self.data.get_list_feito():
					self.DONE_LIST = i
					break
			print("[TRELLO] List "+ self.DONE_LIST.name +" Found")
		except:
			print("[TRELLO] An error ocurred while trying to get board 'Finalizado'")
			return

	# Searching for list Estudos e Acompanhamentos
	def get_list_acompanhamentos(self):
		try:
			self.ESTUDOS_E_ACOMPANHAMENTOS = None
			for i in self.BOARD.list_lists():
				if i.name == self.data.get_list_estudos_e_acompanhamentos():
					self.ESTUDOS_E_ACOMPANHAMENTOS = i
					break
			print("[TRELLO] List "+ self.ESTUDOS_E_ACOMPANHAMENTOS.name +" Found")
		except:
			print("[TRELLO] An error occurred while trying to get board")
			return

	# Searching for list Audiências e Julgamentos
	def get_list_julgamentos(self):
		try:
			self.AUDIENCIAS_E_JULGAMENTOS = None
			for i in self.BOARD.list_lists():
				if i.name == self.data.get_list_audiencias_e_julgamentos():
					self.AUDIENCIAS_E_JULGAMENTOS = i
					break
			print("[TRELLO] List "+ self.AUDIENCIAS_E_JULGAMENTOS.name +" Found")
		except:
			print("[TRELLO] An error ocurred while trying to get board")
			return


t = TrelloProcess()