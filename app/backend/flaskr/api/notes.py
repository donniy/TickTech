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
    return rp_notes.retrieve_all_request(ticket_id)


@apiBluePrint.route('/notes', methods=['POST'])
def add_new_note():
    jsonData = request.get_json()
    if jsonData is None:
        return Iresponse.empty_json_request()

    return rp_notes.create_request(jsonData)


@apiBluePrint.route('/notes/<note_id>/close', methods=['POST'])
def remove_note(note_id):
    return rp_notes.delete_request(note_id)
