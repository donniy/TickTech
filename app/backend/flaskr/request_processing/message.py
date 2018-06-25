from flaskr import database, Iresponse
from flaskr.models.ticket import Ticket
from flask import escape
import flaskr.utils.notifications as notifications
from flaskr.models.Message import Message


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

    try:
        notification = notifications.notify(user_id,
                                            ticket,
                                            text,
                                            Message.NTFY_TYPE_MESSAGE)
        notification = notification  # flake8
    except Exception as e:
        return Iresponse.create_response(str(e), 400)

    return Iresponse.create_response("", 201)


def retrieve_all_request(ticket_id, for_user, read=False):
    body = {}
    ticket = Ticket.query.get(ticket_id)
    if ticket is None:
        body['ticket_id'] = "invalid"
        return Iresponse.create_response(body, 404)

    msgs = list(ticket.messages)

    if read:
        for_user.read_messages(msgs)

    messages = database.serialize_list(msgs)
    return Iresponse.create_response(messages, 200)
