from flaskr import database, sockets
from sqlalchemy_utils import UUIDType

db = database.db
socketio = sockets.get_socketio()

association_table = db.Table('association', db.Model.metadata,
                             db.Column('left_id', db.Integer,
                                       db.ForeignKey('user.id')),
                             db.Column('right_id', UUIDType(binary=False),
                                       db.ForeignKey('label.label_id')))


class User(db.Model):
    """
    A user.
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, nullable=False, primary_key=True)  # student ID
    name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=True)
    password = db.Column(db.String(120), unique=False, nullable=False)
    labels = db.relationship("Label", secondary=association_table,
                             backref="users")
    experience = db.Column(db.Integer, nullable=False, default=1)
    level = db.Column(db.Integer, nullable=False, default=1)

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
