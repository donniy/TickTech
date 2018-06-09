from flaskr.models.ticket import *
from flaskr.models.Message import *
from flaskr import database
from . import apiBluePrint
from flask import jsonify, request, escape
from flaskr import socketio
import uuid, datetime
from flaskr.request_processing import ticket as rp_ticket
from flaskr import Iresponse


#Make this post with a button.
@apiBluePrint.route('/ticket/<ticket_id>/close', methods=['POST'])
def close_ticket(ticket_id):
    """ Update this with a rights check."""
    ticket = Ticket.query.get(ticket_id)
    ticket.close
    db.session.commit()
    return jsonify({'status': "success", 'message': 'ticket closed'})

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

    room = "ticket-messages-{}".format(ticket_id)
    socketio.emit('messageAdded', {'text': message.text, 'user_id': message.user_id}, room=room)

    try:
        database.addItemSafelyToDB(message)
    except database.DatabaseInsertException as DBerror:
        print(DBerror)
        #Need to handle this better somehow. It should never happen though.

    return jsonify({'status': "success", 'message': message.serialize})

@apiBluePrint.route('/ticket/<ticket_id>/messages')
def get_ticket_messages(ticket_id):
    """"""
    ticket = Ticket.query.get(ticket_id)
    print(database.json_list(ticket.messages))
    return database.json_list(list(ticket.messages))

# TODO: Deze verplaatsen naar user zodra die beschikbaar is
@apiBluePrint.route('/student/ticket/<ticket_id>/reply', methods=['POST'])
def student_reply_message(ticket_id):
    """
    Tijdelijke functie, geeft altijd success terug en het bericht.
    """
    if (request.json.get("message") == ''):
        return jsonify({'status': 'failed', 'reason': 'Empty message'})
    ticket = Ticket.query.get(ticket_id)
    message = Message()
    message.ticket = ticket
    message.user_id = 123123123 # TODO: de ingelogde ta's id gebruiken
    message.text = request.json.get("message") #TODO: check voor xss
    db.session.add(message)
    db.session.commit()

    room = "ticket-messages-{}".format(ticket_id)
    socketio.emit('messageAdded', {'text': message.text, 'user_id': message.user_id}, room=room)

    return jsonify({'status': "success", 'message': message.serialize})


@apiBluePrint.route('/ticket/submit', methods=['POST'])
def create_ticket():
    """
    Check ticket submission and add to database.
    """
    jsonData = request.get_json()
    if jsonData is None:
        return Iresponse.empty_json_request()
    return rp_ticket.create_request(jsonData)
