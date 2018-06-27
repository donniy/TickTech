from flaskr import database, Iresponse
from flask import escape
import uuid
from flaskr.models.Course import Course
from flaskr.models.ticket import Ticket
from flaskr.models.user import User
from flaskr.auth import require_ta_rights_in_course


def create_request(jsonData):
    """
    Function that handles the create request from a course.
    """
    mail = escape(jsonData['mail'])
    title = escape(jsonData['title'])
    description = escape(jsonData['description'])

    course = Course()
    course.id = uuid.uuid4()
    course.course_email = mail
    course.title = title
    course.description = description

    if not database.addItemSafelyToDB(course):
        return Iresponse.internal_server_error()

    return Iresponse.create_response("", 200)


def retrieve_course_tickets_request(course_id):
    """
    Function that handle the request that retrieves
    the tickets of a course. In order to be able
    to get the tickets, a user needs to have atleast
    teaching assistant rights in the course.
    """

    @require_ta_rights_in_course(course_id)
    def retrieve_course_tickets(curr_course, curr_user):
        """
        Inner fucntion that gets wrapped in a decorator.
        Retrieves the tickets by course id and returns them if found.
        If no tickets are found we return a 404.
        """
        tickets = Ticket.query.filter_by(course_id=curr_course.id).all()
        if tickets is None:
            return Iresponse.create_response("", 404)

        return Iresponse.create_response(database.serialize_list(tickets), 200)

    return retrieve_course_tickets()


def single_course_request(course_id):
    course = Course.query.filter_by(id=uuid.UUID(course_id)).first()
    return course


def get_tas_by_label(label_id):
    tas = User.query.filter_by(labels=label_id).all()
    print(tas)
    return tas
