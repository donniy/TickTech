from datetime import datetime
from flaskr import database
from sqlalchemy_utils import UUIDType
from flaskr.config import Config

db = database.db

unread_messages_linker = db.Table(
    'unread_link_user',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'),
              primary_key=True),
    db.Column('message_id', db.Integer, db.ForeignKey('message.id'),
              primary_key=True)
)


class Message(db.Model):
    """
    Een message.
    """

    # Enum workaround
    NTFY_TYPE_MESSAGE = 0
    NTFY_TYPE_STATUS = 1
    NTFY_TYPE_CLOSED = 2
    NTFY_TYPE_NEW = 3
    NTFY_LVL_UP = 4
    NTFY_LVLS_UP = 5
    NTFY_LVL_DWN = 6
    NTFY_LVLS_DWN = 7

    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(UUIDType(binary=False), db.ForeignKey('ticket.id'),
                          default=0, nullable=False)
    n_type = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    reply_id = db.Column(db.Integer, nullable=True)

    ticket = db.relationship('Ticket',
                             backref=db.backref('messages', lazy=True))

    sender = db.relationship('User',
                             backref=db.backref('messages', lazy=True))

    recipients = db.relationship('User', secondary=unread_messages_linker,
                                 backref=db.backref('unread', lazy='subquery'))

    def __repr__(self):
        """
        Dit is een soort toString zoals in Java, voor het gebruiken van de
        database in de commandline. Op die manier kan je data maken en
        weergeven zonder formulier.
        """
        return '<{} {}: {}>'.format(self.readable_type, self.id, self.text)

    @property
    def serialize(self):
        """
        Zet de message om in json. Dit is alles wat de front-end kan zien,
        dus zorg dat er geen gevoelige info in zit.
        """
        return {
            'id': self.id,
            'ticket': self.ticket.serialize,
            'type': self.n_type,
            'user_id': self.user_id,
            'user_name': self.sender.name,
            'text': self.text,
            'timestamp': self.timestamp,
            'reply_id': self.reply_id
        }

    @property
    def readable_type(self):
        """
        String variant of message type.
        """
        if self.n_type == Config.NTFY_TYPE_MESSAGE:
            return 'Message'
        elif self.n_type == Config.NTFY_TYPE_STATUS:
            return 'StatusMessage'
        elif self.n_type == Config.NTFY_TYPE_CLOSED:
            return 'ClosedMessage'
        elif self.n_type == Config.NTFY_TYPE_NEW:
            return 'NewTicketMessage'
        elif self.n_type == Config.NTFY_LVL_UP:
            return 'LevelUpMessage'
        elif self.n_type == Config.NTFY_LVLS_UP:
            return 'LevelsUpMessage'
        elif self.n_type == Config.NTFY_LVL_DWN:
            return 'LevelDownMessage'
        elif self.n_type == Config.NTFY_LVLS_DWN:
            return 'LevelsDownMessage'

    @property
    def checkValid(self):
        """
        This function appears not to do anything.
        """
        # TODO: Check if this is used anywhere and if possible remove.
        pass

    def __eq__(self, other):
        """
        Compare to another Message. Relies on uniqueness of id.
        """
        return self.id == other.id
