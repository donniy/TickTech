from flaskr.models.Message import Message
from flaskr.models.user import User
from flaskr import socketio
from flaskr import database


def notify(sender_id, ticket, text, n_type, initial=False):
    """
    Notify everyone in a ticket.
    """
    verbose = False  # Set to True for debugging

    user = User.query.get(sender_id)
    message = Message()
    message.ticket_id = ticket.id
    message.text = text
    message.n_type = n_type
    message.user_id = sender_id

    # We have to remove te owner from the related users in order to
    # notify everyone this message is targeted at.
    us = ticket.related_users
    if verbose:
        print("Users related to ticket:")
        for u in us:
            print(" - {}".format(u.name))
        print("----------------\n\n")

    if user in us:
        us.remove(user)

    if verbose:
        print("Users to notify: {}".format(len(us)))
        for u in us:
            print(" - {}".format(u.name))
        print("----------------\n\n")

    if len(us):
        if verbose:
            print("Adding recipients to unread table... ", end="")
        try:
            message.recipients.extend(list(us))
        except Exception as e:
            if verbose:
                print("Failed..")
                print(e)
            raise Exception("Could not add recipients")

        if verbose:
            print("Done!")
    else:
        if verbose:
            print("No recipients, skip adding")

    if verbose:
        print("Inserting into database")
    if not database.addItemSafelyToDB(message):
        if verbose:
            print("Failed to insert into database.")
        raise Exception("Could not create message")
    if verbose:
        print("Successfully inserted into database")

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
                    .format(message.text[:40],
                            '...' if len(message.text) > 40 else ''),
                    'ticket': str(ticket.id),
                    'ticket_owner': str(ticket.owner.id),
                    'sender': user.serialize,
                    'initial': initial,
                    'ticket_title': "{}{}"
                    .format(ticket.title[:40],
                            '...' if len(ticket.title) > 40 else ''),
                    'type': n_type}

    # We need to notify everyone related to the course. For this,
    # we use the user set we made earlier.
    for u in us:
        u.notify(notification)

    return message
