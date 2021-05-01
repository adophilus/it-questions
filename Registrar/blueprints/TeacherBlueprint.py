from flask import Blueprint
from flask import globals
from flask import redirect
from flask import url_for
from flask_login import current_user, login_required

teacher = Blueprint("teacher", __name__)

@teacher.route("/")
@login_required
def teacherIndexPage ():
	if current_user.ACCOUNT_TYPE != globals.config["account"]["types"]["teacher"]["name"]:
		return globals.methods.redirectUserToHomePage()

	return globals.methods.renderUserAccountHomePage()

@teacher.route("/<id>")
@login_required
def lookupTeacherByIdPage (id):
    return globals.methods.renderAccountPageOf(id, globals.model.Teacher["name"])