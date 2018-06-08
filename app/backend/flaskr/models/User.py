import flask_login
from flaskr import database

db = database.db


class User(flask_login.UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(120), unique=False, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

