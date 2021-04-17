from flask import globals
from flask_login import current_user, login_user
from .account_get import *
from .account_operations import *
from hashlib import md5

import re
import os

def encryptPassword (password):
    return globals.General.fernetEncrypt(password, key = globals.config["ENCRYPTION_KEY"].encode("UTF-8")).decode("UTF-8")

def decryptPassword (password):
    return globals.General.fernetDecrypt(password, key = globals.config["ENCRYPTION_KEY"].encode("UTF-8")).decode("UTF-8")

class Client ():
    def isAdmin ():
        if not (current_user.is_active):
            return False

        return (current_user.ACCOUNT_TYPE == globals.ADMINISTRATOR["name"])

    def isParent ():
        if not (current_user.is_active):
            return False

        return (current_user.ACCOUNT_TYPE == globals.PARENT["name"])

    def isTeacher ():
        if not (current_user.is_active):
            return False

        return (current_user.ACCOUNT_TYPE == globals.TEACHER["name"])

    def isStudent ():
        if not (current_user.is_active):
            return False

        return (current_user.ACCOUNT_TYPE == globals.STUDENT["name"])

    def isVisitor ():
        if not (Client.isAdmin() or Client.isParent() or Client.isTeacher() or Client.isStudent()):
            return True

    def _getUsername ():
        return current_user.USERNAME

    def getUsername ():
        if not (Client.isVisitor()):
            return Client._getUsername()

    def _getId ():
        return current_user.id

    def getId ():
        if not (Client.isVisitor()):
            return Client._getId()

    def _getPassword ():
        return current_user.PASSWORD

    def getPassword ():
        if not (Client.isVisitor()):
            return Client._getPassword()

    def getUserId ():
        if not (Client.isVisitor()):
            return current_user.id

    def hasPassword (password):
        if not (Client.isVisitor()):
            # print("=============")
            # print(Client._getPassword())
            # print(decryptPassword(Client._getPassword()))
            # print(password)
            # print("=============")
            return (decryptPassword(Client._getPassword()) == password)

class Verify ():
    def administrator (username, password):
        user = getAccountByUsername(username)
        if (user):
            password = str(password)
            if (decryptPassword(user.PASSWORD) == password):
                return user

    def parent (username, password):
        user = getAccountByUsername(username)
        if (user):
            password = str(password)
            if (decryptPassword(user.PASSWORD) == password):
                return user

    def teacher (username, password):
        user = getAccountByUsername(username)
        if (user):
            password = str(password)
            if (decryptPassword(user.PASSWORD) == password):
                return user

    def student (username, password):
        user = getAccountByUsername(username)
        if (user):
            password = str(password)
            if (decryptPassword(user.PASSWORD) == password):
                return user

    def credentials (username, password):
        administrator = Verify.administrator(username, password)
        if (administrator):
            return administrator

        parent = Verify.parent(username, password)
        if (parent):
            return parent

        teacher = Verify.teacher(username, password)
        if (teacher):
            return teacher

        student = Verify.student(username, password)
        if (student):
            return student

    def isAllowedEntry (account_status):
        allow_access = globals.config["account"]["statuses"][account_status].get("grant_access")
        return allow_access

class Validate ():
    def username (username):
        if (len(username) < 5):
            return False

        if not (re.search(r"\w", username)):
            return False

        if (re.search(r"\\|#|\(|\)|'|\"|;|:|,|/|\?|~|`", username)):
            return False

        return True

    def password (password):
        if (len(password) < 5):
            return False

        if not (re.search(r"\d", password)):
            return False

        return True

    def email (email):
        if (len(email) < 0):
            return False

        if (re.search(r"[\d\w]+@[\w\d]+\.[\w\d]", email)):
            return True


def loginUser (username, password):

    # if not Validate.username(username):
    #     return globals.General.sendFalse(globals.config.getMessage("INVALID_USERNAME"))

    # if not Validate.password(password):
    #     return globals.General.sendFalse(globals.config.getMessage("INVALID_PASSWORD"))

    if not Verify.credentials(username, password):
        return globals.General.sendFalse(globals.config.getMessage("INVALID_CREDENTIALS"))

    account = getAccountByUsername(username)

    if (account):
        account_details = getAccountDetails(account.id)

        if (account_details == None):
            return globals.General.sendFalse(globals.config.getMessage("UNSUCCESSFUL_SIGNIN"))

        if not (Verify.isAllowedEntry(account_details["status"])):
            return globals.General.sendFalse(globals.config.getMessage("ACCESS_DENIED_PAGE"))

        if (login_user(account)):
            return globals.General.unjsonize({"status": True, "ACCOUNT_TYPE": account.ACCOUNT_TYPE, "data": globals.config.getMessage("SUCCESSFUL_SIGNIN")})
        else:
            return globals.General.sendFalse(globals.config.getMessage("INEXISTENT_ACCOUNT"))

    return globals.General.sendFalse(globals.config.getMessage("INEXISTENT_ACCOUNT"))
