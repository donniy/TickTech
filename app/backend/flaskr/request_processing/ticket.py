from flaskr import database, Iresponse
from flask import jsonify, escape
import uuid
from flaskr.models.ticket import *
from flaskr.models.Message import *


def create_request(jsonData):
    name = escape(jsonData["name"])
    studentid = escape(jsonData["studentid"])
    email = escape(jsonData["email"])
    subject = escape(jsonData["subject"])
    message = escape(jsonData["message"])
    courseid = escape(jsonData["courseid"])
    labelid = escape(jsonData["labelid"])

    response_body = {}

    for letter in name:
        if not letter.isalpha() and not letter in " '-":
            response_body['name'] = 'Invalid name'

    #TODO implement check validation email (is it even possible?)

    # A number should be within certain bounds and only numerical.
    try:
        studentid_num = int(studentid)
        if studentid_num < 10000 or studentid_num > 999999999:
            response_body['student_id'] = 'Invalid'
    except ValueError:
        response_body['student_id'] = 'Invalid'

    if len(subject) > 50:
        response_body['subject'] = 'Too big'

    # Course and labelid shoudl be valid (Implement through server checking)

    #TODO implement LTI checking for course/student accessability and validity.

    # Message should not be empty.
    if len(message) == 0:
        response_body['message'] = 'Empty'

    #status = TicketStatus.query.get(1)
    #if status is None:
        #response_body['status'] = 'Invalid status'

    if len(response_body) != 0:
        return Iresponse.create_response(response_body, 400)

    ticket = Ticket(id=uuid.uuid4(), user_id=studentid, course_id=courseid,
                    status_id=1, title=subject, email=email,
                    timestamp=datetime.now())

    if not database.addItemSafelyToDB(ticket):
        return Iresponse.internal_server_error()

    new_message = Message(ticket_id=ticket.id, user_id=studentid,
                          text=message, timestamp=datetime.now(),
                          ticket=ticket)
    if not database.addItemSafelyToDB(new_message):
        return Iresponse.internal_server_error()

    response_body['ticketid'] = ticket.id
    response = Iresponse.create_response(response_body, 201)
    response.headers.add('Location', 'api/ticket/{0}'.format(ticket.id))
    return response
