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
		##	LISTS
		self.DONE_LIST = None
		self.FAZENDO_LIST = None
		self.CABRAL_LIST = None
		self.VITORIA_LIST = None
		self.PAULO_LIST = None
		self.RAUL_LIST = None
		self.AUDIENCIAS_E_JULGAMENTOS_LIST = None
		self.ESTUDOS_E_ACOMPANHAMENTOS_LIST = None

		##############################
		##	Starting
		self.connection()
		self.get_board()
		self.get_board_users()
		self.CARDS = cards.Card(self.USERS)
		self.get_lists()
		self.process_data()

		print(self.USERS)
		#self.write_xlsx(self.CARDS.getDict(), self.AUDIENCIAS.getDict(), self.ACOMPANHAMENTOS.getDict(), self.USERS)

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
			print("[SYSTEM] Connection stabilished")
		except:
			print("[SYSTEM] An error ocurred while parsing api key")
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
			print("[SYSTEM] Board found")
		except:
			print("[SYSTEM] An error ocurred while trying to retrieve board")
			print("[SYSTEM] Known boards:")
			for i in all_boards:
				print("\t"+str(i))
			return

	# Searching for lists into board
	def get_lists(self):
		self.get_list_feito()
		self.get_list_acompanhamentos()
		self.get_list_julgamentos()
		self.get_list_cabral()
		self.get_list_paulo()
		self.get_list_raul()
		self.get_list_vitoria()
		self.get_list_fazendo()

	def process_data(self):
		print("[SYSTEM] Processing data recived", end=".")
		sys.stdout.flush()
		self.process_fazendo_list()
		print("", end=".")
		sys.stdout.flush()
		self.process_acompanhamento_list()
		print("", end=".")
		sys.stdout.flush()
		self.process_julgamento_list()
		print("", end=".")
		sys.stdout.flush()
		self.process_cabral_list()
		print("", end=".")
		sys.stdout.flush()
		self.process_paulo_list()
		print("", end=".")
		sys.stdout.flush()
		self.process_raul_list()
		print("", end=".")
		sys.stdout.flush()
		self.process_vitoria_list()
		print(" finished")
		sys.stdout.flush()

	# Searching for board users
	def get_board_users(self):
		try:
			members = self.BOARD.all_members()
			for member in members:
				self.USERS.append(member.fetch().full_name)
		except:
			print("[SYSTEM] An error ocurred while searching for users")
			return

	# Process data retrieved from trello ACOMPANHAMENTO list
	def process_acompanhamento_list(self):
		try:
			for card in self.ESTUDOS_E_ACOMPANHAMENTOS_LIST.list_cards():
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
		except:
			print("[FAILURE] process_acompanhamento_list " + card.name)

	# Process data retrieved from trello JULGAMENTO list
	def process_julgamento_list(self):
		try:
			for card in self.AUDIENCIAS_E_JULGAMENTOS_LIST.list_cards():
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
					print("Advogado não atrelado ao card " + card.name)
					continue

				#Dates
				data["Realizado em"] = self.clean_date(data["Realizado em"])
				data["Criado em"] = self.clean_date(data["Criado em"])
				data["Prazo Fatal"] = self.clean_date(data["Prazo Fatal"])
				data["Prazo"] = self.clean_date(data["Prazo"])

				self.CARDS.addCard(data['Advogado'], data)
		except:
			print("[FAILURE] process_julgamento_list")

	# Process data retrieved from trello fazendo list
	def process_fazendo_list(self):
		for card in self.FAZENDO_LIST.list_cards():
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
				print("Advogado não atrelado ao card " + card.name)
				continue

			#Dates
			data["Realizado em"] = self.clean_date(data["Realizado em"])
			data["Criado em"] = self.clean_date(data["Criado em"])
			data["Prazo Fatal"] = self.clean_date(data["Prazo Fatal"])
			data["Prazo"] = self.clean_date(data["Prazo"])

			self.CARDS.addCard(data['Advogado'], data)

	# Process data retrieved from trello CABRAL list
	def process_cabral_list(self):
		for card in self.CABRAL_LIST.list_cards():
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
				print("Advogado não atrelado ao card " + card.name)
				continue

			#Dates
			data["Realizado em"] = self.clean_date(data["Realizado em"])
			data["Criado em"] = self.clean_date(data["Criado em"])
			data["Prazo Fatal"] = self.clean_date(data["Prazo Fatal"])
			data["Prazo"] = self.clean_date(data["Prazo"])

			self.CARDS.addCard(data['Advogado'], data)

	# Process data retrieved from trello PAULO list
	def process_paulo_list(self):
		for card in self.PAULO_LIST.list_cards():
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
				print("Advogado não atrelado ao card " + card.name)
				continue

			#Dates
			data["Realizado em"] = self.clean_date(data["Realizado em"])
			data["Criado em"] = self.clean_date(data["Criado em"])
			data["Prazo Fatal"] = self.clean_date(data["Prazo Fatal"])
			data["Prazo"] = self.clean_date(data["Prazo"])

			self.CARDS.addCard(data['Advogado'], data)

	# Process data retrieved from trello RAUL list
	def process_raul_list(self):
		for card in self.RAUL_LIST.list_cards():
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
				print("Advogado não atrelado ao card " + card.name)
				continue

			#Dates
			data["Realizado em"] = self.clean_date(data["Realizado em"])
			data["Criado em"] = self.clean_date(data["Criado em"])
			data["Prazo Fatal"] = self.clean_date(data["Prazo Fatal"])
			data["Prazo"] = self.clean_date(data["Prazo"])

			self.CARDS.addCard(data['Advogado'], data)

	# Process data retrieved from trello VITORIA list
	def process_vitoria_list(self):
		for card in self.VITORIA_LIST.list_cards():
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
				print("Advogado não atrelado ao card " + card.name)
				continue

			#Dates
			data["Realizado em"] = self.clean_date(data["Realizado em"])
			data["Criado em"] = self.clean_date(data["Criado em"])
			data["Prazo Fatal"] = self.clean_date(data["Prazo Fatal"])
			data["Prazo"] = self.clean_date(data["Prazo"])

			self.CARDS.addCard(data['Advogado'], data)

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
			for i in self.BOARD.list_lists():
				if i.name == self.data.get_list_feito():
					self.DONE_LIST = i
					break
			print("[SYSTEM] List "+ self.DONE_LIST.name +" Found")
		except:
			print("[SYSTEM] An error ocurred while trying to get board 'Finalizado'")
			return

	# Searching for list Estudos e Acompanhamentos
	def get_list_acompanhamentos(self):
		try:
			for i in self.BOARD.list_lists():
				if i.name == self.data.get_list_estudos_e_acompanhamentos():
					self.ESTUDOS_E_ACOMPANHAMENTOS_LIST = i
					break
			print("[SYSTEM] List "+ self.ESTUDOS_E_ACOMPANHAMENTOS_LIST.name +" Found")
		except:
			print("[SYSTEM] An error occurred while trying to get board")
			return

	# Searching for list Audiências e Julgamentos
	def get_list_julgamentos(self):
		try:
			for i in self.BOARD.list_lists():
				if i.name == self.data.get_list_audiencias_e_julgamentos():
					self.AUDIENCIAS_E_JULGAMENTOS_LIST = i
					break
			print("[SYSTEM] List "+ self.AUDIENCIAS_E_JULGAMENTOS_LIST.name +" Found")
		except:
			print("[SYSTEM] An error ocurred while trying to get board")
			return

	# Searching for list cabral
	def get_list_cabral(self):
		try:
			for i in self.BOARD.list_lists():
				if i.name == self.data.get_list_cabral():
					self.CABRAL_LIST = i
					break 
			print("[SYSTEM] List " + self.CABRAL_LIST.name + " Found")
		except:
			print("[SYSTEM] An error ocurred while trying to get board")
			return

	# Searching for list paulo
	def get_list_paulo(self):
		try:
			for i in self.BOARD.list_lists():
				if i.name == self.data.get_list_paulo():
					self.PAULO_LIST = i
					break
			print("[SYSTEM] List " + self.PAULO_LIST.name + " Found")
		except:
			print("[SYSTEM] An error ocurred while trying to get board")
			return

	# Searching for list raul
	def get_list_raul(self):
		try:
			for i in self.BOARD.list_lists():
				if i.name == self.data.get_list_raul():
					self.RAUL_LIST = i
					break
			print("[SYSTEM] List " + self.RAUL_LIST.name + " Found")
		except:
			print("[SYSTEM] An error ocurred while trying to get board")
			return

	# Searching for list vitoria
	def get_list_vitoria(self):
		try:
			for i in self.BOARD.list_lists():
				if i.name == self.data.get_list_vitoria():
					self.VITORIA_LIST = i
					break
			print("[SYSTEM] List " + self.VITORIA_LIST.name + " Found")
		except:
			print("[SYSTEM] An error ocurred while trying to get board")
			return

	# Searching for list fazendo
	def get_list_fazendo(self):
		try:
			for i in self.BOARD.list_lists():
				if i.name == self.data.get_list_fazendo():
					self.FAZENDO_LIST = i
					break
			print("[SYSTEM] List " + self.FAZENDO_LIST.name + " Found")
		except:
			print("[SYSTEM] An error ocurred while trying to get board")
			return

t = TrelloProcess()