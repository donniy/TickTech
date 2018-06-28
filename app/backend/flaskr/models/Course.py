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
    A course class which specifies the course model.
    """
    id = db.Column(UUIDType(binary=False), primary_key=True)
    title = db.Column(db.String(255), unique=False, nullable=False)
    description = db.Column(db.Text, nullable=True)

    # TODO: controle length of data
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
        backref=db.backref('supervisor_courses', lazy=True))

    def __repr__(self):
        """
        Function that will state how the object is
        displayed when printed to the console.
        Like a toString() method in Java.
        """
        return '<Course {}>'.format(self.title)

    @property
    def serialize(self):
        """
        Transforms the object into a json object.
        This will be used at the front-end, so dont include
        sensitive information in the json object.
        """
        return {
            'id': self.id,
            'course_email': self.course_email,
            'title': self.title,
            'description': self.description,
            'tas': [ta.serialize for ta in self.ta_courses],
            'supervisors': [suvi.serialize for suvi in self.supervisors]
        }

    def create(self, id, name, desc, mail, url, port, password):
        self.id = id
        self.title = name
        self.description = desc
        self.course_email = mail
