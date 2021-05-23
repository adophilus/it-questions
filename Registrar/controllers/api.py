from . import Account, validate
from .config import config
from .methods import printDebug, sendFalse, sendTrue

def createQuestion (*args, **kwargs):
	return sendFalse("not implemented yet!")

def createUserAccount (first_name, last_name, other_names, birthday, email, phone_number, username, password, account_type, classroom = None, department = None, subjects_offered = [], extracurricular_activities = [], subjects_teaching = [], ward_id = None):

	if (Account(username = username)):
		return sendFalse(config.getMessage("EXISTENT_USERNAME"))

	if (Account(email = email)):
		return sendFalse(config.getMessage("EXISTENT_EMAIL"))

	if ((not validate.username(username))):
		return sendFalse(config.getMessage("INVALID_USERNAME"))

	if ((not validate.email(email))):
		return sendFalse(config.getMessage("INVALID_EMAIL"))

	if (not validate.names(first_name, last_name)):
		return sendFalse(config.getMessage("INVALID_NAME"))

	if (not validate.password(password)):
		return sendFalse(config.getMessage("INVALID_PASSWORD"))

	birthday = validate.birthday(birthday)
	if (not birthday):
		return sendFalse(config.getMessage("INVALID_BIRTHDAY"))

	account = Account(account_type = account_type)

	is_created = account.create(None, None, first_name, last_name, other_names, birthday, email, phone_number, username, password, account_type, classroom = classroom, department = department, subjects_offered = subjects_offered, extracurricular_activities = extracurricular_activities, subjects_teaching = subjects_teaching, ward_id = ward_id)

	if (not is_created):
		return is_created

	return sendTrue(config.getMessage("SUCCESSFUL_ACCOUNT_CREATION"))