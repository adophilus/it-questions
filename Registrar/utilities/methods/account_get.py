from flask import globals
from flask_login import current_user
import os

def _getAccountById (id):
    user = globals.Administrator.query.filter_by(id = id)

    if (user.first()):
        return user

    user = globals.Parent.query.filter_by(id = id)

    if (user.first()):
        return user

    user = globals.Teacher.query.filter_by(id = id)

    if (user.first()):
        return user

    user = globals.Student.query.filter_by(id = id)

    if (user.first()):
        return user

def _getAccountByEmail (email):
    user = globals.Administrator.query.filter_by(EMAIL = email)

    if (user.first()):
        return user

    user = globals.Parent.query.filter_by(EMAIL = email)

    if (user.first()):
        return user

    user = globals.Teacher.query.filter_by(EMAIL = email)

    if (user.first()):
        return user

    user = globals.Student.query.filter_by(EMAIL = email)

    if (user.first()):
        return user

def getAccountByEmail (email):
    account = _getAccountByEmail(email)
    if (account):
        return account.first()

def getAccountById (id):
    account = _getAccountById(id)
    if (account):
        return account.first()

def _getAccountByUsername (username):
    user = globals.Administrator.query.filter_by(USERNAME = username)

    if (user.first()):
        return user

    user = globals.Parent.query.filter_by(USERNAME = username)

    if (user.first()):
        return user

    user = globals.Teacher.query.filter_by(USERNAME = username)

    if (user.first()):
        return user

    user = globals.Student.query.filter_by(USERNAME = username)

    if (user.first()):
        return user

def getAccountDetails (account_id, account = None):
    if not (account):
        account = getAccountById(account_id)
    
    if not (account):
        return False
    
    account_id = account.id
    try:
        account_details = globals.General.loadJson(_getAccountDetailsPath(account.ACCOUNT_TYPE, account_id))
        return account_details
    except Exception as e:
        return None

def _getAccountDetailsPath (account_type, account_id):
    return os.path.join("data", f"{account_type}s", account_id, "details.json")

def getAccountDetailsPath (account_id):
    account = getAccountById(account_id)
    if (account):
        return _getAccountDetailsPath(account.ACCOUNT_TYPE, account_id)

def getAccountSettings (account_id):
    account = getAccountById(account_id)
    if (account):
        account_settings = globals.General.loadJson(os.path.join("data", f"{account.ACCOUNT_TYPE}s", account_id, "settings.json"))
        return account_settings
    return None


def getAccountSettingsPath (account_id):
    account = getAccountById(account_id)
    if (account):
        return os.path.join("data", account.ACCOUNT_TYPE, account.id, "settings.json")

def getAccountByUsername (username):
    account = _getAccountByUsername(username)
    if (account):
        return account.first()

def getAccountBySession ():
    return getAccountById(current_user.id)

def getSchoolSubjectsList ():
    school_subjects = globals.SchoolSubjects.query.all()
    return school_subjects


def lookupParentById (id):
    account = getAccountById(id)
    if (account and account.ACCOUNT_TYPE == "parent"):
        return account

def lookupTeacherById (id):
    account = getAccountById(id)
    if (account and account.ACCOUNT_TYPE == "teacher"):
        return account

def lookupStudentById (id):
    account = getAccountById(id)
    if (account and account.ACCOUNT_TYPE == "student"):
        return account

def lookupAdministratorById (id):
    account = getAccountById(id)
    if (account and account.ACCOUNT_TYPE == "administrator"):
        return account

def determineAccountStatus ():
    if (globals.config["security"]["ALLOW_REMOTE_ACCOUNT_VALIDATION"] == True):
        return globals.config["account"]["statuses"]["ACTIVE"]["status"]
    else:
        return globals.config["account"]["statuses"]["AWAITING_VERIFICATION"]["status"]

def getAccountStatus (account):
    status = globals.config["statuses"][account.ACCOUNT_STATUS]["status"]
    return status

def getAccountPath (user_id, account_type, verified = True):
    if not (verified):
        account = getAccountById(user_id)
        if not (account):
            return None
    return os.path.join("data", f"{account_type}s", user_id)