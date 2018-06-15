from flaskr.models.Message import *
from flaskr.models.user import *
from flaskr import socketio

def notify(sender_id, ticket, text, n_type):
    """
    Notify everyone in a ticket.
    """
    user = User.query.get(sender_id)
    message = Message()
    message.ticket_id = ticket.id
    message.text = text
    message.n_type = n_type
    message.user_id = sender_id

    if not database.addItemSafelyToDB(message):
        raise Exception("Could not create message")

    # Place the notification in the ticket overview for everyone
    # present in that room.
    socketio.emit('messageAdded',
            {'text': message.text, 'user_id':  user.id, 'user_name': user.name, 'type': message.n_type}, room='ticket-messages-{}'.format(message.ticket_id))

    # TODO: Notify everyone via a private websocket.

    return message
