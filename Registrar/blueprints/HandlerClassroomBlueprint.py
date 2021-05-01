from flask import Blueprint
from flask import globals
from flask_login import login_required, current_user

from ..utilities.General import sendFalse, sendTrue

handlerClassroom = Blueprint("handlerClassroom", __name__)


@handlerClassroom.route("/list")
@login_required
def getListOfClassrooms ():
    classes = [classroom.NAME for classroom in globals.model.Classroom.query.all()]
    return globals.General.unjsonize(classes)

@handlerClassroom.route("/<classroom_id>/send-message", methods = [ "GET", "POST" ])
@login_required
def sendClassroomMessage (classroom_id):
    classroom = globals.model.Classroom.getById(classroom_id)
    if (not classroom):
        return sendFalse(globals.config.getMessage("INEXISTENT_CLASS"))
    return sendTrue(globals.config.getMessage("CLASS_MESSAGE_SENT"))