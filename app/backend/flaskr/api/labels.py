from flaskr import database, Iresponse
from flaskr.models.ticket import TicketLabel
from flaskr.models.Label import Label
from flaskr.models.Course import Course
from . import apiBluePrint
import uuid


@apiBluePrint.route('/labels/<course_id>', methods=['GET'])
def retrieve_labels(course_id):
    """
    Geeft alle ticktes over gegeven course.
    """
    print("Getting ticket")
    # TODO: Controleer of degene die hierheen request permissies heeft.
    labels = Label.query.all()
    print(labels)
    return database.json_list(labels)


@apiBluePrint.route('/labels/<course_id>', methods=['POST'])
def create_labels(course_id):
    """
    Add a lable to a course
    """
    print("Creating label")
    name = "Testlabel"

    courseid = course_id
    labelid = uuid.uuid4()
    exist_label = Label.query.filter_by(label_name=name).all()
    print(exist_label)

    course = Course.query.get(courseid)
    if course is None:
        return Iresponse.create_response("", 404)

    if len(exist_label) == 0:
        new_label = Label()
        new_label.label_name = name
        new_label.label_id = labelid

        if not database.addItemSafelyToDB(new_label):
            return Iresponse.internal_server_error()

        course.labels.append(new_label)
    course.labels.append(exist_label[0])

    database.db.session.commit()
    return Iresponse.create_response("", 200)
