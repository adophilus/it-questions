from datetime import datetime
from flask import globals

from .config import config
from .classroom import Classroom
from .methods import fernetEncrypt, fernetDecrypt
from .private_key_generator import PrivateKeyGenerator
from .. import models

from .methods import loadJson, saveJson

import os
import shutil

class Account ():
	__exists__ = False
	generator = PrivateKeyGenerator()
	accountDetails = {}
	accountDetailsPath = None
	accountSettings = {}
	accountSettingsPath = None

	def __init__ (self, id = None, username = None, email = None, account_type = config.getAccount("student")["name"], _object = None):
		if (_object):
			self.__determineAccountType(_object = _object, account_type = account_type)
		elif (email):
			self.__determineAccountType(email = email, account_type = account_type)
		elif (username):
			self.__determineAccountType(username = username, account_type = account_type)
		else:
			self.__determineAccountType(id, account_type = account_type)

	def __bool__ (self):
		return self.__exists__

	def __determineAccountType (self, id = None, username = None, email = None, account_type = config.getAccount("student")["name"], _object = None):
		if (object):
			administrator = _object
		if (email):
			administrator = models.Administrator.getByEmail(email)
			parent = models.Parent.getByEmail(email)
			teacher = models.Teacher.getByEmail(email)
			student = Student.getByEmail(email)
		elif (username):
			administrator = models.Administrator.getByUsername(username)
			parent = models.Parent.getByUsername(username)
			teacher = models.Teacher.getByUsername(username)
			student = Student.getByUsername(username)
		else:
			administrator = models.Administrator.getById(id)
			parent = models.Parent.getById(id)
			teacher = models.Teacher.getById(id)
			student = Student.getById(id)

		if (administrator):
			self.account = administrator
			self.__exists__ = True
		elif (parent):
			self.account = parent
			self.__exists__ = True
		elif (teacher):
			self.account = teacher
			self.__exists__ = True
		elif (student):
			self.account = student
			self.__exists__ = True
		else:
			if (account_type == config.getAccount("administrator")["name"]):
				self.account = models.Administrator(id = self.__generateId__())
			elif (account_type == config.getAccount("parent")["name"]):
				self.account = models.Parent(id = self.__generateId__())
			elif (account_type == config.getAccount("teacher")["name"]):
				self.account = models.Teacher(id = self.__generateId__())
			else:
				self.account = Student(id = self.__generateId__())

	def setAccountPath (self, path = None):
		if (self.__exists__):
			if (not path):
				path = os.path.join("data", f'{self.account.ACCOUNT_TYPE}s')
			self.accountDetailsPath = path.join("details.json")
			self.accountSettingsPath = path.join("settings.json")

	def __loadAccountDetails (self, from_dict = False):
		if (self.__exists__):
			if (not from_dict):
				self.accountDetails = loadJson(self.accountDetailsPath)
			else:
				self.accountDetails = from_dict

	def saveAccountDetails (self, details = None):
		if (self.__exists__):
			if (not details):
				details = self.accountDetails
			saveJson(self.accountDetailsPath, details)
			return True

	def __loadAccountSettings (self, from_dict = False):
		if (self.__exists__):
			if (not from_dict):
				self.accountSettings = loadJson(self.accountSettingsPath)
			else:
				self.accountSettings = from_dict

	def saveAccountSettings (self, settings = None):
		if (self.__exists__):
			if (not settings):
				settings = self.accountSettings
			saveJson(self.accountSettingsPath, settings)

	@classmethod
	def __generateId__ (cls, unique = True):
		while True:
			id = cls.generator.generate(level = config["id_length"]["account"])

			if (unique):
				account = cls(id)

				if (not account):
					return id

	@classmethod
	def encryptPassword (cls, password):
		return fernetEncrypt(password, key = config["ENCRYPTION_KEY"].encode("UTF-8")).decode("UTF-8")

	@classmethod
	def decryptPassword (cls, password):
		return fernetDecrypt(password, key = config["ENCRYPTION_KEY"].encode("UTF-8")).decode("UTF-8")

	@classmethod
	def getByEmail (cls, email):
		return cls(email = email)

	@classmethod
	def getById (cls, id):
		return cls(id)

	@classmethod
	def getByUsername (cls, username):
		return cls(username = username)

	@classmethod
	def isAllowedEntry (cls):
		return config["account"]["statuses"][self.get("ACCOUNT_STATUS")].get("grant_access")

	def get (self, field):
		return self.account[field]

	def set (self, field, value):
		self.account[field] = value

	def hasUsername (self, username):
		return self.get("USERNAME") == username

	def hasPassword (self, password):
		return self.get("PASSWORD") == self.decryptPassword(password)

	def isAdmin (self):
		return self.get("ACCOUNT_TYPE") == config.getAccountType("administrator")["name"]

	def isParent (self):
		return self.get("ACCOUNT_TYPE") == config.getAccountType("parent")["name"]

	def isTeacher (self):
		return self.get("ACCOUNT_TYPE") == config.getAccountType("teacher")["name"]

	def isStudent (self):
		return self.get("ACCOUNT_TYPE") == config.getAccountType("student")["name"]

	def create (self, account_details = None, account_settings = None):
		if (not self.__exists__):
			if ((not account_details) and (not account_settings)):
				return self.account.create()

			self.__exists__ = True

			self.setAccountPath()

			if (not account_details):
				account_details = {}
			self.__loadAccountDetails(from_dict = account_details)
			self.saveAccountDetails()

			if (not account_settings):
				account_settings = {
					"theme": "default",# hard-coded (for lack of an alternative theme)
					"last_login": "",# f"{globals.clock.date()} {globals.clock.time()}"
					"login_history": {},# history of previous login attempts
					"secret_question": "",# a secret question for logging into the account (in the case of "forgotten password")
					"secret_question_answer": "",# the answer to the secret question
					"enable_secret_question": ""# determines whether the secret question will be enaled or not
				}
			self.__loadAccountSettings(from_dict = account_settings)
			self.saveAccountSettings()
			return True

	def delete (self, first_call = True):
		if (self.__exists__):
			shutil.rmtree(os.path.join("data", f"{self.account.ACCOUNT_STATUS}s", self.account.id))
			if (first_call):
				self.account.delete(first_call = False)
			self.__exists__ = False
			return True

