from flaskr.models.ticket import *
from sqlalchemy import not_ as NOT
from . import apiBluePrint

@apiBluePrint.route('/user/<user_id>')

def retrieve_user_tickets(user_id):
    """
    Geeft alle ticktes van gegeven user.
    """
    # TODO: Controleer of degene die hierheen request permissies heeft.
    tickets = Ticket.query.filter_by(user_id = user_id).all()
    return database.json_list(tickets)


@apiBluePrint.route('/user/active/<user_id>')

def retrieve_active_user_tickets(user_id):
    """
    Geeft alle ticktes van gegeven user.
    """
    # TODO: Controleer of degene die hierheen request permissies heeft.
    tickets = Ticket.query.filter(Ticket.user_id == user_id, Ticket.ticket_status.has(TicketStatus.name!='closed')).all()
    return database.json_list(tickets)
