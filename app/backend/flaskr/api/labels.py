from flaskr import database, Iresponse, request
from flaskr.models.Label import Label
from flaskr.models.Course import Course
from flaskr.models.user import User
from . import apiBluePrint
from flaskr.utils.json_validation import validate_json
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
    Returns all labels of given course.
    """
    print("Getting label. ")
    # TODO: Controleer of degene die hierheen request permissies heeft.
    course = Course.query.get(course_id)
    if course is None:
        return Iresponse.create_response("", 404)
    return Iresponse.create_response(
        database.serialize_list(course.labels), 200)


@apiBluePrint.route('/labels/<course_id>', methods=['POST'])
def create_labels(course_id):
    """
    Adds a label to a course.
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


@apiBluePrint.route('/labels/<label_id>/select', methods=['POST'])
def selectLabel(label_id):
    json_data = request.get_json()

    if not validate_json(json_data, ["user_id"]):
        return Iresponse.create_response("", 404)

    user_id = json_data["user_id"]
    user = User.query.get(user_id)
    label = Label.query.get(label_id)
    user.labels.append(label)
    database.db.session.add(user)
    database.db.session.commit()
    return Iresponse.create_response("", 200)


@apiBluePrint.route('/labels/<label_id>/deselect', methods=['POST'])
def deselectLabel(label_id):
    json_data = request.get_json()

    if not validate_json(json_data, ["user_id"]):
        return Iresponse.create_response("", 404)

    user_id = json_data["user_id"]
    user = User.query.get(user_id)
    label = Label.query.get(label_id)
    user.labels.remove(label)
    database.db.session.add(user)
    database.db.session.commit()
    return Iresponse.create_response("", 200)


@apiBluePrint.route('/labels/<label_id>/selected', methods=['POST'])
def labelSelected(label_id):
    json_data = request.get_json()

    if not validate_json(json_data, ["user_id"]):
        return Iresponse.create_response("", 404)

    user_id = json_data["user_id"]
    user = User.query.get(user_id)
    label = Label.query.get(label_id)
    return Iresponse.create_response({'bool': label in user.labels}, 200)
