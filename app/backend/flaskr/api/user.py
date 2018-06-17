from flaskr.models.ticket import *
from . import apiBluePrint
from flask_jwt import jwt_required, current_identity
from flaskr import Iresponse
from flask import request
from flaskr.models.user import *
from flaskr.utils.json_validation import *
from flaskr.request_processing.user import *


@apiBluePrint.route('/user/<user_id>/tickets')
@jwt_required()
def retrieve_user_tickets(user_id):
    """
    Geeft alle ticktes van gegeven user.
    """
    # TODO: Controleer of degene die hierheen request permissies heeft.
    tickets = Ticket.query.filter_by(user_id=user_id).all()
    return Iresponse.create_response(database.serialize_list(tickets), 200)

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
                                  Ticket.status_id != 2).all()
    return Iresponse.create_response(database.serialize_list(tickets), 200)


@apiBluePrint.route('/user/register', methods=["POST"])
def register_user():
    ''' Expects a request with email, name, id and password (and confirmed)
        and enters new user into database.
    '''

    json_data = request.get_json()

    if not validate_json(json_data, ["email", "name",
                                     "studentid", "password",
                                     "password_confirmation"]):
        return Iresponse.empty_json_request()

    email = escape(json_data["email"])
    name = escape(json_data["name"])
    studentid = escape(json_data["studentid"])
    password = escape(json_data["password"])
    repassword = escape(json_data["password_confirmation"])

    if not validate_userdata(email, name, studentid, password, repassword):
        return Iresponse.empty_json_request()

    # Backend check if email/studentid already exists
    user = User.query.filter_by(email=email).first()
    if user:
        return Iresponse.create_response({"status": False}, 200)

    studentid = json_data["studentid"]
    user = User.query.filter_by(id=studentid).first()

    if user:
        return Iresponse.create_response({"status": False}, 200)

    new_user = User()
    new_user.id = studentid
    new_user.name = name
    new_user.email = email

    if not database.addItemSafelyToDB(new_user):
        return Iresponse.internal_server_error()

    return Iresponse.create_response("", 201)


@apiBluePrint.route('/user/exists', methods=["POST"])
def user_exists():

    json_data = request.get_json()
    if not validate_json(json_data, ["email"]):
        return Iresponse.empty_json_request()

    email = json_data["email"]
    user = User.query.filter_by(email=email).first()

    if user is None:
        return Iresponse.create_response({"status": False}, 200)
    return Iresponse.create_response({"status": True}, 200)


@apiBluePrint.route('/user/idexists', methods=["POST"])
def userid_exists():

    json_data = request.get_json()
    if not validate_json(json_data, ["studentid"]):
        return Iresponse.empty_json_request()

    studentid = json_data["studentid"]
    user = User.query.filter_by(id=studentid).first()

    if user is None:
        return Iresponse.create_response({"status": False}, 200)
    return Iresponse.create_response({"status": True}, 200)


@apiBluePrint.route('/user/<user_id>/courses')
def get_courses_from_student(user_id):
    user = User.query.get(user_id)
    if user is None:
        return Iresponse.create_response("", 404)
    courses = user.student_courses
    if len(courses) == 0:
        return Iresponse.create_response("", 404)
    return Iresponse.create_response(database.serialize_list(courses), 200)


@apiBluePrint.route('/user/<int:user_id>')
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return Iresponse.create_response("", 404)
    return Iresponse.create_response(user.serialize, 200)
