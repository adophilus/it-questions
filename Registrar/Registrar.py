#!/usr/bin/python3 -i

from flask import Flask
from flask import render_template
from flask import Response
from flask import request
from flask import Response
from flask import redirect
from flask import url_for
from flask import globals
from flask import session
from flask_sqlalchemy import SQLAlchemy
from glob import glob
import os
import webbrowser
import sqlite3

from utilities.csvparser import CSVParser
from utilities.config import Config
from utilities import General
from utilities.General import *
from utilities.methods import methods
from utilities import csvparsers
from utilities.PrivateKeyGenerator import PrivateKeyGenerator

globals.CSVParser = CSVParser
globals.General = General

app = Flask(__name__)
globals.app = app

# load configuration files
globals.config = Config(loadJson(os.path.join("data", "Registrar", "configuration.json")))
globals.school_prefs = globals.General.loadJson(os.path.join("data", "school", "preferences.json"))
globals.csvparsers = csvparsers

globals.methods = methods
globals.IDgenerator = PrivateKeyGenerator()

if not globals.config["secret_key"]:
    globals.config["secret_key"] = globals.IDgenerator.generate(level = 4)

# configure application variables
app.config["SECRET_KEY"] = globals.config["secret_key"]
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/Registrar/accounts.db"

globals.methods.refreshConfig()

# define the database connector
globals.db = SQLAlchemy(app)

from models import classroom
from models import chatroom # should be removed
from models import administrator
from models import parent
from models import teacher
from models import student
from models import school_event
from models import school_subject
from models import question


# load important .csv data files
globals.running_processes = CSVParser(os.path.join("data", "Registrar", "running-processes.csv"), parser = csvparsers.parseRunningProcesses, unparser = csvparsers.unparseRunningProcesses)

# database models
globals.Classroom = classroom.Classroom
globals.Chatroom = chatroom.Chatroom # should be removed
globals.Administrator = administrator.Administrator
globals.Parent = parent.Parent
globals.Teacher = teacher.Teacher
globals.Student = student.Student
globals.SchoolEvent = school_event.SchoolEvent
globals.SchoolSubject = school_subject.SchoolSubject
globals.Question = question.Question

globals.methods.loadChatrooms()

# import varous blueprints
from blueprints.MainBlueprint import main
from blueprints.HandlerBlueprint import handler
from blueprints.HandlerQuestionBlueprint import handlerQuestion
from blueprints.QuestionsPool import questionsPool
from blueprints.AdminBlueprint import admin
from blueprints.ParentBlueprint import parent
from blueprints.RegistrarBlueprint import registrar
from blueprints.TeacherBlueprint import teacher
from blueprints.StudentBlueprint import student
from blueprints.ClassroomBlueprint import classroom
from blueprints.ClassroomApiBlueprint import classroomApi
from blueprints.DevelopmentBlueprint import development

app.register_blueprint(main)
app.register_blueprint(handler, url_prefix = "/handler")
app.register_blueprint(handlerQuestion, url_prefix = "/handler/question")
app.register_blueprint(questionsPool, url_prefix = "/questions-pool")
app.register_blueprint(admin, url_prefix = "/administrator")
app.register_blueprint(parent, url_prefix = "/parent")
app.register_blueprint(registrar, url_prefix = "/registrar")
app.register_blueprint(teacher, url_prefix = "/teacher")
app.register_blueprint(student, url_prefix = "/student")
app.register_blueprint(classroom, url_prefix = "/classroom")
app.register_blueprint(classroomApi, url_prefix = "/api/classroom")
app.register_blueprint(development, url_prefix = "/dev")

globals.methods.RunningProcesses.register(os.getpid(), "Registrar", "The process of the main executable -- The Registrar.")
globals.methods.RunningProcesses.save()

"""
globals.days = [
    "",
    "sunday"
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
]
"""

globals.months = [
    "",
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december"
]

def openBrowser (port):
    # webbrowser.open(f"http://{globals.config['host']}:{port}")
    return False

if __name__ == "__main__":
    setTimeout(openBrowser, 2, {"port": globals.config["port"]})
    app.run(host = globals.config["host"], port = globals.config["port"], debug = globals.config["debugging"])
