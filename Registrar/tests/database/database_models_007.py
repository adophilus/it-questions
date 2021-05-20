from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database_models_database_007.db"
db = SQLAlchemy(app)

class Test ():
	id = db.Column(db.Integer, autoincrement = True, primary_key = True)

testTable = db.Table("test", db.metadata,
	db.Column("id", db.Integer, autoincrement = True, primary_key = True)
)

testTable.create(db.engine, True)
db.mapper(Test, testTable)

t = Test()

db.session.add(t)
db.session.commit()

db.session.delete(t)
db.session.commit()

# db.session.delete(t)
# db.session.commit()
"""  stacktrace
C:\Program Files (x86)\Python37-32\lib\site-packages\sqlalchemy\orm\persistence.py:1364: SAWarning: DELETE statement on table 'test' expected to delete 1 row(s); 0 were matched.  Please set confirm_deleted_rows=False within the mapper configuration to prevent this warning.
  % (table.description, expected, rows_matched)
"""

# raises exception
# db.session.delete(None)
# db.session.commit()