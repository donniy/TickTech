from flaskr.models.ticket import *
from sqlalchemy import not_ as NOT
from . import apiBluePrint
from flaskr import Iresponse
from flaskr.models.user import *

@apiBluePrint.route('/user/<user_id>/tickets')
def retrieve_user_tickets(user_id):
    """
    Geeft alle ticktes van gegeven user.
    """
    # TODO: Controleer of degene die hierheen request permissies heeft.
    tickets = Ticket.query.filter_by(user_id = user_id).all()
    print(tickets)
    return database.json_list(tickets)

#maybe add query parameter instead of full api route
@apiBluePrint.route('/user/<user_id>/tickets/active')
def retrieve_active_user_tickets(user_id):
    """
    Geeft alle ticktes van gegeven user.
    """
    # TODO: Controleer of degene die hierheen request permissies heeft.
    tickets = Ticket.query.filter(Ticket.user_id == user_id, Ticket.ticket_status.has(TicketStatus.name!='closed')).all()
    return database.json_list(tickets)


@apiBluePrint.route('/user/<user_id>')
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return Iresponse.create_response("", 404)
    return Iresponse.create_response(user.serialize, 200)


@apiBluePrint.route('/user/<user_id>/courses')
def get_courses_from_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return Iresponse.create_response("", 404)
    courses = user.student_courses
    if len(courses) == 0:
        return Iresponse.create_response("", 404)
    return Iresponse.create_response(database.serialize_list(courses), 200)

@apiBluePrint.route('/user/register')
def register_user():
    jsonData = request.get_json()
    return
