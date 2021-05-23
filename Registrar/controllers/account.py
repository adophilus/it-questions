from datetime import date, datetime
from flask import globals
from flask_login import current_user

from . import validate
from .config import config
from .classroom import Classroom
from .methods import fernetEncrypt, fernetDecrypt, loadJson, printDebug, saveJson, sendFalse
from .private_key_generator import PrivateKeyGenerator
from .. import models

import os
import shutil

class Account ():
	__exists__ = False
	generator = PrivateKeyGenerator()
	accountDetails = {}
	accountDetailsPath = None
	accountSettings = {}
	accountSettingsPath = None
	accountType = None

	def __init__ (self, id = None, username = None, email = None, account_type = config.getAccountType("student")["name"], _object = None, check = False):
		if (_object):
			self.__determineAccountType(_object = _object, account_type = account_type, check = check)
		elif (email):
			printDebug(f"Determining account with email {email}")
			self.__determineAccountType(email = email, account_type = account_type, check = check)
		elif (username):
			printDebug(f"Determining account with username {username}")
			self.__determineAccountType(username = username, account_type = account_type, check = check)
		else:
			printDebug(f"Determining account with id {id}")
			self.__determineAccountType(id, account_type = account_type, check = check)

	def __bool__ (self):
		return self.__exists__

	def __getitem__ (self, item):
		if (hasattr(self, item)):
			return getattr(self, item)
		raise KeyError(f"{item} does not exist!")

	def __str__ (self):
		return self.get("id")

	def __determineAccountType (self, id = None, username = None, email = None, account_type = config.getAccountType("student")["name"], _object = None, check = False):
		if (_object):
			administrator = _object
		elif (email):
			printDebug(f"Checking accounts that have the email '{email}'")
			administrator = Administrator.getByEmail(email)
			parent = Parent.getByEmail(email)
			teacher = Teacher.getByEmail(email)
			student = Student.getByEmail(email)
		elif (username):
			printDebug(f"Checking accounts that have the username '{username}'")
			administrator = Administrator.getByUsername(username)
			parent = Parent.getByUsername(username)
			teacher = Teacher.getByUsername(username)
			student = Student.getByUsername(username)
		else:
			printDebug(f"Checking accounts that have the id '{id}'")
			administrator = Administrator.getById(id)
			parent = Parent.getById(id)
			teacher = Teacher.getById(id)
			student = Student.getById(id)

		if (administrator):
			self.account = administrator
			self.accountType = self.account.accountType
			self.__exists__ = True
		elif (parent):
			self.account = parent
			self.accountType = self.account.accountType
			self.__exists__ = True
		elif (teacher):
			self.account = teacher
			self.accountType = self.account.accountType
			self.__exists__ = True
		elif (student):
			self.account = student
			self.accountType = self.account.accountType
			self.__exists__ = True
		else:
			if (not check):
				printDebug(f"Checking accounts (check = True)", "Account.__determineAccountType")
				if (account_type == config.getAccountType("administrator")["name"]):
					self.account = Administrator(id = self.__generateId__())
				elif (account_type == config.getAccountType("parent")["name"]):
					self.account = Parent(id = self.__generateId__())
				elif (account_type == config.getAccountType("teacher")["name"]):
					self.account = Teacher(id = self.__generateId__())
				else:
					self.account = Student(id = self.__generateId__())
				self.accountType = self.account.accountType

	def setAccountPath (self, path = None):
		if (self.__exists__):
			if (isinstance(self, Student)):
				if (not path):
					path = os.path.join("data", f'{self.ACCOUNT_TYPE}s', self.id)
					self.accountDetailsPath = os.path.join(path, "details.json")
					self.accountSettingsPath = os.path.join(path, "settings.json")
			else:
				if (not path):
					path = os.path.join("data", f'{self.account.ACCOUNT_TYPE}s', self.account.id)
					self.accountDetailsPath = os.path.join(path, "details.json")
					self.accountSettingsPath = os.path.join(path, "settings.json")

	def loadAccountDetails (self, from_dict = False):
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

	def loadAccountSettings (self, from_dict = False):
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
				account = cls(id, check = True)

				if (not account):
					return id

	def getAccount (self):
		return self.account

	@classmethod
	def encryptPassword (cls, password):
		return fernetEncrypt(password, key = config["ENCRYPTION_KEY"].encode("UTF-8")).decode("UTF-8")

	@classmethod
	def decryptPassword (cls, password):
		return fernetDecrypt(password, key = config["ENCRYPTION_KEY"].encode("UTF-8")).decode("UTF-8")

	@classmethod
	def getByEmail (cls, email):
		return cls(email = email, check = True)

	@classmethod
	def getById (cls, id):
		return cls(id, check = True)

	@classmethod
	def getByUsername (cls, username):
		return cls(username = username, check = True)

	def isAllowedEntry (self):
		return config.getAccountStatus(self.get("ACCOUNT_STATUS"))["grant_access"]

	def get (self, field):
		return self.account.get(field)

	def set (self, field, value):
		return self.account.set(field, value)

	def hasUsername (self, username):
		return self.get("USERNAME") == username

	def hasPassword (self, password):
		return self.decryptPassword(self.get("PASSWORD")) == password

	def isAdmin (self):
		return self.accountType == config.getAccountType("administrator")["name"]

	def isParent (self):
		return self.accountType == config.getAccountType("parent")["name"]

	def isTeacher (self):
		return self.accountType == config.getAccountType("teacher")["name"]

	def isStudent (self):
		return self.accountType == config.getAccountType("student")["name"]

	def addClassroom (self, classroom, classroom_profile):
		if (self.isStudent() or self.isTeacher()):
			printDebug("adding classroom to account details", "Account.addClassroom")
			return self.account.addClassroom(classroom, classroom_profile)

	def getClassrooms (self):
		if (not (self.isStudent() or self.isTeacher())):
			return []
		printDebug(type(self), "Account.getClassrooms")
		return self.account.classrooms

	def create (self, account_details, account_settings, first_name = "", last_name = "", other_names = "", birthday = None, email = "", phone_number = "", username = "", password = "", account_type = config.getAccountType("student")["name"], classroom = None, department = "", subjects_offered = [], extracurricular_activities = [], subjects_teaching = [], ward_id = ""):
		if (not self.__exists__):
			if ((not account_details) and (not account_settings)):
				return self.account.create(first_name, last_name, other_names, birthday, email, phone_number, username, password, account_type, classroom = classroom, department = department, subjects_offered = subjects_offered, extracurricular_activities = extracurricular_activities, subjects_teaching = subjects_teaching, ward_id = ward_id)

			self.__exists__ = True

			self.setAccountPath()

			os.mkdir(os.path.dirname(self.accountDetailsPath))

			if (not account_details):
				account_details = {}
			self.loadAccountDetails(from_dict = account_details)
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
			self.loadAccountSettings(from_dict = account_settings)
			self.saveAccountSettings()

			return True

	def delete (self, first_call = True):
		if (self.__exists__):
			shutil.rmtree(os.path.join("data", f"{self.accountType}s", self.account.get("id")))
			if (first_call):
				self.account.delete(first_call = False)
			self.__exists__ = False
			return True


