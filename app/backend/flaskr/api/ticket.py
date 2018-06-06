from flaskr.models.ticket import *
from flaskr.models.Message import *
from . import apiBluePrint
from flask import jsonify, request, escape

@apiBluePrint.route('/ticket/<ticket_id>')
def retrieve_single_ticket(ticket_id):
    """
    Geeft een enkel ticket.
    """
    # TODO: Controlleer rechten
    ticketObj = Ticket.query.get(ticket_id)
    return jsonify(ticketObj.serialize)

@apiBluePrint.route('/ticket/<ticket_id>/reply', methods=['POST'])
def reply_message(ticket_id):
    """
    Tijdelijke functie, geeft altijd success terug en het bericht.
    """
    if (request.json.get("message") == ''):
        return jsonify({'status': 'failed', 'reason': 'Empty message'})
    ticket = Ticket.query.get(ticket_id)
    message = Message()
    message.ticket = ticket
    message.user_id = 12345678 # TODO: de ingelogde ta's id gebruiken
    message.text = request.json.get("message") #TODO: check voor xss
    db.session.add(message)
    db.session.commit()

    return jsonify({'status': "success", 'message': message.serialize})

@apiBluePrint.route('/ticket/<ticket_id>/messages')
def get_ticket_messages(ticket_id):
    """"""
    ticket = Ticket.query.get(ticket_id)
    print(database.json_list(ticket.messages))
    return database.json_list(list(ticket.messages))

@apiBluePrint.route('/ticket/submit', methods=['POST'])
def get_ticket():
    """
    Checkt ticket submission en add to database.
    """

    if ticketValidate(request):
        # TODO add to database.
        return jsonify({'status': "success"});
    # Just return, form is invalid so a failure will occur clientside.
    return;

def ticketValidate(request):

    name = escape(request.json["name"])
    studentid = escape(request.json["studentid"])
    message = escape(request.json["message"])
    courseid = escape(request.json["courseid"])
    labelid = escape(request.json["labelid"])

    # Names can only contain letters, spaces, - or ' in some cases.
    for letter in name:
        if not letter.isalpha() and not letter in " '-":
            return False

    # A number should be within certain bounds and only numerical.
    try:
        studentid_num = int(studentid)
        if studentid_num < 100000 or studentid_num > 999999999:
            return False

    except ValueError:
        return False

    # Course and labelid shoudl be valid (Implement through server checking)

    #TODO implement LTI checking for course/student accessability and validity.

    # Message should not be empty.
    if len(message) == 0:
        return False

    return True
