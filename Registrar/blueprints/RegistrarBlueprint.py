from flask import Blueprint
from flask import globals
from flask_login import login_required, current_user
from flask import render_template
from flask import redirect
from flask import session
from flask import url_for

registrar = Blueprint("registrar", __name__)

@login_required
@registrar.route("/")
def registrarIndexPage ():
    return globals.methods.renderUserAccountHomePage()

@registrar.route("/configuration")
@login_required
def registrarConfigurationPage ():
    return render_template(
		"config.html",
		title = "IT Questions Registrar",
		student_titles = globals.model.Student_titles,
		grading_system = globals.grading_system.selectAll()["rows"],
		school_departments = globals.school_departments.selectAll()["rows"]
	)
