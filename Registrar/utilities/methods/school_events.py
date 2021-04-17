from flask import globals
import datetime

def addSchoolEvent (event_title, description, venue):
	present = globals.methods.getPresent()
	date = datetime.date(present.year, present.month, present.day)

	event = globals.SchoolEvent(
		id = globals.methods.generateSchoolEventId(),
		DATE = date,
		EVENT = event_title,
		DESCRIPTION = description,
		VENUE = venue
	)
	globals.db.session.add(event)
	globals.db.session.commit()

def removeSchoolEvent (id):
	SchoolEvent = globals.methods.getSchoolEventById(id)
	if (SchoolEvent):
		globals.db.session.delete(SchoolEvent)
		globals.db.session.commit()
