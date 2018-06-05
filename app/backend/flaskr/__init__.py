import os
import requests
from flask import Flask, render_template, jsonify
from flask import Flask
from flaskr import database
from datetime import datetime
import os

from flaskr.models import Message
from flaskr.models import ticket

db = database.db


def create_app(test_config=None):
    """
    Function to create an instance of the app.
    A config can be specified. It uses sql alchemy
    which is stored in the database file.
    """

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True,
                static_folder = "../../dist/static",
                template_folder = "../../dist")

    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.instance_path, 'test.db')
    )


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)


    """
    Will setup the testdb if there is no db yet.
    However in debug mode this function will be called multiple
    times, so with an os variable we prevent from multiple insertions.
    This is kinda hacky.
    """
    if not os.environ.get('INITIAL_FLASK_RUN') \
       and not os.path.isfile(app.config['SQLALCHEMY_DATABASE_URI']):
        os.environ['INITIAL_FLASK_RUN'] = "true"
        app.app_context().push()
        database.init_db()


    # Setup blueprints
    from .api import apiBluePrint
    app.register_blueprint(apiBluePrint)


    # Setup routing for vuejs.
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def render_vue(path):
        if app.debug:
            try:
                res = requests.get('http://localhost:8080/{}'.format(path)).text
                return res
            except:
                return "Je gebruikt dev mode maar hebt je Vue development server niet draaien"
        return render_template("index.html")


    return app
