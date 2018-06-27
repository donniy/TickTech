from . import apiBluePrint
from flaskr import database
from flaskr.models.user import User
from flaskr import Iresponse
from flask_jwt_extended import jwt_required
from flaskr.jwt_wrapper import get_current_user
from flaskr.auth import require_ta_in_course, require_role
from flaskr.auth import require_ta_rights_in_course
from flaskr import database


@apiBluePrint.route('/ta/<user_id>/tickets')
@require_role(['ta'])
def retrieve_tickets(user_id):
    """
    Function that returns all the tickets of a ta.
    """
    user = User.query.get(user_id)
    if user is None:
        return Iresponse.create_response("", 404)

    tickets = user.ta_tickets
    if len(tickets) == 0:
        return Iresponse.create_response("", 404)

    return Iresponse.create_response(database.serialize_list(tickets), 200)


@apiBluePrint.route('/ta/<user_id>/courses')
@require_role(['ta'])
def get_all_courses_for_ta(user_id):
    """
    Function that returns all the courses a user
    is ta in.
    """
    user = User.query.get(user_id)
    if user is None:
        return Iresponse.create_response("", 404)
    courses = user.ta_courses
    if len(courses) == 0:
        return Iresponse.create_response("", 404)

    return Iresponse.create_response(database.serialize_list(courses), 200)


@apiBluePrint.route('/ta/courses/<course_id>/tickets', methods=['GET'])
def get_ta_tickets_from_course_for_user(course_id):
    """
    Function that gets the tickets that are bound to
    the current user in a course. The user should have
    ta rights in this course.
    """
    @require_ta_rights_in_course(course_id)
    def get_tickets_inner(curr_course, curr_user):
        """
        Function that gets the ticket. This function is decorated.
        The decorator checks if a jwt is valid and
        if the user is an ta in the course. This is an inner function
        so we have access to the course_id in the decorator.
        """
        ta_tickets = curr_user.ta_tickets
        tickets = list(filter(
            lambda ticket: ticket.course_id == curr_course.id, ta_tickets))
        return Iresponse.create_response(
            database.serialize_list(tickets), 200)

    return get_tickets_inner()
