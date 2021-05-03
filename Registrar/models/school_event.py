from flask import globals

class SchoolEvent (globals.db.Model):
    id = globals.db.Column(globals.db.Text, primary_key = True)
    DAY = globals.db.Column(globals.db.Date)
    EVENT = globals.db.Column(globals.db.Text)
    DESCRIPTION = globals.db.Column(globals.db.Text)
    VENUE = globals.db.Column(globals.db.Text)

    @classmethod
    def getById (cls, id):
        return cls.query.filter_by(id = id).first()