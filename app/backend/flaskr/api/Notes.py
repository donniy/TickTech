from . import apiBluePrint
from flaskr import jsonify, request, database

# remember to add file in __init__
@apiBluePrint.route('/notes/<ticket_id>')
def retrieve_notes(ticket_id):
    # TODO get notes from database
    notes = [{
        "id":1,
        "text":"yo er is iets",
        "user_id":"1234"
    },{
        "id":2,
        "text":"Mooi, wat dan?",
        "user_id":"4321"
    }]
    return jsonify(notes)

@apiBluePrint.route('/note/add', methods=['POST'])
def add_new_note():
    ticket_id = request.json.get('ticket_id')
    user_id = request.json.get('user_id')
    message = request.json.get('message')

    success = database.addNote(user_id, ticket_id,message)

    return jsonify({'test1':ticket_id,'test2':user_id,'test3':message,'success':success})
