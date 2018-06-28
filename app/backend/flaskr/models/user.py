from flaskr import database, sockets
from sqlalchemy_utils import UUIDType
from datetime import datetime
import bcrypt

db = database.db
socketio = sockets.get_socketio()

label_linker = db.Table('label_link', db.Model.metadata,
                             db.Column('user_id', db.Integer,
                                       db.ForeignKey('user.id')),
                             db.Column('label_id', UUIDType(binary=False),
                                       db.ForeignKey('label.label_id')))


class User(db.Model):
    """
    A user class that specifies the user model.
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, nullable=False, primary_key=True)  # student ID
    name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=True)
    password = db.Column(db.String(120), unique=False, nullable=False)
    labels = db.relationship("Label", secondary=label_linker,
                             backref="users")
    experience = db.Column(db.Integer, nullable=False, default=1)
    level = db.Column(db.Integer, nullable=False, default=1)
    code = db.Column(UUIDType(binary=False), nullable=True)
    code_expiration = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        """
        Function that will state how the object is
        displayed when printed to the console.
        Like a toString() method in Java.
        """
        return '<User {}>'.format(self.name)

    @property
    def serialize(self):
        """
        Transforms the object into a json object.
        This will be used at the front-end, so dont include
        sensitive information in the json object.
        """
        return {
            'name': self.name,
            'id': self.id,
            'email': self.email,
        }

    def notify(self, notification):
        """
        Sends a message to this user in a private websocket.
        """
        print("Notifying {}".format(self.name))
        print("Message: {}".format(notification))
        print("Room: {}".format("user-{}".format(self.id)))
        socketio.emit('message', notification,
                      room="user-{}".format(self.id))

    def read_message(self, message):
        """
        Mark given message as read.
        """
        if message in self.unread:
            self.unread.remove(message)
        db.session.add(self)
        db.session.commit()

    def read_messages(self, messages):
        """
        Mark all messages in :messages: as read.
        """
        for message in messages:
            if message in self.unread:
                self.unread.remove(message)
        db.session.add(self)
        db.session.commit()

    def create(self, id, name, email, password):
        """
        Creates a user.
        """
        self.id = id
        self.name = name
        self.email = email
        salt = bcrypt.gensalt()
        hashedpsw = bcrypt.hashpw(password.encode('utf-8'), salt)
        self.password = hashedpsw
        self.level = 0
        self.experience = 0
