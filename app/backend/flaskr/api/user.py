from flaskr.models.ticket import *
from . import apiBluePrint
from flask_jwt import jwt_required, current_identity

@apiBluePrint.route('/user')
@jwt_required()
def retrieve_user_tickets():
    """
    Geeft alle ticktes van gegeven user.
    """
    user = current_identity
    tickets = Ticket.query.filter_by(user_id=user.id).all()
    return database.json_list(tickets)


@apiBluePrint.route('/user/active/<user_id>')
def retrieve_active_user_tickets(user_id):
    """
    Geeft alle ticktes van gegeven user.
    """
    # TODO: Controleer of degene die hierheen request permissies heeft.
    tickets = Ticket.query.filter(Ticket.user_id == user_id, Ticket.ticket_status.has(TicketStatus.name!='closed')).all()
    return database.json_list(tickets)
