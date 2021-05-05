import re

def email (email):
	if (len(email) < 0):
		return False

	if (re.search(r"[\d\w]+@[\w\d]+\.[\w\d]", email)):
		return True

def names (first_name, last_name):
	return first_name.strip() and last_name.strip()

def password (password):
	if (len(password) < 5):
		return False

	if not (re.search(r"\d", password)):
		return False

	return True

def username (username):
	if (len(username) < 5):
		return False

	if not (re.search(r"\w", username)):
		return False

	if (re.search(r"\\|#|\(|\)|'|\"|;|:|,|/|\?|~|`", username)):
		return False

	return True