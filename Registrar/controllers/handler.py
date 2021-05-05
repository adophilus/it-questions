from . import Account, validate
from .config import config
from .methods import sendFalse

def createQuestion (*args, **kwargs):
	return sendFalse("not implemented yet!")

def createUserAccount (first_name, last_name, other_names, birthday, email, phone_number, username, password, account_type, classroom = None, department = None, subjects_offered = [], extracurricular_activities = [], subjects_teaching = [], ward_id = None):
	if (Account(username = username) or Account(email = email)):
		return sendFalse(config.getMessage("EXISTENT_EMAIL_USERNAME"))

	if ((not validate.email(email)) or (not validate.username(username))):
		return sendFalse(config.getMessage("INVALID_EMAIL_USERNAME"))

	if (not validate.names(first_name, last_name)):
		return sendFalse(config.getMessage("INVALID_NAME"))

	if (not validate.password(password)):
		return sendFalse(config.getMessage("INVALID_PASSWORD"))

	account = Account()

	# account.create()
	return str(account)
	return sendFalse("not implemented yet!")