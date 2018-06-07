from datetime import datetime
from flaskr import database
from sqlalchemy_utils import UUIDType
import uuid

db = database.db

labels_helper = db.Table(
    'labels',
    db.Column('label_id', db.Integer, db.ForeignKey('ticket_label.id'), primary_key=True),
    db.Column('ticket_id', db.Integer, db.ForeignKey('ticket.id'), primary_key=True))


class Ticket(db.Model):
    """
    Een ticket.
    """
    id = db.Column(UUIDType(binary=False), primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.String(120), unique=False, nullable=False)

    status_id = db.Column(db.Integer, db.ForeignKey(
        'ticket_status.id'), default=0, nullable=False)

    email = db.Column(db.String(120), unique=False, nullable=True)
    title = db.Column(db.String(255), unique=False, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    # Dit is hoe je een relatie maakt. ticket.status geeft een TicketStatus object met
    # de status van dit ticket. backref betekent: maak een veld 'tickets' op TicketStatus
    # wat een lijst met alle tickets met die status teruggeeft.
    status = db.relationship(
        'TicketStatus', backref=db.backref('tickets', lazy=True))

    #Many to many relation
    labels = db.relationship(
        "TicketLabel", secondary=labels_helper, lazy='subquery',
        backref=db.backref('tickets', lazy=True))


    # Dit is een soort toString zoals in Java, voor het gebruiken van de database
    # in de commandline. Op die manier kan je data maken en weergeven zonder formulier.
    def __repr__(self):
        return '<Ticket {}>'.format(self.title)

    @property
    def serialize(self):
        """
        Zet dit ticket om in json. Dit is alles wat de front-end kan zien,
        dus zorg dat er geen gevoelige info in zit.
        """
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'title': self.title,
            'course_id': self.course_id,
            'status': self.status.serialize,
            'labels': database.serialize_list(self.labels),
            'user_id': self.user_id
        }


    @property
    def checkValid(self):
        """
        Checks if an object is valid to insert into a database. So all
        fields that should be set, are set. If a value is not set, throw
        for now a ValueError().
        """
        status = TicketStatus.query.get(self.status_id)
        if status is None:
            debug_message = "No valid status found with " + \
                            "status_id: {0}".format(self.status_id)

            db_error = database.DatabaseInsertException(debug_message)
            db_error.response_message = "TEST"
            raise db_error


    @property
    def close(self):
        closed_status = TicketStatus.query.filter_by(name='closed').first()
        if closed_status is None:
            return
        self.status_id = closed_status.id





class TicketStatus(db.Model):
    """
    De status van een ticket die kan worden ingesteld.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

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
    course_id = db.Column(db.String(120), unique=False, nullable=False)
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
