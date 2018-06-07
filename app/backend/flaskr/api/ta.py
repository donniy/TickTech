from flaskr import jsonify
from . import apiBluePrint


@apiBluePrint.route('/ta')
def retrieve_tickets():
    # TODO: Query tickets from database
    # tickets = Ticket.query.all()
    cases = [{
            "id": 1, 
            "name": "Tom van de Looij", 
            "course": "Project Software Engineering", 
            "status": "Pending",
            "date": "06-06-2018"
            },
        {
            "id": 2, 
            "name": "Jarno Bakker", 
            "course": "Project Software Engineering", 
            "status": "Pending",
            "date": "06-06-2018"
        },
        {
            "id": 3, 
            "name": "Damian Frölich", 
            "course": "Project Software Engineering", 
            "status": "Pending",
            "date": "06-06-2018"
        }]
    # return database.json_list(tickets)
    return jsonify(cases)
