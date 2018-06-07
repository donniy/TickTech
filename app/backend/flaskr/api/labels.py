from flaskr import database
from flaskr.models.ticket import TicketLabel
from . import apiBluePrint


@apiBluePrint.route('/labels')
def retrieve_labels():
    """
    Geeft alle ticktes over gegeven course.
    """
    # TODO: Controleer of degene die hierheen request permissies heeft.
    labels = TicketLabel.query.all()
    return database.json_list(labels)
