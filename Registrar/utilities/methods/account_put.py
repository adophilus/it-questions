from flask import globals
from .account_get import *

def _getAccountDetailsPath (account_type, account_id):
	return os.path.join("data", f"{account_type}s", account_id, "details.json")

def putAccountDetails (account_id, account_details, account = None):
	if not (account):
		account = Account(account_id)
	if not (account):
		return False
	account_id = account.get("id")
	try:
		globals.General.saveJson(_getAccountDetailsPath(account.ACCOUNT_TYPE, account_id), account_details)
		return True
	except Exception as e:
		return e
