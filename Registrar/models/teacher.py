from flask import globals
from flask_login import UserMixin

from ..controllers.config import config
class Teacher (UserMixin, globals.db.Model):
	id = globals.db.Column(globals.db.Text, primary_key = True)
	FIRST_NAME = globals.db.Column(globals.db.Text)
	LAST_NAME = globals.db.Column(globals.db.Text)
	OTHER_NAMES = globals.db.Column(globals.db.Text)
	USERNAME = globals.db.Column(globals.db.Text)
	PASSWORD = globals.db.Column(globals.db.Text)
	EMAIL = globals.db.Column(globals.db.Text)
	BIRTHDAY = globals.db.Column(globals.db.Date)
	PHONE_NUMBER = globals.db.Column(globals.db.Text)
	ACCOUNT_TYPE = globals.db.Column(globals.db.Text, default = config.getAccountType("teacher")["name"])
	ACCOUNT_STATUS = globals.db.Column(globals.db.Text, default = config.getAccountStatus("ACTIVE"))

	def __bool__ (self):
		return True

	@classmethod
	def getByEmail (cls, email):
		return cls.query.filter_by(EMAIL = email).first()

	@classmethod
	def getById (cls, id):
		return cls.query.filter_by(id = id).first()

	@classmethod
	def getByUsername (cls, username):
		return cls.query.filter_by(USERNAME = username).first()