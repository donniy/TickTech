from flaskr import database, Iresponse
from flaskr.models.ticket import Ticket
from flask import escape
import flaskr.utils.notifications as notifications
from flaskr.models.Message import Message
from flaskr.models.Course import Course
from flaskr.models.user import User
from flaskr.request_processing import levels


def create_request(jsonData, ticket_id):
    """
    Function that handles the create request from a ticket.
    """
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
        if user_id != ticket.user_id:
            notification = notifications.notify(user_id,
                                                ticket,
                                                text,
                                                Message.NTFY_TYPE_MESSAGE)
            notification = notification

        # Add experience if its a teaching assistant who is commenting.
        user = User.query.get(user_id)
        course = Course.query.get(ticket.course_id)
        if user in course.ta_courses:
            level_up = levels.add_experience(levels.EXP_FOR_RESPONSE, user_id)
            levels.notify_level_change(user_id, ticket, level_up)
    except Exception as e:
        return Iresponse.create_response(str(e), 400)

    return Iresponse.create_response("", 201)


def retrieve_all_request(ticket_id, for_user, read=False):
    """
    Function that handle the request that retrieves
    the messages of a ticket. In order to be able
    to get the messages, a user needs to have atleast
    rights for the ticket.
    """
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
