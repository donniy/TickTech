from datetime import datetime
from flaskr import database

db = database.db

class Note(db.Model):
    """
    Een notitie.
    """
    note_id = db.Column(db.Integer, primary_key=True)

    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), default=0, nullable=False)
    # message_id = db.Column(db.Integer, db.ForeignKey('message.message_id'), default=0,nullable=True)

    user_id = db.Column(db.Integer, nullable=False)

    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    ticket = db.relationship('Ticket', backref=db.backref('notes', lazy=True))
    # message = db.relationship('Message', backref=db.backref('notes',lazy=True))

    def __repr__(self):
        return '<Note {}>'.format(self.note_id)

    @property
    def serialize(self):
        return {
            'note_id': self.note_id,
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
