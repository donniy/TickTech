from flaskr import jsonify
from flaskr.models.ticket import Ticket
from . import apiBluePrint
from flaskr import database
from flaskr.models.Course import *
from flaskr.models.user import *
from flaskr import Iresponse


@apiBluePrint.route('/ta/<ta_id>/inbox')
def get_all_cases(ta_id):
    tickets = Ticket.query.all()

    if len(tickets) == 0:
        return Iresponse.create_response("", 404)

    return Iresponse.create_response(database.serialize_list(tickets), 200)


@apiBluePrint.route('ta/<ta_id>/myinbox')
def get_ta_cases(ta_id):
    ticket = Ticket.query.get(ta_id)

    if len(tickets) == 0:
        return Iresponse.create_response("", 404)
    
    return Iresponse.create_response(database.serialize_list(tickets), 200)