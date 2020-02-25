from trello import TrelloClient, Member
import data as dt
import cards as cd
import acompanhamentos as ac
import audiencias as ad
import xlsx
import threading

#Deprecated
class Utils:

	def __init__(self):

		############################################
		## Setting data class
		self.data = dt.Data()
		self.cards = cd.Card()
		self.acompanhamentos = ac.Acompanhamentos()
		self.audiencias = ad.Audiencias()

		self.CARDS = list()
		self.cards_advogado = {}

		############################################
		##	Setting Client Connection
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
		###########################################

		###########################################
		##	Searching for board Name
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
		###########################################

		###########################################
		##	Searching for board done list
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
		###########################################

		###########################################
		##	Searching for board estudos e acompanhamentos
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
		############################################

		############################################
		##	Searching for board Audiências e julgamentos
		try:
			self.AUDIENCIAS_E_JULGAMENTOS = None
			for i in self.BOARD.list_lists():
				if i.name == self.date.get_list_audiencias_e_julgamentos():
					self.AUDIENCIAS_E_JULGAMENTOS = i
			print("[TRELLO] List "+ self.AUDIENCIAS_E_JULGAMENTOS.name +" Found")
		except:
			print("[TRELLO] An error ocurred while trying to get board")
			return
		############################################

		############################################
		##	Data cards processing
		self.process_feito()
		self.process_acompanhamento()
		self.processo_audiencias

		self.set_cards_feito()	#Creating card buffer @Deprecated
		self.create_xlsx()	#Writer thread

	###########################################
	###########################################
	##				METHODS					 ##	
	def process_feito(self):
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






	def set_cards(self):
		# DATA STRUCTURE DICT
		for card in self.DONE_LIST.list_cards():
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
				data["Advogado"] = "Nenhum advogado atrelado"

			#Dates
			data["Realizado em"] = self.clean_date(data["Realizado em"])
			data["Criado em"] = self.clean_date(data["Criado em"])
			data["Prazo Fatal"] = self.clean_date(data["Prazo Fatal"])
			data["Prazo"] = self.clean_date(data["Prazo"])

			self.CARDS.append(data)
			

	def clean_date(self, date_str):
		if date_str == None:
			return None
		new_date = date_str[0:10].split("-")
		return new_date[2]+"/"+new_date[1]+"/"+new_date[0]

	#Starting thread
	def create_xlsx(self):
		print("starting trhread")
		thr = threading.Thread(target=self.xlsx_slave, args=([self.CARDS]), kwargs={})
		thr.start()

	#Thread function
	def xlsx_slave(self, name, cards):
		print("[+] New thread is up")
		excel = xlsx.XLSX(cards[0])

u = Utils()