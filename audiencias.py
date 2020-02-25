class Audiencias:

	def __init__(self, users):
		self.usersDict = {}
		for i in users:
			self.usersDict[i] = list()

	def addCard(self, user, card):
		self.userDict[user].append(card)

	def getCardList(self, user):
		return self.userDict[user]