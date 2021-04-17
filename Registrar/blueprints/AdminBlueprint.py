from flask import Blueprint
from flask import globals
from flask import redirect
from flask import url_for
from flask_login import current_user, login_required

admin = Blueprint("admin", __name__)

@admin.route("/")
@login_required
def adminIndexPage ():
	if not globals.methods.Client.isAdmin():
		return globals.methods.renderUserAccountHomePage()

	return globals.methods.renderUserAccountHomePage()

@admin.route("/<id>")
@login_required
def lookupAdministratorByIdPage (id):
	return globals.methods.renderAccountPageOf(id, globals.ADMINISTRATOR["name"])