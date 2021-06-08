from flask import globals

from ..controllers.config import config

class Question (globals.db.Model):
    id = globals.db.Column(globals.db.Text, primary_key = True)
    TITLE = globals.db.Column(globals.db.String(100))
    IS_PUBLIC = globals.db.Column(globals.db.Integer, default = 0)
    NUMBER_OF_QUESTIONS = globals.db.Column(globals.db.Integer, default = 1)
    CREATOR = globals.db.Column(globals.db.String(config["id_length"]["account"]), nullable = False)
    OWNER = globals.db.Column(globals.db.String(config["id_length"]["account"]), nullable = False)
    IMAGE_PATH = globals.db.Column(globals.db.Text, default = "/static/media/classroom-default.png")

    @classmethod
    def getAll (cls):
        qs = [ question for question in cls.query.all() ]
        for q in qs:
            q.__init__(exists = True)
        return qs

    @classmethod
    def getAllPublic (cls):
        qs = [ question for question in cls.query.filter_by(IS_PUBLIC = 1) ]
        for q in qs:
            q.__init__(exists = True)
        return qs

    @classmethod
    def getById (cls, id):
        q = cls.query.filter_by(id = id).first()
        if (q != None):
            q.__init__(exists = True)
        return q