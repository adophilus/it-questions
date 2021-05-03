from flask import Blueprint
from flask import globals
from flask import render_template
from flask import redirect
from flask import request
from flask import session
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

from ..Registrar import app
from ..contollers.config import config
from ..contollers.methods import sendFalse, jsonize

import os
import re
import time
import urllib

handler = Blueprint("handler", __name__)

# login manager
globals.loginManager = LoginManager()
globals.loginManager.login_view = "main.mainLoginPage"
globals.loginManager.init_app(app)

@globals.loginManager.user_loader
def load_user (user_id):
    # user = globals.methods.Account(user_id)
    # if user.ACCOUNT_TYPE == "administrator":
    #     user = globals.model.Administrator.query.get(user.id)
    # elif user.ACCOUNT_TYPE == "parent":
    #     user = globals.model.Parent.query.get(user.id)
    # elif user.ACCOUNT_TYPE == "teacher":
    #     user = globals.model.Teacher.query.get(user.id)
    # else:
    #     user = globals.model.Student.query.get(user.id)
    # return user
    account = Account(user_id)
    return account.account

@handler.route("/login", methods = [ "POST" ])
def handleLogin ():
    username = request.form.get("username")
    password = request.form.get("password")

    account = Account(username = username)

    if (account):
		if (not (account.hasUsername(username) and  account.hasPassword(password)):
			return sendFalse(config.getMessage("INVALID_CREDENTIALS"))

        if not (account.isAllowedEntry()):
            return sendFalse(config.getMessage("ACCESS_DENIED_PAGE"))

        if (login_user(account)):
            return jsonize({"status": True, "ACCOUNT_TYPE": account.ACCOUNT_TYPE, "data": config.getMessage("SUCCESSFUL_SIGNIN")})
        else:
            return sendFalse(config.getMessage("UNSUCCESSFUL_SIGNIN"))

    return sendFalse(config.getMessage("INEXISTENT_ACCOUNT"))

@handler.route("/logout", methods = [ "POST", "GET" ])
@login_required
def handleLogout ():
    logout_user()
    return sendTrue(config.getMessage("SUCCESSFUL_SIGNOUT"))

@handler.route("/signup", methods = [ "POST" ])
def handleSignUp ():
    if (not config["security"]["ALLOW_REMOTE_ACCOUNT_CREATION"]):
        return sendFalse(config.getMessage("REMOTE_ACCOUNT_CREATION_NOT_ALLOWED"))

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

@handler.route("/account/change/password", methods = [ "POST" ])
@login_required
def changeUserPassword ():
    account = Account(Client.getUserId())
    old_password = request.form.get("confirm_password")
    new_password =  request.form.get("password")

    if (not (account)):
        return sendFalse(config.getMessage("INEXISTENT_ACCOUNT"))

    if (not (account.hasPassword(old_password)):
        return sendFalse(config.getMessage("CHANGES_NOT_SAVED"))

    if (not (globals.methods.Validate.password(new_password)):
        return sendFalse(config.getMessage("INVALID_PASSWORD"))

    if (not (account.hasUsername(globals.methods.Client.getUsername()) and account.hasPassword(confirm_password))):
        return globals.General.sendFalse(config.getMessage("INCORRECT_PASSWORD"))

    if (not account.changePassword(old_password, new_passwowrd)):
        return sendFalse(config.getMessage("ERROR_OCCURRED"))

    return globals.General.sendFalse(config.getMessage("ACCOUNT_SETTINGS_UPDATED"))

@handler.route("/school/events/get/<after_event_id>", methods = ["GET"])
def getSchoolEvents (after_event_id):
    school_events = [ {"ID": school_event.id, "EVENT": school_event.EVENT, "DATE": globals.methods.dateToString(school_event.DAY)["ymd"], "VENUE": school_event.VENUE} for school_event in globals.model.SchoolEvent.query.filter().all() ]

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

@handler.route("/remove-account")
@handler.route("/delete-account")
@login_required
def deleteUserAccount ():
    if (not account(current_user.id).delete(current_user.id).delete()):
        return sendFalse(config.getMessage("ERROR_OCCURRED"))
    return sendTrue(config.getMessage("SUCCESSFUL_ACCOUNT_DELETION"))