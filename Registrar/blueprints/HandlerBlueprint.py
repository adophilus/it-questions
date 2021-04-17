from flask import Blueprint
from flask import globals
from flask import render_template
from flask import redirect
from flask import request
from flask import session
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

from utilities.General import *
import os
import re
import time
import urllib

handler = Blueprint("handler", __name__)

# login manager
globals.loginManager = LoginManager()
globals.loginManager.login_view = "main.mainLoginPage"
globals.loginManager.init_app(globals.app)

@globals.loginManager.user_loader
def load_user (user_id):
    user = globals.methods.getAccountById(user_id)
    if user.ACCOUNT_TYPE == "administrator":
        user = globals.Administrator.query.get(user.id)
    elif user.ACCOUNT_TYPE == "parent":
        user = globals.Parent.query.get(user.id)
    elif user.ACCOUNT_TYPE == "teacher":
        user = globals.Teacher.query.get(user.id)
    else:
        user = globals.Student.query.get(user.id)
    return user

@handler.route("/login", methods = ["POST"])
def handleLogin ():
    return globals.methods.loginUser(request.form.get("username"), request.form.get("password"))

@handler.route("/logout", methods = ["POST", "GET"])
@login_required
def handleLogout ():
    logout_user()
    return unjsonize({"status": True, "data": globals.config.getMessage("SUCCESSFUL_SIGNOUT")})

@handler.route("/signup", methods = ["POST"])
def handleSignUp ():
    if (not globals.config["security"]["ALLOW_REMOTE_ACCOUNT_CREATION"]):
        return globals.General.sendFalse(globals.config.getMessage("REMOTE_ACCOUNT_CREATION_NOT_ALLOWED"))

    # Everyone's fields
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    other_names = request.form.get("other_names")
    birthday = request.form.get("birthday")
    email = request.form.get("email")
    phone_number = request.form.get("phone_number")
    username = request.form.get("username")
    password = request.form.get("password")
    account_type = str(request.form.get("account_type")).lower()

    # Student's fields
    classroom = request.form.get("classroom")
    department = request.form.get("department")
    subjects_offered = request.form.get("subjects_offered")
    extracurricular_activities = request.form.get("extracurricular_activities")

    # Teacher's fields
    subjects_teaching = request.form.get("subjects_teaching")

    # Parent's fields
    ward_id = request.form.get("ward_id")
    # ward_first_name = request.form.get("ward_first_name")
    # ward_last_name = request.form.get("ward_last_name")
    # ward_other_names = request.form.get("ward_other_names")
    # ward_classroom = request.form.get("ward_classroom")

    return globals.methods.createUserAccount(
        # Everyone's fields
        first_name,
        last_name,
        other_names,
        birthday,
        email,
        phone_number,
        username,
        password,
        account_type,

        # Student's fields
        classroom = classroom,
        department = department,
        subjects_offered = subjects_offered,
        extracurricular_activities = extracurricular_activities,

        # Teacher's fields
        subjects_teaching = subjects_teaching,

        # Parent's fields
        ward_id = ward_id
        # ward_first_name = ward_first_name,
        # ward_last_name = ward_last_name,
        # ward_other_names = ward_other_names,
        # ward_classroom = ward_classroom
    )

# @handler.route("/get-calendar")
# def getCalendarArray ():
#     return globals.General.unjsonize(globals.methods.getCalendarArray())

@handler.route("/account/change/password", methods = ["POST"])
@login_required
def changeUserPassword ():
    user_id = globals.methods.Client.getUserId()
    confirm_password = request.form.get("confirm_password")
    changes = {
        "password": request.form.get("password")
    }

    if not (globals.methods.Client.hasPassword(confirm_password)):
        errmsg = globals.config.getMessage("CHANGES_NOT_SAVED")
        return globals.General.sendFalse(errmsg)

    if not (globals.methods.Validate.password(confirm_password)):
        return globals.General.sendFalse(globals.config.getMessage("INVALID_PASSWORD"))

    if not (globals.methods.Verify.credentials(globals.methods.Client.getUsername(), confirm_password)):
        return globals.General.sendFalse(globals.config.getMessage("INCORRECT_PASSWORD"))

    user = globals.methods.getAccountById(user_id)
    if not (user):
        return globals.General.sendFalse(globals.config.getMessage("INEXISTENT_ACCOUNT"))

    if (changes["password"]):
        has_changed_password = globals.methods.changePassword(user, confirm_password, changes["password"])
        if (has_changed_password != 0):
            return has_changed_password

    return globals.General.sendFalse(globals.config.getMessage("ACCOUNT_SETTINGS_UPDATED"))

@handler.route("/list-of-classrooms", methods=["GET", "POST"])
def getListOfClassrooms ():
    classes = globals.Classroom.query.all()
    classes = [classroom.NAME for classroom in classes]
    return globals.General.unjsonize(list(classes))

@handler.route("/list-of-subjects")
def getListOfSubjects ():
    subjects = [subject.SUBJECT_NAME for subject in globals.methods.getSchoolSubjectsList()]
    return globals.General.unjsonize(list(subjects))

