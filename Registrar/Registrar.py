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
import os

from .utilities.csvparser import CSVParser
from .utilities import General
from .utilities.General import *
from .utilities import csvparsers

globals.CSVParser = CSVParser
globals.General = General

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"{globals.config['database']['schema']}:///{globals.config['database']['path']}"
app.config["SECRET_KEY"] = globals.config["secret_key"]
globals.db.init_app(app)
globals.app = app

from . import models
from .utilities.methods import methods
globals.model = models
globals.methods = methods

# load configuration files
globals.school_prefs = globals.General.loadJson(os.path.join("data", "school", "preferences.json"))

# load important .csv data files
globals.running_processes = CSVParser(os.path.join("data", "Registrar", "running-processes.csv"), parser = csvparsers.parseRunningProcesses, unparser = csvparsers.unparseRunningProcesses)

# import varous blueprints
from .blueprints.MainBlueprint import main
from .blueprints.HandlerBlueprint import handler
from .blueprints.HandlerQuestionBlueprint import handlerQuestion
from .blueprints.HandlerClassroomBlueprint import handlerClassroom
from .blueprints.QuestionsPool import questionsPool
from .blueprints.AdminBlueprint import admin
from .blueprints.ParentBlueprint import parent
from .blueprints.RegistrarBlueprint import registrar
from .blueprints.TeacherBlueprint import teacher
from .blueprints.StudentBlueprint import student
from .blueprints.ClassroomBlueprint import classroom
from .blueprints.DevelopmentBlueprint import development

app.register_blueprint(main)
app.register_blueprint(handler, url_prefix = "/handler")
app.register_blueprint(handlerQuestion, url_prefix = "/handler/question")
app.register_blueprint(handlerClassroom, url_prefix = "/handler/classroom")
app.register_blueprint(questionsPool, url_prefix = "/questions-pool")
app.register_blueprint(admin, url_prefix = "/administrator")
app.register_blueprint(parent, url_prefix = "/parent")
app.register_blueprint(registrar, url_prefix = "/registrar")
app.register_blueprint(teacher, url_prefix = "/teacher")
app.register_blueprint(student, url_prefix = "/student")
app.register_blueprint(classroom, url_prefix = "/classroom")
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

if __name__ == "__main__":
	app.run(host = globals.config["host"], port = globals.config["port"], debug = globals.config["debugging"])