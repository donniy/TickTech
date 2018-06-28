from flaskr import database, Iresponse
from flask import escape
import uuid
from flaskr.models.Note import Note
from flaskr.models.ticket import Ticket
from flaskr.models.Course import Course
from flaskr.request_processing import levels
from datetime import datetime
import re


def retrieve_all_request(ticket_id):
    """
    Process the request to receive all notes of a certain ticket.
    """
    notes = Note.query.filter_by(ticket_id=ticket_id).all()
    if len(notes) == 0:
        return Iresponse.create_response("", 404)

    return Iresponse.create_response(database.serialize_list(notes), 200)


# Catch datbase session commit exceptions.
# Maybe make a different call in the database file.
# TODO: Add error handling when a TA is not found.
def parse_note(message, ticket):
    """
    Function that parses a note for mentioned users.
    If a user is mentioned we append them to the
    linked tas in the ticket.
    """
    mentions = re.finditer('@[0-9]+', message)
    course = Course.query.get(ticket.course_id)
    if course is None:
        return

    ta_in_course = course.ta_courses
    for mention in mentions:
        user_id = mention.group(0).split('@')[1]

        for ta in ta_in_course:
            if str(ta.id) == user_id:
                if ta in ticket.bound_tas:
                    continue
                ticket.bound_tas.append(ta)
                level_up = levels.add_experience(levels.EXP_FOR_MENTION, ta.id)
                levels.notify_level_change(ta.id, None, level_up)
                database.db.session.commit()


# TODO: Add checking to getting data from json.
def create_request(jsonData):
    """
    Process the request to create a node.
    """
    ticket_id = escape(jsonData["ticket_id"])
    user_id = escape(jsonData["user_id"])
    message = escape(jsonData["text"])

    response_body = {}

    if message == '':
        response_body['message'] = "empty message"

    if ticket_id == '':
        response_body['ticket_id'] = "No ticket id has been supplied"

    if user_id == '':
        response_body['user_id'] = "No user id has been supplieds"

    ticket = Ticket.query.get(ticket_id)
    if ticket is None:
        response_body['ticket'] = "No ticket exists with this id"

    if len(response_body) != 0:
        return Iresponse.create_response(response_body, 400)

    note = Note()
    note.id = uuid.uuid4()
    note.user_id = user_id
    note.ticket_id = ticket_id
    note.text = message
    note.timestamp = datetime.now()

    if not database.addItemSafelyToDB(note):
        return Iresponse.internal_server_error()

    parse_note(message, ticket)
    levels.add_experience(levels.EXP_FOR_NOTE, note.user_id)
    # add header location.
    return Iresponse.create_response(note.serialize, 201)


def delete_request(note_id):
    """
    Process the request to delete a note.
    """
    note = Note.query.get(note_id)
    if note is None:
        return Iresponse.create_response("", 404)
    try:
        levels.deduct_experience(levels.EXP_FOR_NOTE, note.user_id)
        database.db.session.delete(note)
        database.db.session.commit()
    except Exception:
        print("LOG: Deleting error")
        return Iresponse.internal_server_error()
    return Iresponse.create_response("", 202)
