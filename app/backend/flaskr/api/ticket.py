from flaskr.models.ticket import *
from . import apiBluePrint
from flask import jsonify, request

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
    ticket = Ticket.query.get(ticket_id)
    message = Message()
    message.ticket = ticket
    message.user_id = 12345678 # TODO: de ingelogde ta's id gebruiken
    message.text = request.json.get("message") #TODO: check voor xss
    db.session.add(message)
    db.session.commit()

    return jsonify({'status': "success", 'message': {'text': request.json.get("message"), 'user_id': 12345678, 'id': 5}})
