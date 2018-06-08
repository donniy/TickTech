from flaskr.models.ticket import *
from . import apiBluePrint
from flask import jsonify, request, escape
from flaskr import database
from flaskr.models.Course import *

@apiBluePrint.route('/course/<course_id>')
def retrieve_course_tickets(course_id):
    """
    Geeft alle ticktes over gegeven course.
    """
    # TODO: Controleer of degene die hierheen request permissies heeft.
    tickets = Ticket.query.filter_by(course_id=course_id).all()
    return database.json_list(tickets)

@apiBluePrint.route('/course/new', methods=['POST'])
def create_course():
    """
    Check ticket submission and add to database.
    """
    id = escape(request.json["id"])
    mail = escape(request.json["mail"])
    title = escape(request.json["title"])
    description = escape(request.json["description"])

    c = Course()
    c.id = id
    c.course_email = mail
    c.title = title
    c.description = description

    print(id)
    print(mail)

    try:
        success = database.addItemSafelyToDB(c)
        print(success)
    except database.DatabaseInsertException as err:
        print(err)

    return jsonify({'status':'success'})