class AccountMixin ():
	classrooms = []

	def __init__ (self):
		if (self):
			self.setAccountPath("data")
			self.loadAccountDetails()
			self.loadAccountSettings()

	def __bool__ (self):
		return self.__exists__

	def addClassroom (self, classroom, classroom_profile):
		if (self.isStudent() or self.isTeacher()):
			printDebug("adding classroom to account details", "AccountMixin.addClassroom")
			self.accountDetails["classroom"][classroom.get("id")] = classroom_profile
			self.classrooms.append(classroom)
			self.saveAccountDetails()
			return True

	def getClassrooms (self):
		printDebug(type(self), "AccountMixin.getClassrooms")
		return self.classrooms

	def populateClassrooms (self):
		# VERY DANGEROUS!!! RAISES MAX RECURSION DEPTH EXCEPTION # print("current_user:",current_user)
		# ALSO VERY DANGEROUS!!! CALLS 'current_user' MULTIPLE TIMES THEREBY ADDING MULTIPLE CLASSROOMS # print("dir(current_user):",dir(current_user))
		if (self):
			for classroom_id in self.accountDetails["classroom"].keys():
				created = False
				for classroom in self.classrooms:
					if classroom.get("id") == classroom_id:
						created = True
						break
				if (not created):
					self.classrooms.append(Classroom(classroom_id))

	def setAccountPath (self, path = "data"):
		if (self):
			path = os.path.join(path, f'{self.ACCOUNT_TYPE}s', self.id)
			self.accountDetailsPath = os.path.join(path, "details.json")
			self.accountSettingsPath = os.path.join(path, "settings.json")

	def loadAccountDetails (self, from_dict = False):
		if (self):
			if (not from_dict):
				self.accountDetails = loadJson(self.accountDetailsPath)
			else:
				self.accountDetails = from_dict

	def saveAccountDetails (self, details = None):
		if (self):
			if (not details):
				details = self.accountDetails
			saveJson(self.accountDetailsPath, details)
			return True

	def loadAccountSettings (self, from_dict = False):
		if (self):
			if (not from_dict):
				self.accountSettings = loadJson(self.accountSettingsPath)
			else:
				self.accountSettings = from_dict

	def saveAccountSettings (self, settings = None):
		if (self):
			if (not settings):
				settings = self.accountSettings
			saveJson(self.accountSettingsPath, settings)

