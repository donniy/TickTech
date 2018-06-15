from datetime import datetime
from flaskr import database
from sqlalchemy_utils import UUIDType

db = database.db


class Message(db.Model):

    NTFY_TYPE_MESSAGE = 0
    NTFY_TYPE_STATUS = 1
    NTFY_TYPE_CLOSED = 2
    NTFY_TYPE_NEW = 3

    """
    Een message.
    """
    message_id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(UUIDType(binary=False), db.ForeignKey('ticket.id'),
                          default=0, nullable=False)
    n_type = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    reply_id = db.Column(db.Integer, nullable=True)

    ticket = db.relationship('Ticket',
                             backref=db.backref('messages', lazy=True))

    user = db.relationship('User',
                             backref=db.backref('messages', lazy=True))

    # Dit is een soort toString zoals in Java, voor het gebruiken van de
    # database in de commandline. Op die manier kan je data maken en weergeven
    # zonder formulier.
    def __repr__(self):
        return '<Message {}>'.format(self.message_id)

    @property
    def serialize(self):
        """
        Zet de message om in json. Dit is alles wat de front-end kan zien,
        dus zorg dat er geen gevoelige info in zit.
        """
        return {
            'id': self.message_id,
            'ticket': self.ticket.serialize,
            'type': self.n_type,
            'user_id': self.user_id,
            'user_name': self.user.name,
            'text': self.text,
            'timestamp': self.timestamp,
            'reply_id': self.reply_id
        }

    @property
    def checkValid(self):
        pass
