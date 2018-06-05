from flask import current_app, g
from flask import Flask, render_template, jsonify
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db():
    """
    Function to add all models to the database.
    Call after a context is pushed on the flask context stack,
    otherwise it cannot create the database.
    """

    #Maybe automate this from within the models dir?
    import flaskr.models
    db.create_all()




# Replace to a different file.
def json_list(l):
    """
    Maak JSON van de lijst.
    """
    return jsonify(json_list=[i.serialize for i in l])


