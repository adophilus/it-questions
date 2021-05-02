from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///on_the_fly_database_003.db"
db = SQLAlchemy(app)

# firstTable = db.Table("test", db.metadata,
# 	db.Column("id", db.Integer, autoincrement = True, primary_key = True),
# 	db.Column("value", db.String(46))
# )

# firstTable.create(db.engine, True)

# class RandomTable ():
# 	pass

# db.mapper(RandomTable, firstTable)

# record = RandomTable()
# record.value = "......."

# db.session.add(record)
# db.session.commit()

class RandomTable ():
	pass

randomTable = db.Table("test", db.metadata,
	db.Column("id", db.Integer, autoincrement = True, primary_key = True),
	db.Column("value", db.String(46))
	, extend_existing = True
)

db.mapper(RandomTable, randomTable)

r = randomTable
print(r.exists(db.engine))
# record = RandomTable()
# record.value = "test2"

# db.session.add(record)
# db.session.commit()