import datetime

class Card:

	def __init__(self, users):
		self.usersDict = {}
		for i in users:
			self.usersDict[i] = list()

	######################################
	# Methods
	def sort_dict_lists(self):
		self.UserDict.sort(key=lambda x: datetime.datetime.strptime(x['Prazo'], '%d/%m/%Y'))

	def addCard(self, user, card):
		self.usersDict[user].append(card)

	######################################
	# Getts and Setters

	def getCardList(self, user):
		return self.usersDict[user]

	def getDict(self):
		return self.usersDict

	def printDict(self):
		print(self.usersDict)