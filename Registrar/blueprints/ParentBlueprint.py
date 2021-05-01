from flask import Blueprint
from flask import globals
from flask_login import current_user, login_required
from flask import redirect
from flask import session
from flask import url_for

parent = Blueprint("parent", __name__)

@parent.route("/")
@login_required
def parentIndexPage ():
	if not globals.methods.Client.isParent():
		return globals.methods.redirectUserToHomePage()

	return globals.methods.renderUserAccountHomePage()

@parent.route("/<id>")
@login_required
def lookupParentByIdPage (id):
	return globals.methods.renderAccountPageOf(id, globals.model.Parent["name"])