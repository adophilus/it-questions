from flask import globals
from flask_sqlalchemy import SQLAlchemy
from ..utilities.General import loadJson
from .private_key_generator import PrivateKeyGenerator

import os

class Config (dict):
	def getMessage (self, message):
		return self.get("messages").get(message)

	def getClassroomStatus (self, status):
		return self.get("classroom")["statuses"].get(classroom_status)

def refreshConfig ():
	pass

globals.db = SQLAlchemy()
config = Config(loadJson(os.path.join("data", "Registrar", "configuration.json")))
globals.config = config
globals.IDgenerator = PrivateKeyGenerator()

if not globals.config["secret_key"]:
	globals.config["secret_key"] = globals.IDgenerator.generate(level = 4)

refreshConfig()
