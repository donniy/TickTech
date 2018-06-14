from flaskr import database, Iresponse
from flask import jsonify, escape
import uuid
from flaskr.models.Course import *
from flaskr.models.ticket import *

def create_request(jsonData):
    mail = escape(jsonData['mail'])
    title = escape(jsonData['title'])
    description = escape(jsonData['description'])

    course = Course()
    course.id = uuid.uuid4()
    course.course_email = mail
    course.title - title
    course.description = description

    if not database.addItemSafelyToDB(course):
        return Iresponse.internal_server_error()

    return Iresponse.create_response("", 200)


def retrieve_course_tickets_request(course_id):
    tickets = Ticket.query.filter_by(course_id=course_id).all()
    if tickets is None:
        return Iresponse.create_response("", 404)

    return Iresponse.create_response(database.serialize_list(tickets), 200)
