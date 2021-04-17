from flask import globals

def updateAccountsDB (user, **update):
	user.update(update)
	globals.db.session.commit()

def addNewUserToDB (username, password, account_details, commit = False):

	if (account_details["account_type"] == globals.PARENT["name"]):
		userAccount = globals.Parent(
			id = account_details["identity"],
			FIRST_NAME = account_details["first_name"],
			LAST_NAME = account_details["last_name"],
			OTHER_NAMES = account_details["other_names"],
			USERNAME = username,
			PASSWORD = password,
			EMAIL = account_details["email"],
			WARDS = globals.General.unjsonize(account_details["wards"]),
			PHONE_NUMBER = account_details["phone_number"],
			ACCOUNT_TYPE = account_details["account_type"],
			BIRTHDAY = account_details["birthday"],
			ACCOUNT_STATUS = account_details["status"]
		)
		globals.db.session.add(userAccount)
	elif (account_details["account_type"] == globals.TEACHER["name"]):
		userAccount = globals.Teacher(
			id = account_details["identity"],
			FIRST_NAME = account_details["first_name"],
			LAST_NAME = account_details["last_name"],
			OTHER_NAMES = account_details["other_names"],
			USERNAME = username,
			PASSWORD = password,
			EMAIL = account_details["email"],
			PHONE_NUMBER = account_details["phone_number"],
			ACCOUNT_TYPE = account_details["account_type"],
			BIRTHDAY = account_details["birthday"],
			ACCOUNT_STATUS = account_details["status"]
		)
		globals.db.session.add(userAccount)
	elif (account_details["account_type"] == globals.STUDENT["name"]):
		userAccount = globals.Student(
			id = account_details["identity"],
			FIRST_NAME = account_details["first_name"],
			LAST_NAME = account_details["last_name"],
			OTHER_NAMES = account_details["other_names"],
			AGE = account_details["age"],
			USERNAME = username,
			PASSWORD = password,
			BIRTHDAY = account_details["birthday"],
			EMAIL = account_details["email"],
			PHONE_NUMBER = account_details["phone_number"],
			ACCOUNT_TYPE = account_details["account_type"],
			DEPARTMENT = account_details["department"],
			ACCOUNT_STATUS = account_details["status"]
		)
		globals.db.session.add(userAccount)

	if (commit):
		globals.db.session.commit()
	try:
		return userAccount
	except Exception as e:
		return False

def removeUserAccountFromDB (account, commit = False):
	if (account):
		globals.db.session.delete(account)

		if (commit):
			globals.db.session.commit()
