from flaskr import database
from flaskr.models.ticket import TicketLabel
from flaskr.models.Label import Label
from . import apiBluePrint
from uuid import uuid4


@apiBluePrint.route('/labels/<course_id>/retrieve')
def retrieve_labels(course_id):
    """
    Geeft alle ticktes over gegeven course.
    """
    print("Getting ticket")
    # TODO: Controleer of degene die hierheen request permissies heeft.
    labels = Label.query.all()
    return database.json_list(labels)

@apiBluePrint.route('/labels/<course_id>/create', methods=['POST'])
def create_labels(course_id):
    """
    Add a lable to a course
    """
    print("Creating ticket")
    # TODO: Controleer of degene die hierheen request permissies heeft.
    # name = escape(request.json["name"])
    name = "Testlabel"
    # courseid = escape(request.json["courseid"])
    courseid = 1;
    labelid = uuid.uuid4()

    new_label = Label()
    label.name = name
    label.courseid = courseid
    label.labelid = labelid

    try:
        database.addItemSafelyToDB(new_label)
    except database.DatabaseInsertException as DBerror:
        print(DBerror)

    return jsonify({'status': "success"})
