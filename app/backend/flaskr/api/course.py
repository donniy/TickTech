from flaskr.models.ticket import *
from . import apiBluePrint


@apiBluePrint.route('/course/<course_id>')
def retrieve_course_tickets(course_id):
    """
    Geeft alle ticktes over gegeven course.
    """
    # TODO: Controleer of degene die hierheen request permissies heeft.
    tickets = Ticket.query.filter_by(course_id=course_id).all()
    return database.json_list(tickets)
