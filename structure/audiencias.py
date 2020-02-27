class Audiencias:

	def __init__(self, users):
		self.usersDict = {}
		for i in users:
			self.usersDict[i] = list()

	def addCard(self, user, card):
		self.usersDict[user].append(card)

	def getCardList(self, user):
		return self.usersDict[user]

	def getDict(self):
		return self.usersDict

	def printDict(self):
		print(self.usersDict)