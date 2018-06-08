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