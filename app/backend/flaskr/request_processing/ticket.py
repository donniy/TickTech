from flaskr import database, Iresponse
from flask import escape
import uuid
from flaskr.request_processing import levels
from flaskr.models.ticket import Ticket, TicketStatus
from flaskr.models.user import User
from flaskr.models.Label import Label
from flaskr.models.Message import Message
from flaskr.utils import notifications
from datetime import datetime


# TODO: CHECK IF JSON IS VALID.
def create_request(json_data):
    name = escape(json_data["name"])
    name = name  # flake8
    studentid = escape(json_data["studentid"])
    email = escape(json_data["email"])
    subject = escape(json_data["subject"])
    message = escape(json_data["message"])
    courseid = escape(json_data["courseid"])
    labelid = escape(json_data["labelid"])
    files = json_data['files']

    response_body = {}

    bound_tas = list()
    label = None

    if labelid != "":
        label = Label.query.get(uuid.UUID(labelid))
        bound_tas = get_label_tas(label)

    if len(bound_tas) < 1:
        status_id = 1
    else:
        status_id = 3

    print(status_id)

    ticket = Ticket(id=uuid.uuid4(), user_id=studentid, course_id=courseid,
                    status_id=status_id, title=subject, email=email,
                    label=label, files=files, timestamp=datetime.now())

    for ta in bound_tas:
        ticket.bound_tas.append(ta)
        level_up = levels.add_experience(levels.EXP_FOR_ASSING, ta.id)
        levels.notify_level_change(ta.id, None, level_up)

    if not database.addItemSafelyToDB(ticket):
        return Iresponse.internal_server_error()

    try:
        msg = notifications.notify(studentid,
                                   ticket,
                                   message,
                                   Message.NTFY_TYPE_MESSAGE)
        msg = msg  # flake8
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


# TODO: Should check is the json_data is valid.
def add_ta_to_ticket(json_data):
    ticket = Ticket.query.filter_by(
        id=uuid.UUID(json_data['ticketid'])).first()
    ta = User.query.filter_by(id=json_data['taid']).first()

    # Check if the ta and ticket were found and add if not already there.
    if ticket and ta:
        if ta not in ticket.bound_tas:
            ticket.bound_tas.append(ta)
            ticket.status_id = 4
            database.db.session.commit()
            level_up = levels.add_experience(levels.EXP_FOR_ASSING, ta.id)
            levels.notify_level_change(ta.id, ticket, level_up)
            return Iresponse.create_response({'ta': ta.serialize,
                                             'status': "Assigned"},
                                             200)
        return Iresponse.create_response({'status': "OK"}, 201)
    return Iresponse.create_response("Failure", 400)


# TODO: CHECK IF JSON IS VALID.
def remove_ta_from_ticket(json_data):
    ticket = Ticket.get(uuid.UUID(json_data['ticketid']))
    ta = User.query.filter_by(id=json_data['taid']).first()

    if ticket and ta:
        if ta in ticket.bound_tas:
            ticket.bound_tas.remove(ta)
            return Iresponse.create_response("Success", 200)
    return Iresponse.create_response("Failure", 400)


def get_label_tas(label):
    if label:
        tas_by_label = label.users
        return tas_by_label
    return None


def close_ticket(ticket):
    if ticket:
        ticket.status_id = 2
        database.db.session.commit()
        return "Closed"
