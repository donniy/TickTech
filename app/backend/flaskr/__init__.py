import os
import requests
from flask import Flask, render_template, jsonify, request
from flask import Flask
from flaskr import database
from datetime import datetime
from flask_wtf.csrf import CSRFProtect

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


    if os.environ['FLASK_ENV'] == 'development':
        # When in development mode, we proxy the local Vue server. This means
        # CSRF Protection is not available. Make sure to test application in
        # production mode as well.
        app.config['WTF_CSRF_CHECK_DEFAULT'] = False
    
    
    csrf = CSRFProtect(app)

    db_uri = os.environ.get('DATABASE_CONNECTION')

    if db_uri in [None, '']:
        db_uri = 'sqlite:////tmp/test.db'

    app.config.from_mapping(
        SECRET_KEY='dev',
<<<<<<< HEAD
        SQLALCHEMY_DATABASE_URI=db_uri
=======
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.instance_path, 'test.db')
>>>>>>> master
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

    #Create and populate the database
    app.app_context().push()
    database.init_db()


<<<<<<< HEAD
    @app.route('/api/course/<course_id>')
    def retrieve_course_tickets(course_id):
        """
        Geeft alle ticktes over gegeven course.
        """
        # TODO: Controleer of degene die hierheen request permissies heeft.
        tickets = Ticket.query.filter_by(course_id=course_id).all()
        return database.json_list(tickets)
    
    @app.route('/api/ticket/<ticket_id>/reply', methods=['POST'])
    def reply_message(ticket_id):
        """
        Tijdelijke functie, geeft altijd success terug en het bericht.
        """
        return jsonify({'status': "success", 'message': {'text': request.json.get("message"), 'user_id': 12345678, 'id': 5}})


    @app.route('/api/ticket/<ticket_id>')
    def retrieve_single_ticket(ticket_id):
        """
        Geeft een enkel ticket.
        """
        # TODO: Controlleer rechten
        ticket = Ticket.query.get(ticket_id)
        return jsonify(ticket.serialize)
=======
    # Setup blueprints
    from .api import apiBluePrint
    app.register_blueprint(apiBluePrint)

>>>>>>> master

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
