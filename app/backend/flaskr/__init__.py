import os
import requests
from flask import Flask, render_template
from flaskr import database, sockets
from flask_wtf.csrf import CSRFProtect
import os.path
from flaskr.models import Message, ticket, Note, Course, user, Label
from flask_jwt_extended import JWTManager
from flask_jwt import JWT, jwt_required, current_identity
from flask_socketio import emit, join_room, leave_room
from . import login
import poplib
from mail.thread import MailThread
from datetime import timedelta
from flask_hashfs import FlaskHashFS
from os.path import expanduser
from flask_mail import Mail
from flaskr.config import Config

db = database.db
socketio = sockets.get_socketio()
login_manager = None
app = None
fs = None


def create_app(test_config=None):
    """
    Function to create an instance of the app.
    A config can be specified. It uses sql alchemy
    which is stored in the database file.
    """

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True,
                static_folder="../../dist/static",
                template_folder="../../dist")

    if os.environ.get('FLASK_ENV') == 'development':
        # When in development mode, we proxy the local Vue server. This means
        # CSRF Protection is not available. Make sure to test application in
        # production mode as well.
        app.config['WTF_CSRF_CHECK_DEFAULT'] = False

    app.config['WTF_CSRF_CHECK_DEFAULT'] = False

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['JWT_SECRET_KEY'] = 'very-secure'

    # Send email settings, for now hardcoded
    app.config['MAIL_SERVER'] = Config.EMAIL_SEND_SERVER
    app.config['MAIL_PORT'] = Config.EMAIL_SEND_PORT
    app.config['MAIL_USE_SSL'] = Config.EMAIL_SEND_SSL
    app.config['MAIL_USE_TLS'] = Config.EMAIL_SEND_TLS
    app.config['MAIL_USERNAME'] = Config.EMAIL_SEND_EMAIL
    app.config['MAIL_PASSWORD'] = Config.EMAIL_SEND_PASSWORD
    app.config['MAIL_DEFAULT_SENDER'] = Config.EMAIL_SEND_EMAIL
    Mail(app)

    app.config['SEND_MAIL_ON_MESSAGE'] = False

    # Make user logged in for 1 day.
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=86400)

    # Set hashfs preferences
    fs = FlaskHashFS()
    app.config.update({
        'HASHFS_HOST': None,
        'HASHFS_PATH_PREFIX': '/useruploads',
        'HASHFS_ROOT_FOLDER': expanduser("~") + '/serverdata',
        'HASHFS_DEPTH': 4,
        'HASHFS_WIDTH': 1,
        'HASHFS_ALGORITHM': 'sha256'
    })
    print("Uploads are saved in: " + expanduser("~") + '/serverdata')
    fs.init_app(app)

    csrf = CSRFProtect(app)
    csrf = csrf  # flake8

    db_uri = os.environ.get('DATABASE_CONNECTION')

    if db_uri in [None, '']:
        db_uri = 'sqlite:////tmp/test.db'

    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=db_uri,
        MAX_CONTENT_LENGTH=10485760,
    )

    if test_config:
        app.config.update(test_config)

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
    socketio.init_app(app)

    if not os.path.isfile('/tmp/test.db') and not test_config:
        app.app_context().push()
        database.init_db()

    # Setup blueprints
    from .api import apiBluePrint
    app.register_blueprint(apiBluePrint)

    login.init_jwt(app)

    # Setup routing for vuejs.
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def render_vue(path):
        if app.debug:
            try:
                res = requests.get(
                    'http://localhost:8080/{}'.format(path)
                ).text
                return res
            except Exception as e:
                return "Je gebruikt dev mode maar hebt je Vue" \
                       + "development server niet draaien"
        return render_template("index.html")

    @socketio.on('join-room')
    def sock_join_room(data):
        # TODO: Check if allowed to join room
        print(data)
        print("Want to join {}".format(data['room']))
        r_type, r_id = tuple(data['room'].split('-', maxsplit=1))
        if r_type == "user":
            print("That room is a private user room")
            print("it belongs to user {}".format(r_id))
            print("TODO: check if request was sent by that user")
        try:
            join_room(data['room'])
            emit('join-room', {'status': 'success',
                               'room': data['room']})
        except Exception as e:
            print("Failed to join room")
            emit('join-room', {'status': 'failure',
                               'room': data['room']})

    @socketio.on('leave-room')
    def sock_leave_room(data):
        # TODO: Need to check if in room?
        print(data)
        print("Want to leave {}".format(data['room']))
        try:
            leave_room(data['room'])
        except Exception as e:
            print("Failed to leave toom")

    @socketio.on('setup-email')
    def setup_mail(data):
        emit('setup-email', {'result': 'update', 'data': "recieved data"})
        email = data['email']
        password = data['password']
        port = data['port']
        server = data['pop']
        course_id = data['course_id']
        sleeptime = 60

        thread = MailThread.exist_thread_courseid(course_id)
        if (MailThread.exist_thread_email(email)):
            if thread is None:
                emit('setup-email',
                     {'result': 'fail', 'data': 'Email already exists'})
                return

        try:
            test_connection = poplib.POP3_SSL(server, port)
            test_connection.user(email)
            test_connection.pass_(password)
            test_connection.quit()
        except (poplib.error_proto) as msg:
            message = msg.args[0].decode('ascii')
            emit('setup-email', {'result': 'fail', 'data': message})
            return
        except OSError as msg:
            message = str(msg)
            emit('setup-email', {'result': 'fail', 'data': message})
            return

        if (thread is None):
            new_thread = MailThread(sleeptime, server, port, email, password,
                                    course_id)
            new_thread.setName(course_id)
            new_thread.start()
        else:
            thread.update(sleep_time=sleeptime, server=server, port=port,
                          email=email, password=password)

        course = Course.Course.query.get(course_id)
        course.course_email = email
        course.mail_password = password
        course.mail_port = port
        course.mail_server_url = server
        if not database.addItemSafelyToDB(course):
            emit('setup-email', {'result': 'fail', 'data': 'database error'})
            return

        emit('setup-email', {'result': 'succes'})
        return

    return app
