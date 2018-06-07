from datetime import datetime
from flaskr import database
from sqlalchemy_utils import UUIDType
import uuid

db = database.db

class Note(db.Model):
    """
    Een notitie.
    """
    id = db.Column(UUIDType(binary=False), primary_key=True)

    ticket_id = db.Column(UUIDType(binary=False),db.ForeignKey('ticket.id'), unique=False, nullable=True)
    # message_id = db.Column(db.Integer, db.ForeignKey('message.message_id'), default=0,nullable=True)

    user_id = db.Column(db.Integer, nullable=False)

    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    ticket = db.relationship('Ticket', backref=db.backref('notes', lazy=False))
    # message = db.relationship('Message', backref=db.backref('notes',lazy=True))

    def __repr__(self):
        return '<Note {}>'.format(self.id)

    @property
    def serialize(self):
        return {
            'id': self.id,
            # 'message_id': self.message_id,
            'ticket_id': self.ticket_id,
            'user_id': self.user_id,
            'text': self.text,
            'timestamp': self.timestamp
        }


    @property
    def checkValid(self):
        """
        Checks if an object is valid to insert into a database. So all
        fields that should be set, are set. If a value is not set, throw
        for now a ValueError().
        """
        pass
