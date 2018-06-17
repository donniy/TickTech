from flaskr import database, Iresponse
from flask import jsonify, escape
import uuid
from flaskr.models.ticket import *
from flaskr.models.Message import *
from flaskr.utils import notifications


def create_request(jsonData):
    name = escape(jsonData["name"])
    studentid = escape(jsonData["studentid"])
    email = escape(jsonData["email"])
    subject = escape(jsonData["subject"])
    message = escape(jsonData["message"])
    courseid = escape(jsonData["courseid"])
    labelid = escape(jsonData["labelid"])

    response_body = {}

    ticket = Ticket(id=uuid.uuid4(), user_id=studentid, course_id=courseid,
                    status_id=1, title=subject, email=email,
                    timestamp=datetime.now())

    if not database.addItemSafelyToDB(ticket):
        return Iresponse.internal_server_error()

    try:
        msg = notifications.notify(studentid,
                                   ticket,
                                   message,
                                   Message.NTFY_TYPE_MESSAGE)
    except Exception as e:
        raise e
        return Iresponse.create_response(str(e), 400)
#    new_message = Message(ticket_id=ticket.id, user_id=studentid,
#                          text=message, timestamp=datetime.now(),
#                          ticket=ticket)
#    if not database.addItemSafelyToDB(new_message):
#        return Iresponse.internal_server_error()

    response_body['ticketid'] = ticket.id
    response = Iresponse.create_response(response_body, 201)
    response.headers.add('Location', 'api/ticket/{0}'.format(ticket.id))
    return response
