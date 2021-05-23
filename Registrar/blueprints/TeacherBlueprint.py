from flask import Blueprint
from flask import globals
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import current_user, login_required

from ..controllers import calendar
from ..controllers.account import Account
from ..controllers.methods import sendFalse, sendTrue

teacher = Blueprint("teacher", __name__)

@teacher.route("/")
@login_required
def homeView ():
	account = Account(_object = current_user)
	if (not account.isTeacher()):
		return redirect(f"/{account.get('ACCOUNT_TYPE')}")

	return render_template(f"{account.accountType}/home.html", account = account, url_for = url_for, date_and_time = calendar.getDateTime(), weeks = calendar.getCalendarArray(), no_of_unread_notifications = 0)

@teacher.route("/<id>")
@login_required
def lookupTeacherByIdPage (id):
    return sendFalse("not implemented yet!")