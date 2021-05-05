from flask import globals

from .private_key_generator import PrivateKeyGenerator
from .. import models
from .config import config
from .methods import loadJson, saveJson

import os

class Question ():
	__exists__ = False
	generator = PrivateKeyGenerator()
	questionDetailsPath = None
	questionPublicDetailsPath = None

	def __init__ (self, question_id = None, _object = None, *args, **kwargs):
		question = _object

		if (not object):
			question = models.Question.getById(question_id)

		if (question):
			self.question = question
			self.__exists__ = True
		else:
			self.question = models.Question(id = question_id, *args, **kwargs)

	def __bool__ (self):
		return self.__exists__

	def __str__ (self):
		return self.get("id")

	def setQuestionPath (self, path = None):
		if (self.__exists__):
			if (not path):
				path = os.path.join("data", "questions", self.question.id)
			self.questionDetailsPath = path.join("details.json")
			self.questionPublicDetailsPath = path.join("details-public.json")

	def __loadQuestionDetails (self, from_dict = False):
		if (self.__exists__):
			if (not from_dict):
				self.questionDetails = loadJson(self.questionDetailsPath)
				if (self.get("IS_PUBLIC")):
					self.questionPublicDetails = loadJson(self.questionPublicDetailsPath)
			else:
				self.questionDetails = from_dict
				if (self.get("IS_PUBLIC")):
					self.questionPublicDetails = loadJson(self.questionPublicDetailsPath)

	def saveQuestionDetails (self, details = None, public_details = None):
		if (self.__exists__):
			if (self.get("IS_PUBLIC")):
				if (not public_details):
					public_details = self.questionPublicDetails
				saveJson(self.questionPublicDetailsPath, public_details)

			if (not details):
				details = self.questionDetails
			saveJson(self.questionDetailsPath, details)
			return True

	def updatePublicDetails (self):
		if (self.get("IS_PUBLIC")):
			self.questionPublicDetails = self.questionDetails
			return self.saveQuestionDetails()

	def makePublic (self):
		return self.set("IS_PUBLIC", 1)

	@classmethod
	def __generateId__  (cls, unique = True, question_type = "private"):
		while True:
			id = cls.generator.generate(level = config["id_length"]["question"])

			if (unique):
				question = Question(id)

				if not (question):
					return id

	@classmethod
	def getAll (cls):
		return [Question(_object = question) for question in models.Question.getAll()]

	@classmethod
	def getAllPublic (cls):
		return [ Question(_object = question) for question in models.Question.getAllPublic() ]

	def assignOwner (self, owner):
		self.set("OWNER", owner.get("id"))
		globals.db.session.commit()

	def setCreator (self, creator):
		return self.set("CREATOR", creator.get("id"))

	def setNumberOfQuestions (self, number_of_questions):
		return self.set("NUMBER_OF_QUESTIONS", number_of_questions)

	def create (self):
		if (not self.__exists__):
			self.setQuestionPath()
			os.mkdir(os.dirname(self.questionDetailsPath))

			question_details = {}
			self.saveQuestionDetails(from_dict = question_details)
			self.__loadQuestionDetails(from_dict = question_details)

			globals.db.session.add(self.question)
			globals.db.session.commit()
			self.__exists__ = True

	def delete (self):
		if (self.__exists__):
			globals.db.session.delete(self.question)
			globals.db.session.commit()
			self.__exists__ = False

	def get (self, field):
		return self.question[field]

	def set (self, field, value):
		self.question[field] = value
		globals.db.session.commit()