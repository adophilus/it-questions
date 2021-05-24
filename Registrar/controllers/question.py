from flask import globals

from .private_key_generator import PrivateKeyGenerator
from .. import models
from .config import config
from .methods import loadJson, saveJson

import os

class Question (models.Question):
	__exists__ = False
	generator = PrivateKeyGenerator()
	questionDetailsPath = None
	questionPublicDetailsPath = None
	questionDetails = {}
	questionPublicDetails = {}

	def __init__ (self, id, exists = False, *args, **kwargs):
		kwargs["id"] = id
		self.__exists__ = exists
		models.Question(*args, **kwargs)
		self.setQuestionPath()
		if (self):
			self.loadQuestionDetails()

	def __bool__ (self):
		return self.__exists__

	def __str__ (self):
		return self.id

	def __iter__ (self):
		return [
			[ "id", self.id ],
			[ "title", self.TITLE ],
			[ "is_public", self.IS_PUBLIC ],
			[ "number_of_questions", self.NUMBER_OF_QUESTIONS ],
			[ "creator", self.CREATOR ],
			[ "owner", self.OWNER ],
			[ "image", self.IMAGE_PATH ]
		].__iter()

	def __repr__ (self):
		return f"<Question id='{self.id}' owner='{self.OWNER}' creator='{self.CREATOR}'>"

	def as_dict (self):
		return dict(self.__iter__())

	def setQuestionPath (self, path = None):
		if (self):
			if (not path):
				path = os.path.join("data", "questions", self.id)
			self.questionDetailsPath = path.join("details.json")
			self.questionPublicDetailsPath = path.join("details-public.json")

	def loadQuestionDetails (self, from_dict = False):
		if (self):
			if (from_dict):
				if (self.IS_PUBLIC):
					self.questionPublicDetails = loadJson(self.questionPublicDetailsPath)
				self.questionDetails = loadJson(self.questionDetailsPath)
				return True

			if (self.IS_PUBLIC):
				self.questionPublicDetails = loadJson(self.questionPublicDetails)
			self.questionDetails = loadJson(self.questionDetails)

	def saveQuestionDetails (self, details = None, public_details = None):
		if (self):
			if (self.get("IS_PUBLIC")):
				if (not public_details):
					public_details = self.questionPublicDetails
				saveJson(self.questionPublicDetailsPath, public_details)

			if (not details):
				details = self.questionDetails
			saveJson(self.questionDetailsPath, details)
			return True

	def updatePublicDetails (self):
		if (self.IS_PUBLIC):
			self.questionPublicDetails = self.questionPublicDetails
			return self.saveQuestionDetails()

	def makePublic (self):
		self.IS_PUBLIC = 1
		return self.save()

	@classmethod
	def __generateId__  (cls, unique = True, question_type = "private"):
		while True:
			id = cls.generator.generate(level = config["id_length"]["question"])

			if (unique):
				question = Question(id)

				if not (question):
					return id

	def assignOwner (self, owner):
		self.OWNER = owner.get("id")
		return self.save()

	def setCreator (self, creator):
		self.CREATOR = creator.get("id")
		return self.save()

	def setNumberOfQuestions (self, number_of_questions):
		return self.set("NUMBER_OF_QUESTIONS", number_of_questions)

	def create (self):
		if (not self):
			os.mkdir(os.dirname(self.questionDetailsPath))

			self.questionDetails = {}
			self.questionPublicDetails = {}
			self.saveQuestionDetails()

			globals.db.session.add(self)
			globals.db.session.commit()
			self.__exists__ = True

	def delete (self):
		if (self):
			globals.db.session.delete(self)
			globals.db.session.commit()
			self.__exists__ = False

	def save (self):
		return globals.db.session.commit()