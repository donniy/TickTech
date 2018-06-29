from datetime import datetime
from flaskr import database
from sqlalchemy_utils import UUIDType

db = database.db


class Note(db.Model):

    """
    This is the class that specifies the model for the Note.
    A note is a way of communicating between teaching assistants on a ticket.
    """
    id = db.Column(UUIDType(binary=False), primary_key=True)

    ticket_id = db.Column(
        UUIDType(binary=False), db.ForeignKey('ticket.id'), unique=False,
        nullable=True)

    user_id = db.Column(db.Integer, nullable=False)

    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    ticket = db.relationship('Ticket', backref=db.backref('notes', lazy=False))

    def __repr__(self):
        """
        Function that will state how the object is
        displayed when printed to the console.
        Like a toString() method in Java.
        """
        return '<Note {}>'.format(self.id)

    @property
    def serialize(self):
        """
        Transforms the object into a json object.
        This will be used at the front-end, so dont include
        sensitive information in the json object.
        """
        return {
            'id': self.id,
            'ticket_id': self.ticket_id,
            'user_id': self.user_id,
            'text': self.text,
            'timestamp': self.timestamp
        }
