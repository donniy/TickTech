from . import apiBluePrint
from flask import jsonify, request, escape
from flaskr import database
from flaskr.models.Note import *
from flaskr.request_processing import notes as rp_notes
from flaskr import Iresponse


# remember to add file in __init__


# Add rights check.
@apiBluePrint.route('/notes/<ticket_id>')
def retrieve_notes(ticket_id):
    """
    Return all the notes for a ticket.
    Returns a 404 status if no notes are found.
    Otherwise a 200 with in the body in a json_data
    all the notes.
    """
    return rp_notes.retrieve_all_request(ticket_id)


# Add right check
@apiBluePrint.route('/notes', methods=['POST'])
def add_new_note():
    """
    Creates a new note.
    If no json is given return a 400 with no body.
    If no ticket is found return a 404 error.
    If a note is created return a 201 status.
    """
    jsonData = request.get_json()
    if jsonData is None:
        return Iresponse.empty_json_request()

    return rp_notes.create_request(jsonData)


@apiBluePrint.route('/notes/<note_id>/close', methods=['POST'])
def remove_note(note_id):
    """
    Deletes a note.
    If the note is not found return a 404.
    If the note is deleted return a 202.
    """
    return rp_notes.delete_request(note_id)
