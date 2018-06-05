import os
import requests
from flask import Flask, render_template, jsonify
from flask import Flask
from flaskr import database
from datetime import datetime
from flaskr.models.ticket import *

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
        SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
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
    app.app_context().push()
    database.init_db()


    @app.route('/api/course/<course_id>')
    def retrieve_course_tickets(course_id):
        """
        Geeft alle ticktes over gegeven course.
        """
        # TODO: Controleer of degene die hierheen request permissies heeft.
        tickets = Ticket.query.filter_by(course_id=course_id).all()
        return database.json_list(tickets)

    @app.route('/api/ticket/<ticket_id>')
    def retrieve_single_ticket(ticket_id):
        """
        Geeft een enkel ticket.
        """
        # TODO: Controlleer rechten
        ticket = Ticket.query.get(ticket_id)
        return jsonify(ticket.serialize)

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