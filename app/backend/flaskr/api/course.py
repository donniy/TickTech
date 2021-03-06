from . import apiBluePrint
from flask import request
from flaskr import database, Iresponse, plugins, db
from flaskr.models.Course import Course, CoursePlugin
from flaskr.models.user import User
from flaskr.request_processing import courses as rp_courses
from flaskr.auth import require_role
from flask_jwt_extended import jwt_required
from flaskr.auth import require_ta_rights_in_course
from werkzeug.utils import secure_filename
from flaskr.models.ticket import Ticket, TicketStatus
import csv
import os
import uuid


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
    """
    return rp_courses.retrieve_course_tickets_request(course_id)


@apiBluePrint.route('/courses/<course_id>/plugins', methods=['GET'])
@jwt_required
def retrieve_course_plugins(course_id):
    """
    Retrieve all plugin settins for this course. This means a list
    of all plugins and the active state for each of them.
    """
    course = Course.query.get_or_404(course_id)

    all_plugins = plugins.plugin_list()
    tmp = {}
    for p in all_plugins:
        cp = next((pl for pl in course.plugins if pl.plugin == p), None)
        tmp[p] = {}
        tmp[p]['active'] = False if not cp else cp.active
        tmp[p]['name'] = plugins.get_plugin_name(p)

    return Iresponse.create_response(tmp, 200)


@apiBluePrint.route('/courses/<course_id>/plugins/<plugin_id>',
                    methods=['GET'])
@jwt_required
def get_plugin_configurations(course_id, plugin_id):
    """
    Returns the configuration options for this plugin.
    """
    course = Course.query.get_or_404(course_id)

    if plugin_id not in plugins.plugin_list():
        return Iresponse.create_response({"error": "Plugin does not exist"},
                                         404)

    pids = [p.plugin for p in course.plugins]
    if plugin_id not in pids:
        return Iresponse.create_response({"error": "Plugin not available for\
                this course"}, 403)

    cp = next((p for p in course.plugins if p.plugin == plugin_id), None)
    if cp:
        return Iresponse.create_response(cp.get_settings(), 200)
    else:
        return Iresponse.create_response({"error": "Not found"}, 404)


@apiBluePrint.route('/courses/<course_id>/plugins/<plugin_id>',
                    methods=['PUT'])
@jwt_required
def update_plugin_settings(course_id, plugin_id):
    """
    Update the settings for given plugin.
    """
    course = Course.query.get_or_404(course_id)

    if plugin_id not in plugins.plugin_list():
        return Iresponse.create_response({"error": "Plugin does not exist"},
                                         400)

    cp = next((p for p in course.plugins if p.plugin == plugin_id), None)

    if cp is None:
        return Iresponse.create_response({"error": "Cannot configure plugin"},
                                         400)

    js = request.get_json()

    # We iterate over the known settings to prevent setting arbitrary
    # settings from evil requests, which could waste database space.
    if not cp.settings:
        print("cp.settings: {}".format(cp.settings))
        print("cp.settings not set. assign empty dict")
        print("cp: {}".format(cp))
        cp.settings = {}
        print("done")
    for key in cp.get_setting_values():
        print("add {} to settings".format(key))
        cp.settings[key] = js[key]
        print('done')

    try:
        db.session.commit()
        return Iresponse.create_response({"status": "success"}, 200)
    except Exception as e:
        db.session.rollback()
        print(e)
        # This should not happen so a 500 is returned. If for some reason user
        # input triggers this response, the cause of it should be detected
        # before adding to db and return a 400 instead of letting it arrive
        # here.
        return Iresponse.create_response({"status": "could not process your\
                request"}, 500)


@apiBluePrint.route('/courses/<course_id>/plugins/<plugin_id>',
                    methods=['PATCH'])
@jwt_required
def update_plugin_state(course_id, plugin_id):
    """
    Change the active state of a plugin.
    """
    course = Course.query.get_or_404(course_id)

    if plugin_id not in plugins.plugin_list():
        return Iresponse.create_response({"error": "Plugin does not exist"},
                                         400)

    pids = [p.plugin for p in course.plugins]
    if plugin_id not in pids:
        cp = CoursePlugin(id=uuid.uuid4(),
                          plugin=plugin_id,
                          course_id=course_id,
                          active=request.get_json()['active'])
        course.plugins.append(cp)
        try:
            db.session.add(course)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            return Iresponse.create_response({"status": "could not process\
                                                         your request"}, 500)
        return Iresponse.create_response({"status": "success",
                                          "active": cp.active}, 200)
    else:
        cp = next((p for p in course.plugins if p.plugin == plugin_id), None)
        cp.active = request.get_json()['active']
        try:
            db.session.add(course)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            return Iresponse.create_response({"status": "could not process\
                                              your request"}, 500)
        return Iresponse.create_response({"status": "success",
                                          "active": cp.active}, 200)


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
        tickets = Ticket.query.filter_by(course_id=curr_course.id).all()
        status = TicketStatus.query.filter_by(
            id=TicketStatus.unassigned).first()
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
