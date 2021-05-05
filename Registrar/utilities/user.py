from flask import globals
from .account_get import *

class User ():
	is_ready = False

	def __init__ (self, account = None, user_id = None):
		if (account or user_id):
			self._is_ready

		if (account):
			self.account = account
		elif (user_id):
			self.account = Account(user_id)

	def isReady (self):
		return self.is_ready

	def isAdmin (self):
		if not (self.isReady()):
			return False

        if not (self.account.is_active):
            return False

        if self.account.ACCOUNT_TYPE == config["account"]["types"]["administrator"]["name"]:
            return True

    def isParent (self):
    	if not (self.isReady()):
    		return False

        if not (self.account.is_active):
            return False

        if self.account.ACCOUNT_TYPE == config["account"]["types"]["parent"]["name"]:
            return True

    def isTeacher (self):
    	if not (self.isReady()):
    		return False

        if not (self.account.is_active):
            return False

        if self.account.ACCOUNT_TYPE == config["account"]["types"]["teacher"]["name"]:
            return True

    def isStudent (self):
    	if not (self.isReady()):
    		return False

        if not (self.account.is_active):
            return False

        if self.account.ACCOUNT_TYPE == config["account"]["types"]["student"]["name"]:
            return True