class Administrator (models.Administrator, AccountMixin, Account):
	accountType = config.getAccountType("administrator")["name"]

	def __init__ (self, exists = False, **kwargs):
		self.__exists__ = exists
		kwargs["ACCOUNT_TYPE"] = config.getAccountType("administrator")["name"]
		models.Administrator.__init__(self, **kwargs)
		AccountMixin.__init__(self)

	def __str__ (self):
		return self.id

	def create (self, first_name, last_name, other_names, birthday, email, phone_number, username, password, account_type, **kwargs):
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

		account_details.update(self.accountDetails)
		account_settings.update(self.accountSettings)

		self.set("first_name", first_name)
		self.set("last_name", last_name)
		self.set("last_name", last_name)
		self.set("other_names", other_names)
		self.set("birthday", birthday)
		self.set("email", email)
		self.set("phone_number", phone_number)
		self.set("username", username)
		self.set("password", password)
		self.set("ACCOUNT_STATUS", config.getAccountStatus("ACTIVE")["status"])

		globals.db.session.add(self)
		globals.db.session.commit()

		return Account.create(self, account_details = account_details, account_settings = account_settings)

	def delete (self, first_call = True):
		globals.db.session.delete(self)
		globals.db.session.commit()
		if (first_call):
			return Account.delete(self, False)

	def stepDownRank (self):
		if (self.ADMIN_RANK >= 0):
			self.ADMIN_RANK -= 1
			return True

	def stepUpRank (self):
		if (self.ADMIN_RANK < (len(config.getAccountType("administrator")["rank"])) - 1):
			self.ADMIN_RANK += 1
			return True

	def setAccountStatus (self, account_status):
		self.ACCOUNT_STATUS = account_status

	def get (self, field):
		if (str(field).lower() == "id"):
		    return self.id
		if (str(field).upper() == "FIRST_NAME"):
			return self.FIRST_NAME
		elif (str(field).upper() == "LAST_NAME"):
			return self.LAST_NAME
		elif (str(field).upper() == "OTHER_NAMES"):
			self.OTHER_NAMES
		elif (str(field).upper() == "BIRTHDAY"):
			return self.BIRTHDAY
		elif (str(field).upper() == "USERNAME"):
			return self.USERNAME
		elif (str(field).upper() == "PASSWORD"):
			return self.PASSWORD
		elif (str(field).upper() == "EMAIL"):
			email = validate.email(value)
			if (not email):
				return sendFalse(config.getMessage("INVALID_EMAIL"))
			return self.EMAIL
		elif (str(field).upper() == "PHONE_NUMBER"):
			return self.PHONE_NUMBER
		else:
			raise Exception(f"Invalid field {field}!")

	def set (self, field, value):
		if (str(field).upper() == "FIRST_NAME"):
			self.FIRST_NAME = value
		elif (str(field).upper() == "LAST_NAME"):
			self.LAST_NAME = value
		elif (str(field).upper() == "OTHER_NAMES"):
			self.OTHER_NAMES = value
		elif (str(field).upper() == "BIRTHDAY"):
			self.BIRTHDAY = value
		elif (str(field).upper() == "USERNAME"):
			username = validate.username(value)
			if (not username):
				raise sendFalse(config.getMessage("INVALID_USERNAME"))
			self.USERNAME = username
		elif (str(field).upper() == "PASSWORD"):
			password = validate.password(value)
			if (not password):
				raise sendFalse(config.getMessage("INVALID_PASSWORD"))
			self.PASSWORD = self.encryptPassword(value)
		elif (str(field).upper() == "EMAIL"):
			email = validate.email(value)
			if (not email):
				return sendFalse(config.getMessage("INVALID_EMAIL"))
			self.EMAIL = value
		elif (str(field).upper() == "PHONE_NUMBER"):
			self.PHONE_NUMBER = value
		elif (str(field).upper() == "ACCOUNT_STATUS"):
			self.ACCOUNT_STATUS = value
		else:
			raise Exception(f"Invalid field {field}!")

