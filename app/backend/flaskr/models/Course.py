from datetime import datetime
from flaskr import database, plugins
from sqlalchemy_utils import UUIDType
from sqlalchemy.ext.mutable import MutableDict
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

    supervisors = db.relationship(
        "User", secondary=supervisor_linker, lazy='subquery',
        backref=db.backref('supervisors', lazy=True))

    # Dit is een soort toString zoals in Java, voor het gebruiken van de
    # database in de commandline. Op die manier kan je data maken en weergeven
    # zonder formulier.
    def __repr__(self):
        return '<Course {}>'.format(self.title)

    def get_plugin(self, plugin_id):
        """
        Get the given plugin.
        """
        for cp in self.plugins:
            if cp.plugin == plugin_id:
                return cp
        return None

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

    # Make sure changes in the pickled dict get detected so use a MutableDict.
    settings = db.Column(MutableDict.as_mutable(db.PickleType),
                         unique=False,
                         nullable=True)

    course = db.relationship('Course',
                             lazy=True,
                             backref=db.backref('plugins'))

    def __repr__(self):
        return "<CoursePlugin: {}>".format(self.plugin)

    def __hash__(self):
        return hash(str(self))

    def get_settings(self):
        """
        Returns the settings of this plugin, along with the types and
        descriptions of each setting.
        """
        p = plugins.get_plugin(self.plugin)
        course_settings = p.course_settings
        for setting, props in course_settings.items():
            if self.settings and setting in self.settings:
                props['value'] = self.settings[setting]
            else:
                props['value'] = props['default']
        return p.course_settings

    def get_setting_values(self):
        """
        Returns a simple key: value pair for each setting listing only
        the values and not all other properties of a setting.
        """
        return {k: v['value'] for k, v in self.get_settings().items()}

    def __eq__(self, other):
        """
        Compare this plugin to another plugin. For compatibility to labels
        only the name of the plugin is used.
        """
        return self.plugin == other.plugin
