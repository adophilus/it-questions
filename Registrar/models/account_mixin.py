from ..controllers.methods import printDebug

class AccountMixin ():
	@classmethod
	def getByEmail (cls, email):
		# printDebug("Fetching account by id", "models.AccountMixin.getByEmail")
		a = cls.query.filter_by(EMAIL = email).first()
		if (a != None):
			a.__init__(exists = True)
		return a

	@classmethod
	def getById (cls, id):
		# printDebug("Fetching account by id", "models.AccountMixin.getById")
		a = cls.query.filter_by(id = id).first()
		if (a != None):
			a.__init__(exists = True)
		return a

	@classmethod
	def getByUsername (cls, username):
		# printDebug("Fetching account by username", "models.AccountMixin.getByUsername")
		a = cls.query.filter_by(USERNAME = username).first()
		if (a != None):
			a.__init__(exists = True)
		return a