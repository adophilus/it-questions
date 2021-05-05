from flask import Blueprint
from flask import globals
from flask import render_template
from flask import redirect
from flask import session
from flask import url_for

from ..controllers.config import config

import os

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def mainIndexPage ():
    # return "The server has not been configured. Please contact the technical administrator in order to configure it"

	# if not config["is_configured"]:
	# 	return redirect(url_for("registrar.registrarConfigurationPage"))
	return render_template("home.html", title = "Home")

@main.route("/login")
@main.route("/signin")
@main.route("/sign-in")
def mainLoginPage ():
	return render_template("login.html")

@main.route("/logout")
@main.route("/signout")
@main.route("/sign-out")
def mainLogoutPage ():
	return redirect(url_for("handler.handleLogout"))

@main.route("/about")
def mainAboutPage ():
	return render_template("about.html")

@main.route("/contact")
def mainContactPage ():
	return render_template("contact.html")

@main.route("/faq")
def mainFaqPage ():
	return render_template("faq.html")

@main.route("/signup")
@main.route("/register")
def mainSignupPage ():
	if (config["security"]["ALLOW_REMOTE_ACCOUNT_CREATION"]):
		return render_template("signup.html", url_for = url_for)
	else:
		return redirect(url_for("main.mainLoginPage"))

def mainAccountHomePage ():
	pass