@handler.route("/school/events/get/<after_event_id>", methods = ["GET"])
# @login_required
def getSchoolEvents (after_event_id):
    school_events = [ {"ID": school_event.id, "EVENT": school_event.EVENT, "DATE": globals.methods.dateToString(school_event.DAY)["ymd"], "VENUE": school_event.VENUE} for school_event in globals.SchoolEvent.query.filter().all() ]

    if (after_event_id == "null"):
        return globals.General.unjsonize(school_events)

    return_events = []
    start = False
    for school_event in school_events:
        if (start):
            return_events.append(school_event)

        if (school_event["ID"] == after_event_id):
            start = True

    return globals.General.unjsonize(return_events)

@login_required
@handler.route("/chatroom/get", methods = ["GET"])
def getMyChatrooms ():
    if (globals.methods.Client.isAdmin()):
        return "check HandlerBlueprint getMyChatrooms"

    chatrooms = globals.methods.getAccountDetails(current_user.id).get("chatrooms")

    for chatroom_id in chatrooms:
        chatroom = globals.methods.getChatroomById(chatroom_id)
        if not (current_user.id in chatroom.MEMBERS):
            chatrooms.remove(chatroom_id)
        else:
            chatrooms.remove(chatroom_id)
            chatrooms.append({
                "name": chatroom.NAME,
                "id": chatroom.id
            })

    return globals.General.unjsonize(chatrooms)

@login_required
@handler.route("/chatroom/chat/add/<chatroom_id>", methods = ["POST"])
def addChatroomChat (chatroom_id):
    chatroom = globals.methods.getChatroomById(chatroom_id)

    if not (globals.methods.Client.isAdmin() or globals.methods.Client.isTeacher()):
        if not (current_user.id in globals.General.jsonize(chatroom.MEMBERS)):
            errmsg = globals.config.getMessage("UNAUTHORIZED_CHATROOM_ACCESS")
            return unjsonize({"data": errmsg, "error": errmsg, "status": False})

    if (not chatroom):
        errmsg = globals.config.getMessage("INEXISTENT_CHATROOM")
        return unjsonize({"data": errmsg, "error": errmsg, "status": False})

    chatfile_path = globals.chatrooms[chatroom_id]["chats-file"]

    if not (chatfile_path):
        errmsg = globals.config.getMessage("INEXISTENT_CHATROOM")
        return unjsonize({"data": errmsg, "error": errmsg, "status": False})

    chat_message = request.form.get("chat_message")
    present = globals.methods.getPresent()

    if (not chat_message):
        errmsg = globals.config["message"]["EMPTY_CHATROOM_CHAT"]
        return unjsonize({"data": errmsg, "error": errmsg, "status": False})

    present = globals.methods.getPresent()

    float_time = time.time()
    date = globals.methods.getPresentYMD()
    _time = f"{present.hour}:{present.minute}"
    sender = globals.methods.Client.getUsername()

    parser = globals.chatrooms[chatroom_id]["chats"]
    chat = {
        "FLOAT_TIME": float_time,
        "DATE": date,
        "TIME": _time,
        "MESSAGE": chat_message,
        "SENDER": sender
    }
    parser.insert(chat)
    parser.save()

    return unjsonize({"data": chat, "status": True})

@login_required
@handler.route("/chatroom/chat/get/<chatroom_id>/<after_chat_float_time>", methods = ["GET"])
def getChatroomChats (chatroom_id, after_chat_float_time):
    chatroom = globals.methods.getChatroomById(chatroom_id)

    if not (globals.methods.Client.isAdmin() or globals.methods.Client.isTeacher()):
        if not (current_user.id in globals.General.jsonize(chatroom.MEMBERS)):
            errmsg = globals.config.getMessage("UNAUTHORIZED_CHATROOM_ACCESS")
            return unjsonize({"data": errmsg, "error": errmsg, "status": False})

    if (not chatroom):
        errmsg = globals.config.getMessage("INEXISTENT_CHATROOM")
        return unjsonize({"data": errmsg, "error": errmsg, "status": False})

    chatfile_path = globals.chatrooms[chatroom_id]["chats-file"]

    if not (chatfile_path):
        errmsg = globals.config.getMessage("INEXISTENT_CHATROOM")
        return unjsonize({"data": errmsg, "error": errmsg, "status": False})

    parser = globals.chatrooms[chatroom_id]["chats"]
    chats = []
    for row in parser.selectAll()["rows"]:
        if (len(row) == 0):
            continue

        float_time = row[0]
        date = row[1]
        _time = row[2]
        message = row[3]
        sender = row[4]

        chats.append({
            "FLOAT_TIME": float_time,
            "DATE": date,
            "TIME": _time,
            "MESSAGE": message,
            "SENDER": sender
        })

    if (after_chat_float_time == "null"):
        return unjsonize({
            "data": chats,
            "status": True
        })

    after_chat_float_time = float(after_chat_float_time)

    globals.General.putContentIn("ouput.txt", str(after_chat_float_time))

    return_chats = []
    start = False
    for chat in chats:
        if (start):
            return_chats.append(chat)

        if (chat["FLOAT_TIME"] >= after_chat_float_time):
            start = True

    return unjsonize({"data": return_chats, "status": True})
@handler.route("/account/is-logged-in")
def checkUserLogin ():
    return str(not globals.methods.Client.isVisitor())

@handler.route("/remove-account")
@handler.route("/delete-account")
@login_required
def deleteUserAccount ():
    return globals.methods.removeUserAccount(current_user.id)
