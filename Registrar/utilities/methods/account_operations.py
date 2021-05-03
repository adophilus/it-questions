from datetime import datetime, date
from flask import globals
from flask_login import logout_user
from flask_sqlalchemy import sqlalchemy

import shutil

from .account_auth import *
from .account_gen import *
from .account_get import *
from .account_put import *
# from .chatroom_get import *
from .classroom_get import *

def calculateUserAge (birthDate):
	today = date.today()
	age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
	return age

def removeUserAccount (user_id):

def createUserAccount (first_name, last_name, other_names, birthday, email, phone_number, username, password, account_type, classroom = "", department = "", subjects_offered = [], extracurricular_activities = [], subjects_teaching = [], ward_id = ""): # ward_first_name = "", ward_last_name = "", ward_other_names = "", ward_classroom = ""):
	first_name = first_name.strip()
	last_name = last_name.strip()
	other_names = other_names.strip()
	birthday = birthday.strip()
	email = email.strip()
	phone_number = phone_number.strip()
	classroom = classroom.strip()
	department = department.strip()
	ward_id = ward_id.strip()
	# ward_first_name = ward_first_name.strip()
	# ward_last_name = ward_last_name.strip()
	# ward_other_names = ward_other_names.strip()
	# ward_classroom = ward_classroom.strip()

	if (not account_type in globals.config["account"]["types"]):
		return globals.General.unjsonize({"data": config.getMessage("INVALID_ACCOUNT_TYPE"), "status": False})

	if (not globals.methods.Validate.username(username)):
		return globals.General.sendFalse(config.getMessage("INVALID_USERNAME"))

	if (not globals.methods.Validate.password(password)):
		return globals.General.sendFalse(config.getMessage("INVALID_PASSWORD"))

	if (not globals.methods.Validate.email(email)):
		return globals.General.sendFalse(config.getMessage("INVALID_EMAIL"))

	if ((account_type == globals.config["account"]["types"]["student"]["name"] and (not getClassroomByName(classroom))) or (account_type == globals.config["account"]["types"]["parent"]["name"] and (not getClassroomByName(ward_classroom)))):
		return globals.General.sendFalse(config.getMessage("INEXISTENT_CLASS"))

	if (getAccountByUsername(username)):
		return globals.General.sendFalse(config.getMessage("EXISTENT_ACCOUNT"))

	if (getAccountByEmail(email)):
		return globals.General.sendFalse(config.getMessage("EXISTENT_EMAIL"))

	if not (account_type in globals.config["account"]["types"]):
		return globals.General.sendFalse(config.getMessage("INVALID_ACCOUNT_TYPE"))

	if (len(first_name) == 0 or len(last_name) == 0):
		return globals.General.sendFalse(config.getMessage("INVALID_NAME"))

	# Generate a unique ID for the user
	id = generateUserId(unique = True)
	account_path = os.path.join("data", f"{account_type}s", id)

	# Hash the user's password
	password = globals.methods.encryptPassword(password)

	# Format the user's birthday and set age
	try:
		birthday = datetime.strptime(birthday, "%d/%m/%Y").strftime("%Y-%m-%d")
		birthday = datetime.strptime(birthday, "%Y-%m-%d")
		age = calculateUserAge(birthday)
	except Exception:
		return globals.General.sendFalse(config.getMessage("INVALID_BIRTHDAY"))

	account_details = account_settings = {}

	account_details = {
		"age": age,
		"identity": id,
		"unread_messages": 0,
		"unread_notifications": 0,
		"first_name": first_name,
		"last_name": last_name,
		"other_names": other_names,
		"birthday": birthday,
		"email": email,
		"phone_number": phone_number,
		"account_type": account_type
	}

	if (account_type == "student"):
		_classroom = getClassroomByName(classroom)[0]
		if not (_classroom):
			return globals.General.sendFalse(config.getMessage("INEXISTENT_CLASS"))

		account_details.update({
			# define miscellaneous fields for students
			"height": "unknown",
			"weight": "unknown",
			"complexion": "unknown",
			"eye_color": "unknown",
			"subjects_offerred": [subject.strip() for subject in subjects_offered.split(",")],
			"department": department,
			"extracurricular_activities": extracurricular_activities,
			"guardian": {},
			"classroom": {},
			"unread_public_remarks": 0
		})
	elif (account_type == "parent"):
		# if (len(ward_first_name) == 0 or len(ward_last_name) == 0):
		# 	return globals.General.sendFalse(config.getMessage("INVALID_WARD_NAME"))

		# _classroom = getClassroomByName(ward_classroom)
		# if not (_classroom):
		# 	return globals.General.sendFalse(config.getMessage("INEXISTENT_CLASS"))
		ward = Account(ward_id)
		if (ward):
			account_details["ward"] = globals.methods.addWardToGuardian(ward, None, account_details)

	elif (account_type == "teacher"):
		account_details.update({
			"is_homeroom_teacher": False,
			"questions": [],
			"subjects_teaching": subjects_teaching,
			"classroom": {}
		})
	elif (account_type == "administrator"):
		account_details["questions"] = []

	# Determine the account status of the account
	account_details["status"] = determineAccountStatus()

	# Create the user account directory
	createUserAccountDirectory(account_path)

	userAccount = globals.methods.addNewUserToDB(username, password, account_details)
	if (not userAccount):
		return globals.General.sendFalse(config.getMessage("ERROR_OCCURRED"))

	if (account_type == "student"):
		classroom_profile = globals.methods.addUserToClassroom(userAccount, _classroom)
		print("\n" * 3)
		print(classroom_profile)
		print("\n" * 3)
		if (classroom_profile == None):
			return globals.General.sendFalse(config.getMessage("ERROR_OCCURRED") + "cprof")
		elif (classroom_profile == False):
			return globals.General.sendFalse(config.getMessage("ERROR_OCCURRED") + "cprofN")
		account_details["classroom"].update(classroom_profile)

		createUserAccountPublicRemarksFile(account_path)

	createUserAccountDetailsFile(account_details, account_path)
	createUserAccountSettingsFile(account_settings, account_path)
	createUserAccountNotificationsFile(account_path)

	globals.db.session.commit()
	return globals.General.sendTrue(config.getMessage("SUCCESSFUL_ACCOUNT_CREATION"))

