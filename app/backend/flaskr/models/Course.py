from datetime import datetime
from flaskr import database
from sqlalchemy_utils import UUIDType
import uuid

db = database.db

ta_course_linker = db.Table(
    'ta',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('ticket_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)

student_course_linker = db.Table(
    'student',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)


class Course(db.Model):
    """
    Een course.
    """
    id = db.Column(UUIDType(binary=False), primary_key=True)
    course_email = db.Column(db.String(120), unique=False, nullable=False)
    title = db.Column(db.String(255), unique=False, nullable=False)
    description = db.Column(db.Text, nullable=True)


    # Dit is een soort toString zoals in Java, voor het gebruiken van de database
    # in de commandline. Op die manier kan je data maken en weergeven zonder formulier.
    def __repr__(self):
        return '<Course {}>'.format(self.title)

    @property
    def serialize(self):
        """
        Zet dit course om in json. Dit is alles wat de frontend kan zien,
        dus zorg dat er geen gevoelige info in zit.
        """
        return {
            'id': self.id,
            'course_id': self.course_id,
            'course_email': self.course_email,
            'title': self.title,
            'description': self.description
        }

    @property
    def checkValid(self):
        """
        Checks if an object is valid to insert into a database. So all
        fields that should be set, are set. If a value is not set, throw
        for now a ValueError().
        """
        pass
