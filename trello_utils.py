from trello import TrelloClient
import data as dt

class Utils:

	def __init__(self):

		############################################
		## Setting data class
		self.data = dt.Data()
		self.BUFFER = list()


		############################################
		##	Setting Client Connection
		client = TrelloClient(
		    api_key= self.data.get_api_key(),
		    api_secret= self.data.get_api_secret(),
		    token= self.data.get_token(),
		)

		###########################################
		##	Searching for board Name
		all_boards = client.list_boards()
		self.BOARD = None
		for i in all_boards:
			if i.name == self.data.get_board_name():
				self.BOARD = i
				break

		###########################################
		##	Searching for board done list
		self.DONE = None
		for i in self.BOARD.list_lists():
			if i.name == self.data.get_list_name():
				self.DONE = i
				break

		#Getting Cards
		for card in self.DONE.list_cards():
			print(card.customFields[1].name)




		

u = Utils()