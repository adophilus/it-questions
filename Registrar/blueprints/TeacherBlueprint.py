from flask import Blueprint
from flask import globals
from flask import redirect
from flask import url_for
from flask_login import current_user, login_required

teacher = Blueprint("teacher", __name__)

@teacher.route("/")
@login_required
def teacherIndexPage ():
	account = Account(_object = current_user)
	if (not account.isTeacher()):
		return redirect(f"/{account.get('ACCOUNT_TYPE')}")

	return globals.methods.renderUserAccountHomePage()

@teacher.route("/<id>")
@login_required
def lookupTeacherByIdPage (id):
    return sendFalse("not implemented yet!")