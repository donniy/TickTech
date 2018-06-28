from . import apiBluePrint
from flask import jsonify, request, escape
from flaskr import database, Iresponse, plugins, db
from flaskr.models.Course import Course, CoursePlugin
from flaskr.models.user import User
from flaskr.request_processing import courses as rp_courses
from werkzeug.utils import secure_filename
import csv
import os
from flask_jwt_extended import jwt_required
import uuid


@apiBluePrint.route('/courses/single/<course_id>', methods=['GET'])
def retreive_course(course_id):
    course = Course.query.get(course_id)
    if course:
        return Iresponse.create_response(course.serialize, 200)
    else:
        return Iresponse.create_response("Course not found", 404)


@apiBluePrint.route('/courses/<course_id>/tickets', methods=['GET'])
def retrieve_course_tickets(course_id):
    """
    Geeft alle ticktes over gegeven course.
    """
    # TODO: Controleer of degene die hierheen request permissies heeft.
    return rp_courses.retrieve_course_tickets_request(course_id)


@apiBluePrint.route('/courses/<course_id>/plugins', methods=['GET'])
@jwt_required
def retrieve_course_plugins(course_id):
    """
    Retrieve all plugin settins for this course. This means a list
    of all plugins and the active state for each of them.
    """
    course = Course.query.get_or_404(course_id)
    # TODO: Check if user is supervisor in this course.

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
    # TODO: Check if user is supervisor in this course.

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
    # TODO: Check if user is supervisor in this course.

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
    # TODO: Check if user is supervisor in this course.

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
def get_course_tas(course_id):
    course = Course.query.get(course_id)
    if course is None:
        return Iresponse.create_response("", 404)
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


@apiBluePrint.route('/courses/<course_id>/tas', methods=['POST'])
def add_tas_to_course(course_id):
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
    f = open(filename, 'r')
    reader = csv.reader(f, delimiter=',')
    course = Course.query.get(course_id)
    if course is None:
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
    return True


@apiBluePrint.route('/courses/<course_id>/students', methods=['POST'])
def add_students_to_course(course_id):
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
    return True
