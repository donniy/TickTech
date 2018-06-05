from flaskr.models.ticket import *
from . import apiBluePrint
from flask import jsonify

@apiBluePrint.route('/ticket/<ticket_id>')
def retrieve_single_ticket(ticket_id):
    """
    Geeft een enkel ticket.
    """
    # TODO: Controlleer rechten
    ticketObj = Ticket.query.get(ticket_id)
    return jsonify(ticketObj.serialize)
