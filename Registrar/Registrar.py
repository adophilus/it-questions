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

from .controllers.config import config

import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"{config['database']['schema']}:///{config['database']['path']}"
app.config["SECRET_KEY"] = config["secret_key"]
globals.db.init_app(app)
globals.app = app


# import varous blueprints
from .blueprints.MainBlueprint import main
from .blueprints.HandlerBlueprint import handler
from .blueprints.HandlerQuestionBlueprint import handlerQuestion
from .blueprints.QuestionsPool import questionsPool
from .blueprints.AdminBlueprint import admin
from .blueprints.ParentBlueprint import parent
from .blueprints.RegistrarBlueprint import registrar
from .blueprints.TeacherBlueprint import teacher
from .blueprints.StudentBlueprint import student
from .blueprints.ClassroomBlueprint import classroom
from .blueprints.DevelopmentBlueprint import development
from .blueprints.school import school

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
app.register_blueprint(development, url_prefix = "/dev")
app.register_blueprint(school, url_prefix = "/school")

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
	app.run(host = config["host"], port = config["port"], debug = config["debugging"])