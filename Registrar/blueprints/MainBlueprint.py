from flask import Blueprint
from flask import globals
from flask import render_template
from flask import redirect
from flask import url_for

from ..controllers.config import config

import os

main = Blueprint("main", __name__)

@main.route("/")
def homeView ():
    # return "The server has not been configured. Please contact the technical administrator in order to configure it"

	# if not config["is_configured"]:
	# 	return redirect(url_for("registrar.registrarConfigurationPage"))
	return render_template("home.html", title = "Home")

@main.route("/about")
def aboutView ():
	return render_template("about.html")

@main.route("/contact")
def contactView ():
	return render_template("contact.html")

@main.route("/faq")
def faqView ():
	return render_template("faq.html")