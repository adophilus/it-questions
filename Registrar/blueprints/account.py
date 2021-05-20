from flask import Blueprint
from flask import globals
from flask import render_template
from flask import redirect
from flask import session
from flask import url_for

from ..controllers.config import config

import os

account = Blueprint("account", __name__)

@account.route("/login")
def loginView ():
	return render_template("account/login.html")

@account.route("/logout")
def logoutView ():
	return redirect(url_for("handler.handleLogout"))

@account.route("/signup")
@account.route("/register")
def signupView ():
	if (config["security"]["ALLOW_REMOTE_ACCOUNT_CREATION"]):
		return render_template("account/signup.html", url_for = url_for)
	else:
		return redirect(url_for("account.loginView"))
