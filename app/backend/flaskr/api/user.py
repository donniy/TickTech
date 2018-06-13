from flaskr.models.ticket import *
from . import apiBluePrint
from flask_jwt import jwt_required, current_identity
from flaskr import Iresponse
from flaskr.models.user import *


@apiBluePrint.route('/user/<user_id>/tickets')
@jwt_required()
def retrieve_user_tickets(user_id):
    """
    Geeft alle ticktes van gegeven user.
    """
    # TODO: Controleer of degene die hierheen request permissies heeft.
    tickets = Ticket.query.filter_by(user_id=user_id).all()
    return database.json_list(tickets)

# maybe add query parameter instead of full api route


@apiBluePrint.route('/user/<user_id>/tickets/active')
@jwt_required()
def retrieve_active_user_tickets(user_id):
    """
    Geeft alle ticktes van gegeven user.
    """
    # TODO: Controleer of degene die hierheen request permissies heeft.
    user_id = current_identity.id
    tickets = Ticket.query.filter(Ticket.user_id == user_id,
                                  Ticket.ticket_status.has(
                                      TicketStatus.name != 'closed')).all()
    return database.json_list(tickets)


@apiBluePrint.route('/user/register', methods=["POST"])
def register_user():
    jsonData = request.get_json()
    if jsonData is None:
        return Iresponse.internal_server_error()
    email = escape(jsonData["email"])
    name = escape(jsonData["name"])
    studentid = escape(jsonData["studentid"])
    password = escape(jsonData["password"])

    response_body = {}

    new_user = User()
    new_user.id = studentid
    new_user.name = name
    new_user.email = email

    if not database.addItemSafelyToDB(new_user):
        return Iresponse.internal_server_error()

    response = Iresponse.create_response(response_body, 201)
    return response


@apiBluePrint.route('/user/<int:user_id>')
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return Iresponse.create_response("", 404)
    return Iresponse.create_response(user.serialize, 200)


@apiBluePrint.route('/user/<user_id>/courses')
def get_courses_from_student(user_id):
    user = User.query.get(user_id)
    if user is None:
        return Iresponse.create_response("", 404)
    courses = user.student_courses
    if len(courses) == 0:
        return Iresponse.create_response("", 404)
    return Iresponse.create_response(database.serialize_list(courses), 200)