def removeUserAccountDirectory (user_id, account_type):
	account_path = getAccountPath(user_id, account_type)
	if not (account_path):
		return False
	shutil.rmtree(account_path)
	return True

# def _removeUserFromChatroom (user_id, chatroom_id):
# 	chatroom = getChatroomById(chatroom_id)
# 	if (chatroom):
# 		chatroom_members = globals.General.jsonize(chatroom.MEMBERS)

# 		if (user_id in chatroom_members):
# 			chatroom_members.remove(user_id)
# 			chatroom.MEMBERS = globals.General.json.dumps(chatroom_members)

# 			if (commit):
# 				globals.db.session.commit()

# def removeUserAccountFromChatrooms (account, account_details, commit = False):
# 	if (account):
# 		user_id = account.get("id")

# 		chatroom_ids = account_details["chatrooms"]

# 		for chatroom_id in chatroom_ids:
# 			_removeUserFromChatroom(user_id, chatroom_id)

# 		if (commit):
# 			globals.db.session.commit()

def removeUserAccountPublicRemarksFile (id, account_path):
	if (os.path.isfile("public_remarks.csv")):
		os.unlink(os.path.join(account_path, "public_remarks.csv"))
		print(f"[{id}] Removing \"public_remarks.csv\" file...")
	else:
		print(f"[{id}] File \"public_remarks.csv\" has already been deleted.")

def removeUserAccountDetailsFile (id, account_path):
	rmpath = os.path.join(account_path, "details.json")
	if (os.path.isfile(rmpath)):
		os.unlink(rmpath)
		print(f"[{id}] Removing \"details.json\" file...")
	else:
		print(f"[{id}] File \"details.json\" has already been deleted.")

def removeUserAccountSettingsFile (id, account_path):
	rmpath = os.path.join(account_path, "settings.json")
	if (os.path.isfile(rmpath)):
		os.unlink(rmpath)
		print(f"[{id}] Removing \"settings.json\" file...")
	else:
		print(f"[{id}] File \"settings.json\" has already been deleted.")

def removeUserAccountNotificationsFile (id, account_path):
	rmpath = os.path.join(account_path, "notifications.csv")
	if (os.path.isfile(rmpath)):
		os.unlink(rmpath)
		print(f"[{id}] Removing \"notifications.csv\" file...")
	else:
		print(f"[{id}] File \"notifications.csv\" has already been deleted.")

def createUserAccountDirectory (account_path):
	os.mkdir(account_path)

def createUserAccountDetailsFile (account_details, account_path):
	details = {**account_details}
	details["birthday"] = details["birthday"].strftime("%Y-%m-%d")
	globals.General.putContentIn(
		os.path.join(
			account_path,
			"details.json"
		),
		globals.General.unjsonize(
			details
		)
	)

def createUserAccountSettingsFile (account_settings, account_path):
	settings = {
		"theme": "default",# hard-coded (for lack of an alternative theme)
		"last_login": "",# f"{globals.clock.date()} {globals.clock.time()}"
		"login_history": {},# history of previous login attempts
		"secret_question": "",# a secret question for logging into the account (in the case of "forgotten password")
		"secret_question_answer": "",# the answer to the secret question
		"enable_secret_question": ""# determines whether the secret question will be enaled or not
	}

	settings.update(account_settings)
	globals.General.putContentIn(
		os.path.join(
			account_path,
			"settings.json"
		),
		globals.General.unjsonize(
			settings
		)
	)

def createUserAccountNotificationsFile (account_path):
	globals.General.putContentIn(os.path.join(account_path, "notifications.csv"), "")

def createUserAccountPublicRemarksFile (account_path):
	globals.General.putContentIn(os.path.join(account_path, "public_remarks.csv"), "")

def isCurrentAccount (account_id):
	if account_id == current_user.id:
		return True

def changePassword (user, old_password, new_password):
	if (globals.methods.Client.hasPassword(new_password)):
		return globals.General.sendFalse(config.getMessage("CANNOT_REPEAT_OLD_PASSWORD"))

	new_password = globals.methods.encryptPassword(new_password)
	user.PASSWORD = new_password
	globals.db.session.commit()
	# return globals.General.sendTrue(config.getMessage("PASSWORD_CHANGE_SUCCESSFUL"))
	return False