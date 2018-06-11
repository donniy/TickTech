from . import apiBluePrint
from flask import jsonify, request, escape
from flaskr import database
from flaskr.models.Note import *

# remember to add file in __init__
@apiBluePrint.route('/notes/<ticket_id>')
def retrieve_notes(ticket_id):
    notes = Note.query.filter_by(ticket_id=ticket_id).all()
    return database.json_list(notes)

@apiBluePrint.route('/note/add', methods=['POST'])
def add_new_note():
    ticket_id = escape(request.json["ticket_id"])
    user_id = escape(request.json["user_id"])
    message = escape(request.json["text"])

    n = Note()
    n.id = uuid.uuid1()
    n.user_id = user_id
    if n.user_id is None:
        n.user_id = 1
    n.ticket_id = ticket_id
    n.text = message
    n.timestamp = datetime.now()

    try:
        success =  database.addItemSafelyToDB(n)
        print(success)
    except database.DatabaseInsertException as err:
        print(err)

    ret = {
        "id":n.id,
        "user_id":n.user_id,
        "ticket_id":n.ticket_id,
        "text":n.text,
        "timestamp":n.timestamp
    }

    return jsonify(ret)

@apiBluePrint.route('/note/<note_id>/close', methods=['POST'])
def remove_note(note_id):
    note = Note.query.get(note_id)
    db.session.delete(note)
    db.session.commit()
    return jsonify({'status': "success", 'message': 'note closed'})
