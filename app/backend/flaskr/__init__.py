import os
import requests
from flask import Flask, render_template, jsonify, request
from flask import Flask
from flaskr import database
from datetime import datetime
from flask_wtf.csrf import CSRFProtect
import os.path
from flaskr.models import Message, ticket, Note, Course, User
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_login import LoginManager

db = database.db
socketio = None
login_manager = None

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

    global socketio
    socketio = SocketIO(app)

    global login_manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    db_uri = os.environ.get('DATABASE_CONNECTION')

    if db_uri in [None, '']:
        db_uri = 'sqlite:////tmp/test.db'

    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=db_uri
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

    if not os.path.isfile(db_uri):
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


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


    @login_manager.unauthorized_handler
    def unauthorized():
        """
        Executed whenever an api call is unauthorized.
        """
        return database.jsonify({'status': 'unauthorized'})


    @socketio.on('join-room')
    def sock_join_room(data):
        #TODO: Check if allowed to join room
        print(data)
        print("Want to join {}".format(data['room']))
        try:
            join_room(data['room'])
        except:
            print("Failed to join room")

    @socketio.on('leave-room')
    def sock_leave_room(data):
        #TODO: Need to check if in room?
        print(data)
        print("Want to leave {}".format(data['room']))
        try:
            leave_room(data['room'])
        except:
            print("Failed to leave toom")

    return app