class Parent (models.Parent, AccountMixin, Account):
	accountType = config.getAccountType("parent")["name"]

	def __init__ (self, exists = False, **kwargs):
		self.__exists__ = exists
		kwargs["ACCOUNT_TYPE"] = config.getAccountType("parent")["name"]
		models.Parent.__init__(self, **kwargs)
		AccountMixin.__init__(self)

	def __str__ (self):
		return self.id

	def addWard (self, ward):
		if (isinstance(ward, models.Student)):
			if (ward):
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

	def create (self, first_name, last_name, other_names, birthday, email, phone_number, username, password, account_type, wards = [], **kwargs):
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

		account_details.update(self.accountDetails)
		account_settings.update(self.accountSettings)

		self.set("first_name", first_name)
		self.set("last_name", last_name)
		self.set("last_name", last_name)
		self.set("other_names", other_names)
		self.set("birthday", birthday)
		self.set("email", email)
		self.set("phone_number", phone_number)
		self.set("username", username)
		self.set("password", password)
		self.set("ACCOUNT_STATUS", config.getAccountStatus("ACTIVE")["status"])
		for ward_id in wards:
			self.addWard(Student(ward_id, check = True))

		globals.db.session.add(self)
		globals.db.session.commit()

		return Account.create(self, account_details = account_details, account_settings = account_settings)

	def delete (self, first_call = True):
		globals.db.session.delete(self)
		globals.db.session.commit()
		if (first_call):
			return Account.delete(self, False)

	def setAccountStatus (self, account_status):
		self.ACCOUNT_STATUS = account_status

	def get (self, field):
		if (str(field).lower() == "id"):
		    return self.id
		if (str(field).upper() == "FIRST_NAME"):
			return self.FIRST_NAME
		elif (str(field).upper() == "LAST_NAME"):
			return self.LAST_NAME
		elif (str(field).upper() == "OTHER_NAMES"):
			self.OTHER_NAMES
		elif (str(field).upper() == "BIRTHDAY"):
			return self.BIRTHDAY
		elif (str(field).upper() == "USERNAME"):
			return self.USERNAME
		elif (str(field).upper() == "PASSWORD"):
			return self.PASSWORD
		elif (str(field).upper() == "EMAIL"):
			email = validate.email(value)
			if (not email):
				return sendFalse(config.getMessage("INVALID_EMAIL"))
			return self.EMAIL
		elif (str(field).upper() == "PHONE_NUMBER"):
			return self.PHONE_NUMBER
		elif (str(field).upper() == "ACCOUNT_STATUS"):
			return self.ACCOUNT_STATUS
		else:
			raise Exception(f"Invalid field {field}!")

	def set (self, field, value):
		if (str(field).upper() == "FIRST_NAME"):
			self.FIRST_NAME = value
		elif (str(field).upper() == "LAST_NAME"):
			self.LAST_NAME = value
		elif (str(field).upper() == "OTHER_NAMES"):
			self.OTHER_NAMES = value
		elif (str(field).upper() == "BIRTHDAY"):
			self.BIRTHDAY = value
		elif (str(field).upper() == "USERNAME"):
			username = validate.username(value)
			if (not username):
				raise sendFalse(config.getMessage("INVALID_USERNAME"))
			self.USERNAME = username
		elif (str(field).upper() == "PASSWORD"):
			password = validate.password(value)
			if (not password):
				raise sendFalse(config.getMessage("INVALID_PASSWORD"))
			self.PASSWORD = self.encryptPassword(value)
		elif (str(field).upper() == "EMAIL"):
			email = validate.email(value)
			if (not email):
				return sendFalse(config.getMessage("INVALID_EMAIL"))
			self.EMAIL = value
		elif (str(field).upper() == "PHONE_NUMBER"):
			self.PHONE_NUMBER = value
		elif (str(field).upper() == "ACCOUNT_STATUS"):
			self.ACCOUNT_STATUS = value
		else:
			raise Exception(f"Invalid field {field}!")

