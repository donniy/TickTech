from flaskr.models.ticket import Ticket
from . import apiBluePrint
from flask_jwt_extended import jwt_required
from flaskr.jwt_wrapper import get_current_user
from flaskr import Iresponse, database
from flask import request, escape
from flaskr.models.user import User
from flaskr.request_processing.user import validate_userdata
from flaskr.utils.json_validation import validate_json


@apiBluePrint.route('/user/tickets')
@jwt_required
def retrieve_user_tickets():
    """
    Returns all the tickets of the user.
    """
    curr_user = get_current_user()
    tickets = Ticket.query.filter_by(user_id=curr_user.id).all()
    return Iresponse.create_response(database.serialize_list(tickets), 200)


@apiBluePrint.route('/user/tickets/course/<course_id>', methods=['GET'])
@jwt_required
def get_user_ticket_for_course(course_id):
    """
    Function that gets all the tickets of a user in the course with
    id: <course_id>
    """
    curr_user = get_current_user()
    tickets = Ticket.query.filter(Ticket.user_id == curr_user.id,
                                  Ticket.course_id == course_id).all()
    return Iresponse.create_response(database.serialize_list(tickets), 200)


@apiBluePrint.route('/user/<user_id>/tickets/active')
@jwt_required
def retrieve_active_user_tickets(user_id):
    """
    Gets all the active tickets of a user with id: <user_id>
    """
    # TODO: Controleer of degene die hierheen request permissies heeft.
    current_identity = get_current_user()
    user_id = current_identity.id
    tickets = Ticket.query.filter(Ticket.user_id == user_id,
                                  Ticket.status_id != 2).all()
    return Iresponse.create_response(database.serialize_list(tickets), 200)


@apiBluePrint.route('/user/notifications', methods=["GET"])
@jwt_required
def unread_messages():
    """
    Retrieve all unread messages of this user.
    If in the url the param course_id is specified
    only the unread messages with a course_id matching
    the specified course_id will be returned.
    """
    specified_course = request.args.get('course_id')
    current_identity = get_current_user()
    tmp = {}
    unread = current_identity.unread
    for msg in unread:
        if str(msg.ticket_id) not in tmp:
            if specified_course is not None:
                tick = Ticket.query.filter_by(id=msg.ticket_id).first()
                if str(tick.course_id) != str(specified_course):
                    continue
            ticket_id = str(msg.ticket_id)
            tmp[ticket_id] = {'ticket': msg.ticket.serialize, 'n': 0}
            if current_identity in msg.ticket.bound_tas:
                tmp[ticket_id]['ta'] = True
            else:
                tmp[ticket_id]['ta'] = False
        tmp[ticket_id]['n'] += 1
    return Iresponse.create_response(tmp, 200)


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
    """
    Function that checks if a user email already exists.
    """
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
    """
    Function that checks if the id of a user already exists.
    """
    json_data = request.get_json()
    if not validate_json(json_data, ["studentid"]):
        return Iresponse.empty_json_request()

    studentid = json_data["studentid"]
    user = User.query.filter_by(id=studentid).first()

    if user is None:
        return Iresponse.create_response({"status": False}, 200)
    return Iresponse.create_response({"status": True}, 200)


@apiBluePrint.route('/user/student_courses', methods=['GET'])
@jwt_required
def get_courses_user_is_student_in():
    curr_user = get_current_user()
    if curr_user is None:
        return Iresponse.create_response("", 404)
    courses = curr_user.student_courses
    return Iresponse.create_response(database.serialize_list(courses), 200)


@apiBluePrint.route('/user/teachingAssistant_courses', methods=['GET'])
@jwt_required
def get_courses_user_is_ta_in():
    curr_user = get_current_user()
    if curr_user is None:
        return Iresponse.create_response("", 404)
    courses = curr_user.ta_courses
    return Iresponse.create_response(database.serialize_list(courses), 200)


@apiBluePrint.route('/user/<int:user_id>')
@jwt_required
def get_user(user_id):
    user = get_current_user()
    if user is None:
        return Iresponse.create_response("", 404)
    return Iresponse.create_response(user.serialize, 200)
