from flaskr import jsonify
from flaskr.models.ticket import Ticket
from . import apiBluePrint
from flaskr import database

@apiBluePrint.route('/ta')
def retrieve_tickets():
    # TODO: Query tickets from database
    tickets = Ticket.query.all()
    print(tickets)
    # cases = [{
    #         "id": 1,
    #         "name": "Tom van de Looij",
    #         "course": "Project Software Engineering",
    #         "status": "Pending",
    #         "date": "06-06-2018"
    #         },
    #     {
    #         "id": 2,
    #         "name": "Jarno Bakker",
    #         "course": "Project Software Engineering",
    #         "status": "Pending",
    #         "date": "06-06-2018"
    #     },
    #     {
    #         "id": 3,
    #         "name": "Damian Frölich",
    #         "course": "Project Software Engineering",
    #         "status": "Pending",
    #         "date": "06-06-2018"
    #     }]
    return database.json_list(tickets)
    # return jsonify(cases)
