from flask_login import current_user
from ..models import Administrator, Parent, Teacher, Student

class Client ():
    def isAdmin ():
        if not (current_user.is_active):
            return False

        return (current_user.ACCOUNT_TYPE == config.getAccountType("administrator")["name"])

    def isParent ():
        if not (current_user.is_active):
            return False

        return (current_user.ACCOUNT_TYPE == config.getAccountType("parent")["name"])

    def isTeacher ():
        if not (current_user.is_active):
            return False

        return (current_user.ACCOUNT_TYPE == config.getAccountType("teacher")["name"])

    def isStudent ():
        if not (current_user.is_active):
            return False

        return (current_user.ACCOUNT_TYPE == config.getAccountType("student")["name"])

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
            return (decryptPassword(Client._getPassword()) == password)
