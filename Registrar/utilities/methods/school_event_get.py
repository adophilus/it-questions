from flask import globals


def _getSchoolEventById (id):
    schoolEvent = globals.SchoolEvent.query.filter_by(id = id)

    if (schoolEvent.first()):
        return schoolEvent

def getSchoolEventById (id):
    schoolEvent = _getSchoolEventById(id)
    if (schoolEvent):
        return schoolEvent.first()