class Administrator (models.Administrator, Account):
	def __init__ (self, *args, **kwargs):
		self.setAccountPath(os.path.join("data", self.ACCOUNT_TYPE))
		self.__loadAccountDetails()
		self.__loadAccountSettings()
		models.Administrator.__init__(self, *args, **kwargs)

	def __dict__ (self):
		return self.id

	def __str__ (self):
		return self.id

	def create (self):
		account_details = {
			"unread_messages": 0,
			"unread_notifications": 0
		}

		account_settings = {
			"theme": "default",# hard-coded (for lack of an alternative theme)
			"last_login": "",# f"{globals.clock.date()} {globals.clock.time()}"
			"login_history": {},# history of previous login attempts
			"secret_question": "",# a secret question for logging into the account (in the case of "forgotten password")
			"secret_question_answer": "",# the answer to the secret question
			"enable_secret_question": ""# determines whether the secret question will be enaled or not
		}

		return Account.create(self, account_details = account_details, account_settings = account_settings)

	def delete (self, first_call = True):
		globals.db.session.delete(self)
		globals.db.session.commit()
		if (first_call):
			return Account.delete(self, False)

	def get (self, field):
		return self[field]

	def set (self, field, value):
		self[field] = value

class Parent (models.Parent, Account):
	def __init__ (self, *args, **kwargs):
		self.setAccountPath(os.path.join("data", self.ACCOUNT_TYPE))
		self.__loadAccountDetails()
		self.__loadAccountSettings()
		models.Parent.__init__(self, *args, **kwargs)

	def __dict__ (self):
		return self.id

	def __str__ (self):
		return self.id

	def addWard (self, ward):
		if (isinstance(ward, models.Student)):
			self.wards.append(ward)
			self.WARDS = jsonize(self.wards)
			globals.db.session.commit()
			return True

	def hasWard (self, ward):
		return ward in self.wards

	def removeWard (self, ward):
		if (ward in self.wards):
			self.wards.remove(ward)
			self.WARD = jsonize(self.wards)
			globals.db.session.commit()
			return True

	def create (self):
		account_details = {
			"unread_messages": 0,
			"unread_notifications": 0
		}

		account_settings = {
			"theme": "default",# hard-coded (for lack of an alternative theme)
			"last_login": "",# f"{globals.clock.date()} {globals.clock.time()}"
			"login_history": {},# history of previous login attempts
			"secret_question": "",# a secret question for logging into the account (in the case of "forgotten password")
			"secret_question_answer": "",# the answer to the secret question
			"enable_secret_question": ""# determines whether the secret question will be enaled or not
		}

		return Account.create(self, account_details = account_details, account_settings = account_settings)

	def delete (self, first_call = True):
		globals.db.session.delete(self)
		globals.db.session.commit()
		if (first_call):
			return Account.delete(self, False)

	def get (self, field):
		return self[field]

	def set (self, field, value):
		self[field] = value

