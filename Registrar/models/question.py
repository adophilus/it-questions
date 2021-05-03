from flask import globals

class Question (globals.db.Model):
    id = globals.db.Column(globals.db.Text, primary_key = True)
    QUESTION_TITLE = globals.db.Column(globals.db.Text)
    QUESTION_TYPE = globals.db.Column(globals.db.Text)
    NUMBER_OF_QUESTIONS = globals.db.Column(globals.db.Integer)
    CREATOR = globals.db.Column(globals.db.Text)
    CREATOR_ID = globals.db.Column(globals.db.Text)
    OWNER = globals.db.Column(globals.db.Text)
    OWNER_ID = globals.db.Column(globals.db.Text)
    IMAGE_PATH = globals.db.Column(globals.db.Text)

    @classmethod
    def getById (cls, id):
        return cls.query.filter_by(id = id).first()