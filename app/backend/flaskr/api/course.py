from flaskr.models.ticket import *
from . import apiBluePrint
from flask import jsonify, request, escape
from flaskr import database, Iresponse
from flaskr.models.Course import *
from flaskr.models.user import *
from flaskr.request_processing import courses as rp_courses

@apiBluePrint.route('/courses/<course_id>/tickets')
def retrieve_course_tickets(course_id):
    """
    Geeft alle ticktes over gegeven course.
    """
    # TODO: Controleer of degene die hierheen request permissies heeft.
    return rp_courses.retrieve_course_tickets_request(course_id)


@apiBluePrint.route('/courses', methods=['POST'])
def create_course():
    """
    Check ticket submission and add to database.
    """
    jsonData = request.get_json()
    if jsonData is None:
        return Iresponse.empty_json_request()

    return rp_courses.create_request(jsonData)


@apiBluePrint.route('/courses', methods=['GET'])
def retrieve_all_courses():
    courses = Course.query.all()
    return Iresponse.create_response(database.serialize_list(courses), 200)


# remember to add file in __init__
@apiBluePrint.route('/courses/<user_id>')
def retrieve_courses(user_id):
    # TODO get courses from LTI api
    # TODO put user id in data and not in link

    user = User.query.get(user_id)
    if user is None:
        return Iresponse.create_response("", 404)
    courses = user.ta_courses

    return database.json_list(courses)
