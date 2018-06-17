from flaskr import jsonify
from flaskr.models.ticket import Ticket
from . import apiBluePrint
from flaskr import database
from flaskr.models.Course import *
from flaskr.models.user import *
from flaskr import Iresponse


@apiBluePrint.route('/ta/<user_id>/tickets')
def retrieve_tickets(user_id):
    user = User.query.get(user_id)
    if user is None:
        return Iresponse.create_response("", 404)

    tickets = user.ta_tickets
    if len(tickets) == 0:
        return Iresponse.create_response("", 404)

    return Iresponse.create_response(database.serialize_list(tickets), 200)


@apiBluePrint.route('/ta/<user_id>/courses')
def get_all_courses_for_ta(user_id):
    user = User.query.get(user_id)
    if user is None:
        return Iresponse.create_response("", 404)
    courses = user.ta_courses
    if len(courses) == 0:
        return Iresponse.create_response("", 404)

    return Iresponse.create_response(database.serialize_list(courses), 200)
