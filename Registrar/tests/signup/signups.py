from ...controllers.account import Account
from ...controllers.methods import printDebug

def signupTeacher (accountUsername = "teacher"):
	ac = Account(username = accountUsername)
	ac2 = Account.getById(id = "mvwDNo8qFcmlc7tIGlgq8GeOV")
	printDebug(f"ac.__bool__(): {ac.__bool__()}")
	printDebug(f"ac2.__bool__(): {ac2.__bool__()}")