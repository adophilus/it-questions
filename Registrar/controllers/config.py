from collections import defaultdict

from flask import globals
from flask_sqlalchemy import SQLAlchemy

from .methods import loadJson
from .private_key_generator import PrivateKeyGenerator

import os

class Config (defaultdict):
	def __init__ (self, path = os.path.join("data", "Registrar", "configuration.json")):
		self.path = path
		defaultdict.__init__(self, lambda: None, loadJson(self.path))

	def getAccountStatus (self, status):
		return self["account"]["status"][status]

	def getAccountType (self, account_type):
		return self["account"]["types"][account_type]

	def getMessage (self, message):
		return self["messages"].get(message)

	def getClassroomStatus (self, status):
		return self["classroom"]["status"][status]

	def save (self, path = None):
		if (not path):
			path = self.path
		saveJson(path, self)

globals.db = SQLAlchemy()
config = Config()
generator = PrivateKeyGenerator()
school_prefs = loadJson(os.path.join("data", "school", "preferences.json"))

if (not config["secret_key"]):
	config["secret_key"] = generator.generate(level = 4)
