from . import apiBluePrint
from flask import request
from flaskr import database, Iresponse
from flaskr.models.Course import Course
from flaskr.models.user import User
from flaskr.request_processing import courses as rp_courses
from flaskr.auth import require_role
from flask_jwt_extended import jwt_required
from flaskr.auth import require_ta_rights_in_course
from werkzeug.utils import secure_filename
from flaskr.models import ticket
import csv
import os


@apiBluePrint.route('/courses/single/<course_id>', methods=['GET'])
@jwt_required
def retreive_course(course_id):
    """
    Function that returns information about a specific course.
    """
    course = Course.query.get(course_id)
    if course:
        return Iresponse.create_response(course.serialize, 200)
    else:
        return Iresponse.create_response("Course not found", 404)


@apiBluePrint.route('/courses/<course_id>/tickets', methods=['GET'])
@require_role(['supervisor', 'ta'])
def retrieve_course_tickets(course_id):
    """
    Function that returns all tickets of a the given course.
    TODO: Controle if user has permissions.
    """
    return rp_courses.retrieve_course_tickets_request(course_id)


@apiBluePrint.route('/courses/<course_id>/tickets/unassigned', methods=['GET'])
def get_unassigned_course_tickets(course_id):
    """
    Function that returns the tickets in a course that are unassigned.
    """
    @require_ta_rights_in_course(course_id)
    def get_unassigned_tickets_inner(curr_course, curr_user):
        """
        Inner function, wrapped in a decorator, so we check if the user
        has the correct rigths, to get the unassigned tickets.
        """
        tickets = ticket.Ticket.query.filter_by(course_id=curr_course.id).all()
        status = ticket.TicketStatus.query.filter_by(name="Unassigned").first()
        unassign_tickets = list(filter(
            lambda ticket: ticket.status_id == status.id, tickets))
        print(unassign_tickets)
        return Iresponse.create_response(
            database.serialize_list(unassign_tickets), 200)

    return get_unassigned_tickets_inner()


@apiBluePrint.route('/courses', methods=['POST'])
@require_role(['supervisor'])
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
@jwt_required
def retrieve_all_courses():
    """
    Retrieve all courses from database.
    """
    courses = Course.query.all()
    return Iresponse.create_response(database.serialize_list(courses), 200)


# not used at the moment. If still not used in the future delete this function
# @apiBluePrint.route('/courses/ta/<user_id>', methods=['GET'])
# def retrieve_courses(user_id):
#     # TODO get courses from LTI api
#     # TODO put user id in data and not in link

#     user = User.query.get(user_id)
#     if user is None:
#         return Iresponse.create_response("", 404)
#     courses = user.ta_courses

#     return Iresponse.create_response(database.serialize_list(courses), 200)


@apiBluePrint.route('/courses/<course_id>/tas', methods=['GET'])
@jwt_required
def get_course_tas(course_id):
    """
    Return all the tas in a course.
    """
    course = Course.query.get(course_id)
    if course is None:
        return Iresponse.create_response("", 404)
    tas = course.ta_courses
    return Iresponse.create_response(database.serialize_list(tas), 200)


@apiBluePrint.route('/courses/<course_id>/students', methods=['GET'])
@require_role(['supervisor', 'ta'])
def get_course_students(course_id):
    """
    Returns all the students in a course.
    """
    course = Course.query.get(course_id)
    print(course_id)
    if course is None:
        return Iresponse.create_response("", 404)
    print(course.student_courses)
    return Iresponse.create_response(
        database.serialize_list(course.student_courses),
        200)


@apiBluePrint.route('/courses/<course_id>/tas', methods=['POST'])
@require_role(['supervisor'])
def add_tas_to_course(course_id):
    """
    Add new teaching assistants to course.
    """
    if request.files == '':
        return Iresponse.empty_json_request()
    for f_id in request.files:
        f = request.files[f_id]
        if f.filename.split('.').pop() != "csv":
            return Iresponse.create_response("", 400)
        filename = secure_filename(f.filename)
        f.save(filename)
        read_tas_csv(filename, course_id)
        os.remove(filename)
    return Iresponse.create_response("", 200)


def read_tas_csv(filename, course_id):
    """
    Add teaching assistants from uploaded file.
    """
    f = open(filename, 'r')
    reader = csv.reader(f, delimiter=',')
    course = Course.query.get(course_id)
    if course is None:
        f.close()
        return False
    for row in reader:
        if len(row) != 3:
            continue
        stud_id = int(row[0])
        user = User.query.get(stud_id)
        if user is None:
            user = User(id=int(row[0]), name=row[1], email=row[2])
            if not database.addItemSafelyToDB(user):
                continue

        if user not in course.ta_courses:
            print("ADDING TA")
            course.ta_courses.append(user)
            database.get_db().session.commit()
    f.close()
    return True


@apiBluePrint.route('/courses/<course_id>/students', methods=['POST'])
@require_role(['supervisor'])
def add_students_to_course(course_id):
    """
    Add students to course.
    """
    if request.files == '':
        return Iresponse.empty_json_request()

    for f_id in request.files:
        f = request.files[f_id]
        if f.filename.split('.').pop() != "csv":
            return Iresponse.create_response("", 400)
        filename = secure_filename(f.filename)
        f.save(filename)
        read_students_csv(filename, course_id)
        os.remove(filename)
    return Iresponse.create_response("", 200)


def read_students_csv(filename, course_id):
    """
    Reads in a csv file and creates a user
    if the there is no user yet with the gived id.
    Adds the user to the specified course if its not
    yet active.
    This will probably be removed when
    the integration with lti works.
    If not, add some better error handeling
    and exiting.
    """
    f = open(filename, 'r')
    reader = csv.reader(f, delimiter=',')
    course = Course.query.get(course_id)
    if course is None:
        f.close()
        return False
    for row in reader:
        if len(row) != 3:
            continue
        stud_id = int(row[0])
        user = User.query.get(stud_id)
        if user is None:
            user = User(id=int(row[0]), name=row[1], email=row[2])
            if not database.addItemSafelyToDB(user):
                continue

        if user not in course.student_courses:
            print("APPENDING USER")
            course.student_courses.append(user)
            database.get_db().session.commit()
    f.close()
    return True
