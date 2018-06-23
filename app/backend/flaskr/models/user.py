from flaskr import database, sockets
from flaskr.models import Course
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
    Een user.
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, nullable=False, primary_key=True)  # student ID
    name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=True)
    labels = db.relationship("Label", secondary=association_table,
                             backref="users")

    courses_user_is_student_in = db.relationship(
        "Course", secondary=Course.student_course_linker,
        lazy='subquery',
        backref=db.backref('courses_user_is_student_in'))

    courses_user_is_ta_in = db.relationship(
        "Course", secondary=Course.ta_course_linker,
        lazy='subquery',
        backref=db.backref('courses_user_is_ta_in'))

    courses_user_is_supervisor_in = db.relationship(
        "Course", secondary=Course.supervisor_linker,
        lazy='subquery',
        backref=db.backref('courses_user_is_supervisor_in'))

    # Dit is een soort toString zoals in Java, voor het gebruiken van de
    # database in de commandline. Op die manier kan je data maken en weergeven
    # zonder formulier.
    def __repr__(self):
        return '<User {}>'.format(self.name)

    @property
    def serialize(self):
        """
        Zet de user om in json. Dit is alles wat de frontend kan zien,
        dus zorg dat er geen gevoelige info in zit.
        """
        return {
            'name': self.name,
            'id': self.id,
            'email': self.email,
        }

    @property
    def checkValid(self):
        """
        Niet nodig.
        """
        pass

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
