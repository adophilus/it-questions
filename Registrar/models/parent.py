from flask import globals
from flask_login import UserMixin

from ..controllers.config import config
from .account_mixin import AccountMixin

class Parent (UserMixin, globals.db.Model, AccountMixin):
    id = globals.db.Column(globals.db.Text, primary_key = True)
    FIRST_NAME = globals.db.Column(globals.db.Text)
    LAST_NAME = globals.db.Column(globals.db.Text)
    OTHER_NAMES = globals.db.Column(globals.db.Text)
    USERNAME = globals.db.Column(globals.db.Text)
    PASSWORD = globals.db.Column(globals.db.Text)
    EMAIL = globals.db.Column(globals.db.Text)
    PHONE_NUMBER = globals.db.Column(globals.db.Text)
    BIRTHDAY = globals.db.Column(globals.db.Date)
    WARDS = globals.db.Column(globals.db.Text, default = "[]")
    ACCOUNT_TYPE = globals.db.Column(globals.db.Text, default = config.getAccountType("parent")["name"])
    ACCOUNT_STATUS = globals.db.Column(globals.db.Text, default = config.getAccountStatus("ACTIVE"))