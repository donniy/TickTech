from flaskr import database, Iresponse, request
from flaskr.models.ticket import TicketLabel
from flaskr.models.Label import Label
from flaskr.models.Course import Course
from . import apiBluePrint
import uuid

@apiBluePrint.route('/labels/<label_id>/close', methods=['POST'])
def remove_label(label_id):
    label = Label.query.get(label_id)
    print(label)
    if label is None:
        return Iresponse.create_response("", 404)
    try:
        database.db.session.delete(label)
        database.db.session.commit()
    except Exception:
        print("LOG: Deleting error")
        return Iresponse.internal_server_error()

    return Iresponse.create_response("", 202)


@apiBluePrint.route('/labels/<course_id>', methods=['GET'])
def retrieve_labels(course_id):
    """
    Geeft alle ticktes over gegeven course.
    """
    print("Getting ticket")
    # TODO: Controleer of degene die hierheen request permissies heeft.
    course = Course.query.get(course_id)
    if course is None:
        return Iresponse.create_response("", 404)
    return database.json_list(course.labels)


@apiBluePrint.route('/labels/<course_id>', methods=['POST'])
def create_labels(course_id):
    """
    Add a lable to a course
    """

    data = request.get_json()
    if data is None:
        return Iresponse.create_response("", 404)
    name = data["name"]
    labelid = uuid.uuid4()
    exist_label = Label.query.filter_by(label_name=name).all()

    if exist_label:
        return Iresponse.create_response("", 200)

    course = Course.query.get(course_id)
    if course is None:
        return Iresponse.create_response("", 404)

    new_label = Label()
    new_label.label_name = name
    new_label.label_id = labelid

    if not database.addItemSafelyToDB(new_label):
        return Iresponse.internal_server_error()

    course.labels.append(new_label)
    database.db.session.commit()
    return Iresponse.create_response("", 200)