class Teacher (models.Teacher, AccountMixin, Account):
	classrooms = []
	subjects_teaching = []
	questions = []
	accountType = config.getAccountType("teacher")["name"]
	accountDetails = {
		"subjects_teaching": [],
		"classroom": {}
	}

	def __init__ (self, exists = False, **kwargs):
		self.__exists__ = exists
		kwargs["ACCOUNT_TYPE"] = config.getAccountType("teacher")["name"]
		models.Teacher.__init__(self, **kwargs)
		AccountMixin.__init__(self)
		self.populateClassrooms()
		self.populateSubjectsTeaching()

	def __str__ (self):
		return self.id

	def populateSubjectsTeaching (self):
		printDebug("Not implemented yet!", "Teacher.populateSubjectsTeaching")

	def addClassroom (self, classroom, classroom_profile = None):
		if (not classroom_profile):
			return False

		self.accountDetails["classroom"][classroom.get("id")] = classroom_profile
		self.classrooms.append(classroom)
		self.saveAccountDetails()
		return True

	def addQuestion (self, question):
		if (isinstance(question, Question)):
			self.questions.append(question)

	def addSubjectsTeaching (self, subject):
		if (isinstance(subject, models.Subject)):
			self.subjects_teaching.append(subject)

	def create (self, first_name, last_name, other_names, birthday, email, phone_number, username, password, account_type, **kwargs):
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

		account_details.update(self.accountDetails)
		account_settings.update(self.accountSettings)

		self.set("first_name", first_name)
		self.set("last_name", last_name)
		self.set("last_name", last_name)
		self.set("other_names", other_names)
		self.set("birthday", birthday)
		self.set("email", email)
		self.set("phone_number", phone_number)
		self.set("username", username)
		self.set("password", password)
		self.set("ACCOUNT_STATUS", config.getAccountStatus("ACTIVE")["status"])

		globals.db.session.add(self)
		globals.db.session.commit()

		return Account.create(self, account_details = account_details, account_settings = account_settings)

	def delete (self, first_call = True):
		globals.db.session.delete(self)
		globals.db.session.commit()
		if (first_call):
			return Account.delete(self, False)

	def setAccountStatus (self, account_status):
		self.ACCOUNT_STATUS = account_status

	def get (self, field):
		if (str(field).lower() == "id"):
		    return self.id
		if (str(field).upper() == "FIRST_NAME"):
			return self.FIRST_NAME
		elif (str(field).upper() == "LAST_NAME"):
			return self.LAST_NAME
		elif (str(field).upper() == "OTHER_NAMES"):
			self.OTHER_NAMES
		elif (str(field).upper() == "BIRTHDAY"):
			return self.BIRTHDAY
		elif (str(field).upper() == "USERNAME"):
			return self.USERNAME
		elif (str(field).upper() == "PASSWORD"):
			return self.PASSWORD
		elif (str(field).upper() == "EMAIL"):
			email = validate.email(value)
			if (not email):
				return sendFalse(config.getMessage("INVALID_EMAIL"))
			return self.EMAIL
		elif (str(field).upper() == "PHONE_NUMBER"):
			return self.PHONE_NUMBER
		elif (str(field).upper() == "ACCOUNT_STATUS"):
			return self.ACCOUNT_STATUS
		else:
			raise Exception(f"Invalid field {field}!")

	def set (self, field, value):
		if (str(field).upper() == "FIRST_NAME"):
			self.FIRST_NAME = value
		elif (str(field).upper() == "LAST_NAME"):
			self.LAST_NAME = value
		elif (str(field).upper() == "OTHER_NAMES"):
			self.OTHER_NAMES = value
		elif (str(field).upper() == "BIRTHDAY"):
			self.BIRTHDAY = value
		elif (str(field).upper() == "USERNAME"):
			username = validate.username(value)
			if (not username):
				raise sendFalse(config.getMessage("INVALID_USERNAME"))
			self.USERNAME = username
		elif (str(field).upper() == "PASSWORD"):
			password = validate.password(value)
			if (not password):
				raise sendFalse(config.getMessage("INVALID_PASSWORD"))
			self.PASSWORD = self.encryptPassword(value)
		elif (str(field).upper() == "EMAIL"):
			email = validate.email(value)
			if (not email):
				return sendFalse(config.getMessage("INVALID_EMAIL"))
			self.EMAIL = value
		elif (str(field).upper() == "PHONE_NUMBER"):
			self.PHONE_NUMBER = value
		elif (str(field).upper() == "ACCOUNT_STATUS"):
			self.ACCOUNT_STATUS = value
		else:
			raise Exception(f"Invalid field {field}!")

