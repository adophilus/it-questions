from flask import globals

from .config import config
from .methods import fernetEncrypt, fernetDecrypt
from .private_key_generator import PrivateKeyGenerator
from .. import models

import shutil

class Account ():
	__exists__ = False
	generator = PrivateKeyGenerator()

	def __init__ (self, id = None, username = None, email = None, account_type = config.getAccount("student")["name"]):
		if (email):
			self.__determineAccountType(email = email, account_type = account_type)
		elif (username):
			self.__determineAccountType(username = username, account_type = account_type)
		else:
			self.__determineAccountType(id, account_type = account_type)

	def __bool__ (self):
		return self.__exists__

	def __determineAccountType (self, id = None, username = None, email = None):
		if (email):
			administrator = models.Administrator.getByEmail(email)
			parent = models.Parent.getByEmail(email)
			teacher = models.Teacher.getByEmail(email)
			student = models.Student.getByEmail(email)
		elif (username):
			administrator = models.Administrator.getByUsername(username)
			parent = models.Parent.getByUsername(username)
			teacher = models.Teacher.getByUsername(username)
			student = models.Student.getByUsername(username)
		else:
			administrator = models.Administrator.getById(id)
			parent = models.Parent.getById(id)
			teacher = models.Teacher.getById(id)
			student = models.Student.getById(id)

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
				self.account = Administrator(id = self.__generateId__())
			elif (account_type == config.getAccount("parent")["name"]):
				self.account = Parent(id = self.__generateId__())
			elif (account_type == config.getAccount("teacher")["name"]):
				self.account = Teacher(id = self.__generateId__())
			else:
				self.account = Student(id = self.__generateId__())

	@classmethod
	def __generateId__ (cls, unique = True):
		while True:
			id = cls.generator.generate(level = config["id_length"]["account"])

			if (unique):
				account = Account(id)

				if not (account):
					return id

	@classmethod
	def encryptPassword (cls, password):
		return fernetEncrypt(password, key = config["ENCRYPTION_KEY"].encode("UTF-8")).decode("UTF-8")

	@classmethod
	def decryptPassword (cls, password):
		return fernetDecrypt(password, key = config["ENCRYPTION_KEY"].encode("UTF-8")).decode("UTF-8")

	@classmethod
	def getByEmail (cls, email):
		return self.account.getByEmail(email)

	@classmethod
	def getById (cls, id):
		return self.account.getById(id)

	@classmethod
	def getByUsername (cls, username):
		return self.account.getByUsername(username)

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

	def create (self):
		if (not self.__exists__):
			globals.db.session.add(self.account)
			globals.db.session.commit()
			return True

	def delete (self):
		if (self.__exists__):
			for classroom in account_details["classroom"]:
				globals.methods.removeUserAccountFromClassroom(account, classroom["id"])

			shutil.rmtree(user_id, account_type)
			self.classrooms.removeMember(self.id)

			globals.db.session.delete(self.account)
			globals.db.session.commit()
			self.__exists__ = False
			return True

class Administrator (Account):
	pass

class Parent (Account):
	pass

class Teacher (Account):
	pass

class Student (Account):
	pass