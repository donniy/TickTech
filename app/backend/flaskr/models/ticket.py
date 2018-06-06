from datetime import datetime
from flaskr import database

db = database.db


class Ticket(db.Model):
    """
    Een ticket.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.String(120), unique=False, nullable=False)

    status_id = db.Column(db.Integer, db.ForeignKey(
        'ticket_status.id'), default=0, nullable=False)
    label_id = db.Column(db.Integer, db.ForeignKey(
        'ticket_label.id'), default=0, nullable=False)

    email = db.Column(db.String(120), unique=False, nullable=True)
    title = db.Column(db.String(255), unique=False, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Dit is hoe je een relatie maakt. ticket.status geeft een TicketStatus object met
    # de status van dit ticket. backref betekent: maak een veld 'tickets' op TicketStatus
    # wat een lijst met alle tickets met die status teruggeeft.
    status = db.relationship(
        'TicketStatus', backref=db.backref('tickets', lazy=True))

    # Zie status hierboven, labelvariant van gemaakt.
    label = db.relationship(
        'TicketLabel', backref=db.backref('tickets', lazy=True))

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
            'label': self.label.serialize,
            'user_id': self.user_id
        }


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


class TicketLabel(db.Model):
    """
    Label van een ticket, die in kan worden gesteld.
    """
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Colum(db.Integer, unique=False, nullable=True)
    course_id = db.Column(db.String(120), unique=False, nullable=False)
    name = db.Column(db.String(50), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'ticket_id':  self.ticket_id,
            'course_id': self.course_id,
            'name': self.name
        }
