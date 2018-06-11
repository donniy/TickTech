from flaskr import database, Iresponse
from flask import jsonify, escape
import uuid
from flaskr.models.Note import *
from flaskr.models.ticket import Ticket
from datetime import datetime


def retrieve_all_request(ticket_id):
    """
    Process the request to receive all notes of a certain ticket.
    """
    notes = Note.query.filter_by(ticket_id=ticket_id).all()
    print(notes)
    return Iresponse.create_response(database.serialize_list(notes), 200)


def create_request(jsonData):
    """
    Process the request to create a node.
    """
    response_body = {}
    ticket_id = escape(jsonData["ticket_id"])
    user_id = escape(jsonData["user_id"])
    message = escape(jsonData["text"])

    ticket = Ticket.query.get(ticket_id)
    if ticket is None:
        return Iresponse.create_response("", 404)

    note = Note()
    note.id = uuid.uuid4()
    note.user_id = user_id
    note.ticket_id = ticket_id
    note.text = message
    note.timestamp = datetime.now()

    if not database.addItemSafelyToDB(note):
        return Iresponse.internal_server_error()

    #add header location.
    return Iresponse.create_response(note.serialize, 201)


def delete_request(note_id):
    """
    Process the request to delete a note.
    """
    note = Note.query.get(note_id)
    if note is None:
        return Iresponse.create_response("", 404)
    try:
        db.session.delete(note)
        db.session.commit()
    except Exception:
        print("LOG: Deleting error")
        return Iresponse.internal_server_error()
    return Iresponse.create_response("", 202)
