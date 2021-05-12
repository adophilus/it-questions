from flask import Blueprint
from flask import globals
from flask_login import current_user, login_required
from flask import redirect
from flask import session
from flask import url_for

parent = Blueprint("parent", __name__)

@parent.route("/")
@login_required
def homeView ():
	account = Account(_object = current_user)
	if (not account.isParent()):
		return redirect(f"/{account.get('ACCOUNT_TYPE')}")

	return globals.methods.renderUserAccountHomePage()

@parent.route("/<id>")
@login_required
def lookupParentByIdPage (id):
	return sendFalse("not implemented yet!")