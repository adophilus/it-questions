from datetime import datetime

from flask import Blueprint
from flask import request
from flask_login import login_required

from ..controllers.account import Account
from ..controllers.config import config
from ..controllers.methods import jsonize, sendFalse, sendTrue
from ..models.school_event import SchoolEvent

school = Blueprint("school", __name__)

@school.route("/event/get/<event_id>", methods = [ "POST" ])
def getEventById (event_id):
	schoolEvent = SchoolEvent.getById(event_id)
	if (schoolEvent):
		return jsonize(schoolEvent.as_dict())

	return jsonize(config.getMessage("INEXISTENT_SCHOOL_EVENT_CREATION"))

@school.route("/event/get", methods = [ "POST" ])
def getEventAllEvents ():
	return sendTrue([ schoolEvent.as_dict() for schoolEvent in SchoolEvent.getAll() ])

@school.route("/event/add", methods = [ "POST" ])
# @login_required
def addSchoolEvent ():
	# if (not Account(_object = current_user).isAdmin()):
	# 	return sendFalse(config.getMessage("ACCESS_DENIED"))

	event_name = request.form.get("event")
	description = request.form.get("description")
	venue = request.form.get("venue")

	try:
		date_time = datetime.strptime(request.form.get("datetime"), "%d/%m/%Y %H:%M")

		event = SchoolEvent(DATE_TIME = date_time, EVENT = event_name, DESCRIPTION = description, VENUE = venue)
		event.add()
	except Exception as e:
		return sendFalse(config.getMessage("UNSUCCESSFUL_SCHOOL_EVENT_CREATION"))

	return sendTrue(config.getMessage("SUCCESSFUL_SCHOOL_EVENT_CREATION"))