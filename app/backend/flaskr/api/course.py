from flaskr.models.ticket import *
from . import apiBluePrint
from flask import jsonify, request, escape
from flaskr import database, Iresponse
from flaskr.models.Course import *
from flaskr.models.user import *
from flaskr.request_processing import courses as rp_courses


@apiBluePrint.route('/courses/<course_id>', methods=['GET'])
def retreive_course(course_id):
    course = Course.query.get(course_id)
    return Iresponse.create_response(course.serialize, 200)


@apiBluePrint.route('/courses/<course_id>/tickets', methods=['GET'])
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
    print("Posted to /courses")
    jsonData = request.get_json()
    if jsonData is None:
        return Iresponse.empty_json_request()

    return rp_courses.create_request(jsonData)


@apiBluePrint.route('/courses', methods=['GET'])
def retrieve_all_courses():
    courses = Course.query.all()
    return Iresponse.create_response(database.serialize_list(courses), 200)


# remember to add file in __init__
@apiBluePrint.route('/courses/<user_id>', methods=['GET'])
def retrieve_courses(user_id):
    # TODO get courses from LTI api
    # TODO put user id in data and not in link

    user = User.query.get(user_id)
    if user is None:
        return Iresponse.create_response("", 404)
    courses = user.ta_courses

    return database.json_list(courses)


@apiBluePrint.route('/courses/<course_id>/tas', methods=['GET'])
def get_course_tas(course_id):
    course = Course.query.get(course_id)
    tas = course.ta_courses
    return Iresponse.create_response(database.serialize_list(tas), 200)

@apiBluePrint.route('/courses/<course_id>/students', methods=['GET'])
def get_course_students(course_id):
    course = Course.query.get(course_id)
    print(course_id)
    if course is None:
        return Iresponse.create_response("", 404)
    print(course.student_courses)
    return Iresponse.create_response(
        database.serialize_list(course.student_courses),
        200)
