from datetime import datetime
from flaskr import database
from sqlalchemy_utils import UUIDType

db = database.db

bound_tas_helper = db.Table(
    'ta_tracker',
    db.Column('ticket_id', UUIDType(binary=False),
              db.ForeignKey('ticket.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'),
              primary_key=True)
)

ticket_files_helper = db.Table(
    'ticket_files',
    db.Column('file_id', UUIDType(binary=False),
              db.ForeignKey('files.file_id'), unique=False, primary_key=True),
    db.Column('ticket_id', UUIDType(binary=False),
              db.ForeignKey('ticket.id'), primary_key=True),
)


class Ticket(db.Model):

    """
    This is the class that specifies the model for a ticket.
    A ticket is created when a user has a question. The ticket
    will then own multiple entities, like notes and messages.
    The ticket is a container class for a question.
    """
    id = db.Column(UUIDType(binary=False), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(UUIDType(binary=False),
                          db.ForeignKey('course.id'),
                          unique=False,
                          nullable=False)

    ta_id = db.Column(db.Integer, nullable=True)

    status_id = db.Column(db.Integer, db.ForeignKey(
        'ticket_status.id'), default=0, nullable=False)

    email = db.Column(db.String(120), unique=False, nullable=True)
    title = db.Column(db.String(255), unique=False, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    label_id = db.Column(
        UUIDType(binary=False), db.ForeignKey('label.label_id'), unique=False,
        nullable=True)

    label = db.relationship('Label',
                            backref=db.backref('tickets', lazy=True))
    course = db.relationship('Course',
                             backref=db.backref('tickets', lazy=False))

    bound_tas = db.relationship(
        "User", secondary=bound_tas_helper, lazy='subquery',
        backref=db.backref('ta_tickets', lazy=True)
    )

    # Many to many relationship
    owner = db.relationship(
        "User", backref=db.backref('created_tickets', lazy=True))

    # Many to many relationship
    files = db.relationship(
        "File", secondary=ticket_files_helper, lazy='subquery',
        backref=db.backref('tickets', lazy=True))

    def __repr__(self):
        return '<Ticket {}>'.format(self.title)

    @property
    def serialize(self):
        """
        Ticket can be unassigned, so teaching assistant id can be None.
        Transforms the object into a json object.
        This will be used at the front-end, so dont include
        sensitive information in the json object.
        """
        if self.ta_id is None:
            self.ta_id = "null"

        if self.label_id is None:
            serialized_label = {}
        else:
            serialized_label = self.label.serialize

        return {
            'id': self.id,
            'user_id': self.user_id,
            'course_id': self.course_id,
            'course': self.course.serialize,
            'ta_id': self.ta_id,
            'email': self.email,
            'title': self.title,
            'timestamp': self.timestamp,
            'status': self.ticket_status.serialize,
            'label': serialized_label,
            'tas': database.serialize_list(self.bound_tas),
            'files': database.serialize_list(self.files)
        }

    @property
    def close(self):
        # id 2 is the closed status
        closed_status = TicketStatus.query.filter_by(id=2).first()
        if closed_status is None:
            return
        self.status_id = closed_status.id

    @property
    def assign(self):
        # ID 3 is the assigned status.
        assign_status = TicketStatus.query.filter_by(id=3).first()
        if assign_status is None:
            return
        self.status_id = assign_status.id

    @property
    def help(self):
        # id 4 is the helping status
        help_status = TicketStatus.query.filter_by(id=4).first()
        if help_status is None:
            return
        self.status_id = help_status.id

    @property
    def related_users(self):
        """
        Returns all users that are somehow related to this
        ticket. That means, all teaching assistants and the student that
        created this ticket.
        """
        tmp = [self.owner]
        tmp.extend(self.bound_tas)
        return set(tmp)

    def __eq__(self, other):
        """
        Compare two instances of this model. Note that this only
        compares the id's since it assumes both models were retrieved
        from the database (primary keys are unique).
        """
        return self.id == other.id


class TicketStatus(db.Model):
    """
    The ticket status that can be set
    Pre-defined statuses:
    1.  Unassigned
    2.  Closed
    3.  Assigned but waiting for reply
    4.  Receiving help
    Use LabelA == LabelB for comparison instead of text comparison
    """

    unassigned = 1
    closed = 2
    waiting_for_help = 3
    receiving_help = 4

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, default="Pending")

    tickets = db.relationship(
        'Ticket', backref=db.backref('ticket_status', lazy=False))

    @property
    def serialize(self):
        """
        Transforms the object into a json object.
        This will be used at the front-end, so dont include
        sensitive information in the json object.
        """
        return {
            'id': self.id,
            'name': self.name
        }

    @property
    def checkValid(self):
        pass

    def __eq__(self, other):
        """
        Set the == and != behavior.
        """
        return self.id == other.id


class TicketLabel(db.Model):

    """
    Label on a ticket.
    """
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(UUIDType(binary=False), unique=False, nullable=True)
    course_id = db.Column(UUIDType(binary=False), unique=False, nullable=False)
    name = db.Column(db.String(50), nullable=False)

    @property
    def serialize(self):
        """
        Transforms the object into a json object.
        This will be used at the front-end, so dont include
        sensitive information in the json object.
        """
        return {
            'id': self.id,
            'course_id': self.course_id,
            'name': self.name
        }

    @property
    def checkValid(self):
        pass


class File(db.Model):
    """
    A File.
    """

    __tablename__ = 'files'
    file_location = db.Column(db.Text, unique=False, nullable=False,
                              primary_key=True)
    file_name = db.Column(db.Text, unique=False, nullable=False)
    file_id = db.Column(UUIDType(binary=False), primary_key=True)
    is_duplicate = db.Column(db.Boolean, default=False, nullable=False)
    is_ocrable = db.Column(db.Boolean, default=False, nullable=False)

    @property
    def serialize(self):
        """
        Transforms the object into a json object.
        This will be used at the front-end, so dont include
        sensitive information in the json object.
        """
        return {
            'file_location': self.file_location,
            'file_name': self.file_name,
            'is_duplicate': self.is_duplicate,
            'is_ocrable': self.is_ocrable
        }

    @property
    def checkValid(self):
        pass
