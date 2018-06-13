from flaskr.models.ticket import *
from flaskr.models.Message import *
from flaskr.models.user import *
from flaskr import database
from . import apiBluePrint
from flask import jsonify, request, escape
from flaskr import socketio
import uuid
import datetime
from flaskr.request_processing import ticket as rp_ticket
from flaskr.request_processing import message as rp_message
from flaskr import Iresponse


# Make this post with a button.
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
    if ticketObj is None:
        return Iresponse.create_response("", 404)
    return Iresponse.create_response(ticketObj.serialize, 200)


@apiBluePrint.route('/ticket/<ticket_id>/messages', methods=['POST'])
def create_message(ticket_id):
    """
    Tijdelijke functie, geeft altijd success terug en het bericht.
    """
    jsonData = request.get_json()
    if request is None:
        return Iresponse.empty_json_request()

    userId = escape(jsonData["user_id"])
    msg = rp_message.create_request(jsonData, ticket_id)

    ticket = Ticket.query.get(ticket_id)
    user = User.query.get(userId)

    if ticket is not None and user is not None:
        # unassigned
        if ticket.ticket_status.id == 1:
            ticket.ticket_status = TicketStatus.query.get(4)
        # assigned
        elif ticket.ticket_status.id == 3:
            ticket.ticket_status = TicketStatus.query.get(4)

        tas = ticket.binded_tas
        if user not in tas:
            # add user to bound tas
            tas.append(user)

    db.session.commit()
    return msg


@apiBluePrint.route('/ticket/<ticket_id>/messages')
def get_ticket_messages(ticket_id):
    return rp_message.retrieve_all_request(ticket_id)


@apiBluePrint.route('/ticket/submit', methods=['POST'])
def create_ticket():
    """
    Check ticket submission and add to database.
    """
    jsonData = request.get_json()
    if jsonData is None:
        return Iresponse.empty_json_request()
    return rp_ticket.create_request(jsonData)
