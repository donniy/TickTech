from flaskr.models.Message import *
from flaskr.models.user import *
from flaskr import socketio


def notify(sender_id, ticket, text, n_type, initial=False):
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
        print("oh no something went wrong")
        raise Exception("Could not create message")

    # Place the notification in the ticket overview for everyone
    # present in that room.
    socketio.emit('messageAdded',
                  {'text': message.text,
                   'user_id':  user.id,
                   'user_name': user.name,
                   'type': message.n_type},
                  room='ticket-messages-{}'
                  .format(message.ticket_id))

    notification = {'text': "{}{}"
                    .format(user.name, message.text[:40],
                    '...' if len(message.text) > 40 else ''),
                    'ticket': str(ticket.id),
                    'ticket_owner': str(ticket.owner.id),
                    'sender': user.serialize,
                    'initial': initial,
                    'type': n_type}

    # We need to notify everyone related to the course. For this,
    # we first retrieve all related users. After that, we remove
    # the sender (:user:) if it is present in the list. Now we
    # have everyone who needs to be notified and we can notify
    # them with the notify function on the user model.
    us = ticket.related_users
    print("Users related to ticket:")
    for u in us:
        print(" - {}".format(u.name))
    if user in us:
        us.remove(user)

    print("Users to notify:")
    for u in us:
        print(" - {}".format(u.name))
        u.notify(notification)

    return message
