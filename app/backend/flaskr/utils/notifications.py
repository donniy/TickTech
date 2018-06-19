from flaskr.models.Message import *
from flaskr.models.user import *
from flaskr import socketio


def notify(sender_id, ticket, text, n_type):
    """
    Notify everyone in a ticket.
    """
    print("#########################################")
    print("# I will notify that something happened #")
    print("#########################################")
    user = User.query.get(sender_id)
    message = Message()
    message.ticket_id = ticket.id
    message.text = text
    message.n_type = n_type
    message.user_id = sender_id

    if not database.addItemSafelyToDB(message):
        print("oh no something went wrong")
        raise Exception("Could not create message")

    # Place the notification in the ticket overview for everyone
    # present in that room.
    print("#")
    print("# First send message to ticket chat")
    socketio.emit('messageAdded',
                  {'text': message.text,
                   'user_id':  user.id,
                   'user_name': user.name,
                   'type': message.n_type},
                  room='ticket-messages-{}'
                  .format(message.ticket_id))

    notification = {'text': "{}: {}{}"
                    .format(user.name, message.text[:40],
                    '...' if len(message.text) > 40 else ''),
                    'ticket': str(ticket.id)}

    # TODO: For now, we always notify Erik. This needs to be changed.
    print("#\n# Ticket info:")
    print("# ------------\n# Sender: {}".format(user.name))
    us = ticket.related_users

    print("# All users related to course:")
    for u in us:
        print("#  - {}".format(u.name))

    if user in us:
        us.remove(user)

    print("# Users to notify:")
    for u in us:
        print("#  - {}".format(u.name))
        u.notify(notification)

    return message
