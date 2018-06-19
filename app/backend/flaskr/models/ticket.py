from datetime import datetime
from flaskr import database
from sqlalchemy_utils import UUIDType
import uuid
import re
from flask import Response, jsonify, escape

db = database.db

binded_tas_helper = db.Table(
    'ta_tracker',
    db.Column('ticket_id', UUIDType(binary=False),
              db.ForeignKey('ticket.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'),
              primary_key=True)
)

labels_helper = db.Table(
    'labels',
    db.Column('label_id', db.Integer,
              db.ForeignKey('ticket_label.id'), primary_key=True),
    db.Column('ticket_id', db.Integer, db.ForeignKey('ticket.id'),
              primary_key=True)
)


class Ticket(db.Model):

    """
    Een ticket.
    """
    id = db.Column(UUIDType(binary=False), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(UUIDType(binary=False), unique=False, nullable=False)

    ta_id = db.Column(db.Integer, nullable=True)

    status_id = db.Column(db.Integer, db.ForeignKey(
        'ticket_status.id'), default=0, nullable=False)

    email = db.Column(db.String(120), unique=False, nullable=True)
    title = db.Column(db.String(255), unique=False, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Dit is hoe je een relatie maakt. ticket.status geeft een TicketStatus
    # object met de status van dit ticket. backref betekent: maak een veld
    # 'tickets' op TicketStatus wat een lijst met alle tickets met die status
    # teruggeeft.

    # status = db.relationship(
    #     'TicketStatus', backref=db.backref('tickets', lazy=False))

    binded_tas = db.relationship(
        "User", secondary=binded_tas_helper, lazy='subquery',
        backref=db.backref('ta_tickets', lazy=True)
    )

    owner = db.relationship(
            "User", backref=db.backref('created_tickets', lazy=True))

    # Many to many relation
    labels = db.relationship(
        "TicketLabel", secondary=labels_helper, lazy='subquery',
        backref=db.backref('tickets', lazy=True))

    # Dit is een soort toString zoals in Java, voor het gebruiken van de
    # database in de commandline. Op die manier kan je data maken en weergeven
    # zonder formulier.
    def __repr__(self):
        return '<Ticket {}>'.format(self.title)

    @property
    def serialize(self):
        """
        Ticket can be unassigned, so ta_id can be None.
        """
        if self.ta_id is None:
            self.ta_id = "null"

        return {
            'id': self.id,
            'user_id': self.user_id,
            'course_id': self.course_id,
            'ta_id': self.ta_id,
            'email': self.email,
            'title': self.title,
            'timestamp': self.timestamp,
            'status': self.ticket_status.serialize,
            'labels': database.serialize_list(self.labels),
            'tas': database.serialize_list(self.binded_tas)
        }

    @property
    def close(self):
        closed_status = TicketStatus.query.filter_by(name='closed').first()
        if closed_status is None:
            return
        self.status_id = closed_status.id

    @property
    def related_users(self):
        """
        Returns all users that are somehow related to this
        ticket. That means, all TA's and the student that
        created this ticket.
        """
        tmp = [self.owner]
        tmp.extend(self.binded_tas)
        print("Binded tas:")
        print(self.binded_tas)
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
    De status van een ticket die kan worden ingesteld.

    Pre-defined statuses:
    1.  Unassigned
    2.  Closed
    3.  Assigned but waiting for reply
    4.  Receiving help

    Use numbers for comparison instead of text comparison

    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, default="Pending")

    tickets = db.relationship(
        'Ticket', backref=db.backref('ticket_status', lazy=False))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }

    @property
    def checkValid(self):
        pass


class TicketLabel(db.Model):

    """
    Label van een ticket, die in kan worden gesteld.
    """
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(UUIDType(binary=False), unique=False, nullable=True)
    course_id = db.Column(UUIDType(binary=False), unique=False, nullable=False)
    name = db.Column(db.String(50), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'name': self.name
        }

    @property
    def checkValid(self):
        pass