class Student (models.Student, AccountMixin, Account):
	accountType = config.getAccountType("student")["name"]
	accountDetails = {
		"classroom": {}
	}

	def __init__ (self, exists = False, **kwargs):
		self.__exists__ = exists
		printDebug("Calling student __init__ method", "Student.__init__")
		kwargs["ACCOUNT_TYPE"] = config.getAccountType("student")["name"]
		models.Student.__init__(self, **kwargs)
		AccountMixin.__init__(self)
		self.populateClassrooms()

	def __str__ (self):
		return self.id

	@classmethod
	def calculateAge (cls, birthday):
		return ((datetime.now() - birthday).days) + 1

	def create (self, first_name, last_name, other_names, birthday, email, phone_number, username, password, account_type, classroom = None, department = None, subjects_offered = [], extracurricular_activities = [], **kwargs):
		if (not self.__exists__):
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

			account_details.update(self.accountDetails)
			account_settings.update(self.accountSettings)

			classroom = Classroom(classroom)

			self.set("first_name", first_name)
			self.set("last_name", last_name)
			self.set("last_name", last_name)
			self.set("other_names", other_names)
			self.set("birthday", birthday)
			self.set("email", email)
			self.set("phone_number", phone_number)
			self.set("username", username)
			self.set("password", password)
			if (classroom):
				classroom.addMember(self)
			self.set("department", department)
			self.set("ACCOUNT_STATUS", config.getAccountStatus("ACTIVE")["status"])
			self.AGE = self.calculateAge(birthday)

			globals.db.session.add(self)
			globals.db.session.commit()

			return Account.create(self, account_details = account_details, account_settings = account_settings)

	def delete (self, first_call = True):
		if (self.__exists__):
			for classroom in self.classrooms:
				self.accountDetails["classroom"].remove(classroom)
				classroom.removeMember(self.id)

			globals.db.session.delete(self)
			globals.db.session.commit()
			if (first_call):
				return Account.delete(self, False)

	def setAccountStatus (self, account_status):
		self.ACCOUNT_STATUS = account_status

	def get (self, field):
		if (str(field).lower() == "id"):
		    return self.id
		if (str(field).upper() == "FIRST_NAME"):
			return self.FIRST_NAME
		elif (str(field).upper() == "LAST_NAME"):
			return self.LAST_NAME
		elif (str(field).upper() == "OTHER_NAMES"):
			self.OTHER_NAMES
		elif (str(field).upper() == "AGE"):
			return self.AGE
		elif (str(field).upper() == "BIRTHDAY"):
			return self.BIRTHDAY
		elif (str(field).upper() == "USERNAME"):
			return self.USERNAME
		elif (str(field).upper() == "PASSWORD"):
			return self.PASSWORD
		elif (str(field).upper() == "EMAIL"):
			email = validate.email(value)
			if (not email):
				return sendFalse(config.getMessage("INVALID_EMAIL"))
			return self.EMAIL
		elif (str(field).upper() == "PHONE_NUMBER"):
			return self.PHONE_NUMBER
		elif (str(field).upper() == "ACCOUNT_STATUS"):
			return self.ACCOUNT_STATUS
		elif (str(field).upper() == "DEPARTMENT"):
			return self.DEPARTMENT
		else:
			raise Exception(f"Invalid field {field}!")

	def set (self, field, value):
		if (str(field).upper() == "FIRST_NAME"):
			self.FIRST_NAME = value
		elif (str(field).upper() == "LAST_NAME"):
			self.LAST_NAME = value
		elif (str(field).upper() == "OTHER_NAMES"):
			self.OTHER_NAMES = value
		elif (str(field).upper() == "BIRTHDAY"):
			self.AGE = self.calculateAge(value)
			self.BIRTHDAY = value
		elif (str(field).upper() == "USERNAME"):
			username = validate.username(value)
			if (not username):
				raise sendFalse(config.getMessage("INVALID_USERNAME"))
			self.USERNAME = username
		elif (str(field).upper() == "PASSWORD"):
			password = validate.password(value)
			if (not password):
				raise sendFalse(config.getMessage("INVALID_PASSWORD"))
			self.PASSWORD = self.encryptPassword(value)
		elif (str(field).upper() == "EMAIL"):
			email = validate.email(value)
			if (not email):
				return sendFalse(config.getMessage("INVALID_EMAIL"))
			self.EMAIL = value
		elif (str(field).upper() == "PHONE_NUMBER"):
			self.PHONE_NUMBER = value
		elif (str(field).upper() == "DEPARTMENT"):
			self.DEPARTMENT = value
		elif (str(field).upper() == "ACCOUNT_STATUS"):
			self.ACCOUNT_STATUS = value
		else:
			raise Exception(f"Invalid field {field}!")