class Teacher (models.Teacher, Account):
	classrooms = []
	questions = []

	def __init__ (self, *args, **kwargs):
		self.setAccountPath(os.path.join("data", self.ACCOUNT_TYPE))
		self.__loadAccountDetails()
		self.__loadAccountSettings()
		self.__populateClassrooms()
		models.Teacher.__init__(self, *args, **kwargs)

	def __dict__ (self):
		return self.id

	def __str__ (self):
		return self.id

	def __populateClassrooms (self):
		for classroom in self.accountDetails["classroom"]:
			self.classrooms.append(Classroom(classroom["id"]))

	def addClassroom (self, classroom, classroom_profile = None):
		if (not classroom_profile):
			return classroom_profile

		if (isinstance(classroom, Classroom)):
			self.account_details[classroom.id] = classroom_profile
			self.saveAccountDetails()
			return True

	def addQuestion (self, question):
		if (isinstance(question, Question)):
			self.questions.append(question)

	def addSubjectsTeaching (self, subject):
		if (isinstance(subject, models.Subject)):
			self.subjects_teaching.append(subject)

	def create (self):
		account_details = {
			"unread_messages": 0,
			"unread_notifications": 0,
			"is_homeroom_teacher": False,
			"questions": self.questions,
			"subjects_teaching": self.subjects_teaching,
			"classroom": {}
		}

		account_settings = {
			"theme": "default",# hard-coded (for lack of an alternative theme)
			"last_login": "",# f"{globals.clock.date()} {globals.clock.time()}"
			"login_history": {},# history of previous login attempts
			"secret_question": "",# a secret question for logging into the account (in the case of "forgotten password")
			"secret_question_answer": "",# the answer to the secret question
			"enable_secret_question": ""# determines whether the secret question will be enaled or not
		}

		return Account.create(self, account_details = account_details, account_settings = account_settings)

	def delete (self, first_call = True):
		globals.db.session.delete(self)
		globals.db.session.commit()
		if (first_call):
			return Account.delete(self, False)

	def get (self, field):
		return self[field]

	def set (self, field, value):
		self[field] = value

class Student (models.Student, Account):
	classrooms = []

	def __init__ (self, *args, **kwargs):
		self.setAccountPath(os.path.join("data", self.ACCOUNT_TYPE))
		self.__loadAccountDetails()
		self.__loadAccountSettings()
		self.__populateClassrooms()
		models.Student.__init__(self, *args, **kwargs)

	def __dict__ (self):
		return self.id

	def __str__ (self):
		return self.id

	def __populateClassrooms (self):
		for classroom in self.accountDetails["classroom"]:
			self.classrooms.append(Classroom(classroom["id"]))

	def addClassroom (self, classroom, classroom_profile = None):
		if (not classroom_profile):
			return classroom_profile

		if (isinstance(classroom, Classroom)):
			self.account_details[classroom.id] = classroom_profile
			self.saveAccountDetails()
			return True

	def calculateAge (self):
		self.AGE = ((datetime.now() - self.BIRTHDAY).days) + 1

	def create (self):
		account_details = {
			"unread_messages": 0,
			"unread_notifications": 0,
			"unread_public_remarks": 0,
			"height": "unknown",
			"weight": "unknown",
			"complexion": "unknown",
			"eye_color": "unknown",
			"subjects_offerred": [],
			"extracurricular_activities": extracurricular_activities,
			"guardian": {},
			"classroom": {}
		}

		account_settings = {
			"theme": "default",# hard-coded (for lack of an alternative theme)
			"last_login": "",# f"{globals.clock.date()} {globals.clock.time()}"
			"login_history": {},# history of previous login attempts
			"secret_question": "",# a secret question for logging into the account (in the case of "forgotten password")
			"secret_question_answer": "",# the answer to the secret question
			"enable_secret_question": ""# determines whether the secret question will be enaled or not
		}

		self.calculateAge()
		return Account.create(self, account_details = account_details, account_settings = account_settings)

	def delete (self, first_call = True):
		for classroom in self.classrooms:
			self.accountDetails["classroom"].remove(classroom)
			classroom.removeMember(self.id)

		globals.db.session.delete(self)
		globals.db.session.commit()
		if (first_call):
			return Account.delete(self, False)

	def get (self, field):
		return self[field]

	def set (self, field, value):
		self[field] = value