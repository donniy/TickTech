from flask import current_app, g
from flask import Flask, render_template, jsonify
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def init_db():
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    return db


def json_list(l):
    """
    Maak JSON van de lijst.
    """
    return jsonify(json_list=[i.serialize for i in l])

class Ticket(db.Model):
    """
    Een ticket.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=True)
    course_id = db.Column(db.String(120), unique=False, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('ticket_status.id'), default=0, nullable=False)
    title = db.Column(db.String(255), unique=False, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Dit is hoe je een relatie maakt. ticket.status geeft een TicketStatus object met
    # de status van dit ticket. backref betekent: maak een veld 'tickets' op TicketStatus
    # wat een lijst met alle tickets met die status teruggeeft.
    status = db.relationship('TicketStatus', backref=db.backref('tickets', lazy=True))

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


class Message(db.Model):
    """
    Een message.
    """
    message_id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), default=0, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    reply_id = db.Column(db.Integer, nullable=True)

    ticket = db.relationship('Ticket', backref=db.backref('messages', lazy=True))

    # Dit is een soort toString zoals in Java, voor het gebruiken van de database
    # in de commandline. Op die manier kan je data maken en weergeven zonder formulier.
    def __repr__(self):
        return '<Message {}>'.format(self.message_id)

    @property
    def serialize(self):
        """
        Zet de message om in json. Dit is alles wat de front-end kan zien,
        dus zorg dat er geen gevoelige info in zit.
        """
        return {
            'message_id': self.message_id,
            'ticket_id': self.ticket_id,
            'user_id': self.user_id,
            'message': self.message,
            'timestamp': self.timestamp,
            'reply_id': self.reply_id
        }