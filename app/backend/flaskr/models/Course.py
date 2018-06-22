from datetime import datetime
from flaskr import database
from sqlalchemy_utils import UUIDType
import uuid

db = database.db

ta_course_linker = db.Table(
    'ta_link_course',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'),
              primary_key=True),
    db.Column('course_id', UUIDType(binary=False), db.ForeignKey('course.id'),
              primary_key=True)
)

student_course_linker = db.Table(
    'student_link_course',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'),
              primary_key=True),
    db.Column('course_id', UUIDType(binary=False), db.ForeignKey('course.id'),
              primary_key=True)
)

label_course_linker = db.Table(
    "label_link_course",
    db.Column('course_id', UUIDType(binary=False), db.ForeignKey('course.id'),
              primary_key=True),
    db.Column('label_id', UUIDType(binary=False),
              db.ForeignKey('label.label_id'), primary_key=True)
)

supervisor_linker = db.Table(
    "supervisor_linker",
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'),
              primary_key=True),
    db.Column('course_id', UUIDType(binary=False), db.ForeignKey('course.id'),
              primary_key=True)
)


class Course(db.Model):
    """
    Een course.
    """
    id = db.Column(UUIDType(binary=False), primary_key=True)
    title = db.Column(db.String(255), unique=False, nullable=False)
    description = db.Column(db.Text, nullable=True)

    # TODO: lengthe van deze data
    course_email = db.Column(db.String(120), unique=False, nullable=True)
    mail_server_url = db.Column(db.String(120), unique=False, nullable=True)
    mail_port = db.Column(db.Integer, nullable=True)
    mail_password = db.Column(db.String(120), unique=False, nullable=True)

    # Many to many relation
    student_courses = db.relationship(
        "User", secondary=student_course_linker, lazy='subquery',
        backref=db.backref('student_courses', lazy=True))

    ta_courses = db.relationship(
        "User", secondary=ta_course_linker, lazy='subquery',
        backref=db.backref('ta_courses', lazy=True))

    labels = db.relationship(
        "Label", secondary=label_course_linker, lazy='subquery',
        backref=db.backref('labels', lazy=True))

    supervisors = db.relationship(
        "User", secondary=supervisor_linker, lazy='subquery',
        backref=db.backref('supervisors', lazy=True))

    # Dit is een soort toString zoals in Java, voor het gebruiken van de
    # database in de commandline. Op die manier kan je data maken en weergeven
    # zonder formulier.
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
            'course_email': self.course_email,
            'title': self.title,
            'description': self.description,
            'tas': [ta.serialize for ta in self.ta_courses],
            'supervisors': [suvi.serialize for suvi in self.supervisors]
        }

    @property
    def checkValid(self):
        """
        Checks if an object is valid to insert into a database. So all
        fields that should be set, are set. If a value is not set, throw
        for now a ValueError().
        """
        pass


class CoursePlugin(db.Model):
    """
    Keeps track of enabled plugins for each course.
    """
    id = db.Column(UUIDType(binary=False), primary_key=True)
    plugin = db.Column(db.String(255), unique=False, nullable=False)
    active = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    course_id = db.Column(UUIDType(binary=False), db.ForeignKey(
        'course.id'), nullable=False, default='asdf')

    course = db.relationship('Course', lazy=True, backref=db.backref('plugins'))

    # TODO: Add settings
