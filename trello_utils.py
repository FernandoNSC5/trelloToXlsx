from trello import TrelloClient, Member
import data as dt

class Utils:

	def __init__(self):

		############################################
		## Setting data class
		self.data = dt.Data()
		self.CARDS = list()


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
				if i.name == self.data.get_list_name():
					self.DONE_LIST = i
					break
			print("[TRELLO] List Found")
		except:
			print("[TRELLO] An error ocurred while trying to get board 'Finalizado'")
			return
		###########################################

		self.set_cards()	#Creating card buffer
		print(self.CARDS)


	###########################################
	###########################################
	##				METHODS					 ##	
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
			user_id = card.member_id[0]
			user_id = Member(self.client, user_id)
			data["Advogado"] = user_id.fetch().full_name

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

u = Utils()