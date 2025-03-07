from flask import Blueprint
from flask import globals
from flask import redirect
from flask import url_for
from flask_login import current_user, login_required

from ..controllers.methods import sendFalse

admin = Blueprint("administrator", __name__)

@admin.route("/")
@login_required
def homeView ():
	if not globals.methods.Client.isAdmin():
		return globals.methods.renderUserAccountHomePage()

	return globals.methods.renderUserAccountHomePage()

@admin.route("/<id>")
@login_required
def lookupAdministratorByIdPage (id):
	return sendFalse("not implemented yet!")