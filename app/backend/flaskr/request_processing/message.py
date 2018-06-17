from flaskr import database, Iresponse
from flaskr.models.ticket import *
from flask import jsonify, escape
import uuid
import flaskr.utils.notifications as notifications
from flaskr.models.Message import *
from flaskr import socketio


def create_request(jsonData, ticket_id):
    user_id = escape(jsonData["studentid"])
    text = escape(jsonData["message"])

    response_body = {}

    if text == '':
        response_body['message'] = "empty message"

    ticket = Ticket.query.get(ticket_id)
    if ticket is None:
        response_body['ticket'] = "No ticket exists with this id"

    if len(response_body) != 0:
        return Iresponse.create_response(response_body, 400)

#    print(ticket.id)
#    message = Message()
#    message.ticket_id = ticket.id
#    message.user_id = user_id
#    message.text = text
#    if not database.addItemSafelyToDB(message):
#        return Iresponse.internal_server_error()
#
#    room = "ticket-messages-{}".format(ticket_id)
#    socketio.emit('messageAdded',
#                  {'text': message.text, 'user_id': message.user_id},
#                  room=room)
    try:
        notification = notifications.notify(user_id,
                                            ticket,
                                            text,
                                            Message.NTFY_TYPE_MESSAGE)
    except Exception as e:
        return Iresponse.create_response(str(e), 400)

    return Iresponse.create_response("", 201)


def retrieve_all_request(ticket_id):
    body = {}
    ticket = Ticket.query.get(ticket_id)
    if ticket is None:
        body['ticket_id'] = "invalid"
        return Iresponse.create_response(body, 404)
    messages = database.serialize_list(list(ticket.messages))
    print(messages)
    return Iresponse.create_response(messages, 200)
