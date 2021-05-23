from flask import Blueprint
from flask import globals
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import current_user, login_required

from ..controllers.account import Account
from ..controllers.methods import sendFalse

questionsManager = Blueprint("questionsManager", __name__)

@questionsManager.route("/")
@login_required
def homeView ():
	account = Account(_object = current_user)
	if not (current_user.isAdmin() or current_user.isTeacher()):
		return redirect(url_for(f"{account.accountType}.homeView"))

	return render_template(f"{account.accountType}/questions-manager.html", account = account, url_for = url_for)
